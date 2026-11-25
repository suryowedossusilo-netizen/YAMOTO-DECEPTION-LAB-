"""Local research engine. Extracts observable media features; never infers deception."""
import base64
import io
import json
import math
import os
import sqlite3
import sys
import wave
from datetime import datetime, timezone
from pathlib import Path

VERSION = "0.3.0"
MAX_MEDIA_BYTES = 15 * 1024 * 1024
SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS sessions(
 id INTEGER PRIMARY KEY, created_at TEXT NOT NULL, kind TEXT NOT NULL,
 source_name TEXT, duration_seconds REAL, notes TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS datasets(
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT DEFAULT '',
 created_at TEXT NOT NULL, participant_count INTEGER DEFAULT 0, label_scheme TEXT DEFAULT ''
);
CREATE TABLE IF NOT EXISTS experiments(
 id INTEGER PRIMARY KEY, name TEXT NOT NULL, dataset_id INTEGER,
 model_type TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'NOT TRAINED',
 created_at TEXT NOT NULL, result_json TEXT DEFAULT '{}'
);
"""

def db_path():
    root = Path(os.environ.get("YAMOTO_DATA_DIR", Path.home() / ".local" / "share" / "YamotoDeceptionLab"))
    root.mkdir(parents=True, exist_ok=True)
    return root / "yamoto.sqlite3"

def connect():
    c = sqlite3.connect(db_path())
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    return c

def now():
    return datetime.now(timezone.utc).isoformat()

def _media_bytes(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Media data is required.")
    encoded = value.split(",", 1)[1] if value.startswith("data:") and "," in value else value
    if len(encoded) > MAX_MEDIA_BYTES * 2:
        raise ValueError("Media exceeds the 15 MB processing limit.")
    raw = base64.b64decode(encoded, validate=True)
    if not raw or len(raw) > MAX_MEDIA_BYTES:
        raise ValueError("Media must be between 1 byte and 15 MB.")
    return raw

def _save_observation(kind, features, duration=None, source_name="local upload"):
    with connect() as c:
        cur = c.execute(
            "INSERT INTO sessions(created_at,kind,source_name,duration_seconds,notes) VALUES(?,?,?,?,?)",
            (now(), kind, source_name[:180], duration, json.dumps(features, ensure_ascii=False))
        )
        return cur.lastrowid

def analyze_frame(q):
    raw = _media_bytes(q.get("data"))
    try:
        import cv2
        import mediapipe as mp
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("MediaPipe/OpenCV is not installed in this build.") from exc

    image = cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("The uploaded file is not a supported image.")
    height, width = image.shape[:2]
    if width * height > 20_000_000:
        raise ValueError("Image dimensions exceed the 20-megapixel processing limit.")

    with mp.solutions.face_mesh.FaceMesh(
        static_image_mode=True, max_num_faces=1, refine_landmarks=True,
        min_detection_confidence=0.5
    ) as mesh:
        result = mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not result.multi_face_landmarks:
        features = {"face_detected": False, "message": "No face detected in this frame."}
    else:
        points = result.multi_face_landmarks[0].landmark
        xs = [p.x for p in points]
        ys = [p.y for p in points]
        def distance(a, b):
            return math.hypot(points[a].x - points[b].x, points[a].y - points[b].y)
        def ratio(vertical_pairs, horizontal_pair):
            vertical = sum(distance(a, b) for a, b in vertical_pairs) / len(vertical_pairs)
            horizontal = distance(*horizontal_pair)
            return round(vertical / horizontal, 5) if horizontal > 1e-8 else None
        features = {
            "face_detected": True,
            "landmarks_count": len(points),
            "frame_width": width,
            "frame_height": height,
            "face_box_normalized": {
                "x": round(max(0.0, min(xs)), 5),
                "y": round(max(0.0, min(ys)), 5),
                "width": round(max(xs) - min(xs), 5),
                "height": round(max(ys) - min(ys), 5)
            },
            "left_eye_openness_geometry": ratio([(160, 144), (158, 153)], (33, 133)),
            "right_eye_openness_geometry": ratio([(385, 380), (387, 373)], (362, 263)),
            "mouth_openness_geometry": ratio([(13, 14)], (78, 308)),
            "interpretation": "Geometry only; not emotion, intent, honesty, or deception."
        }
    record_id = _save_observation("face_geometry", features, source_name=q.get("source_name", "image frame"))
    return {"ok": True, "record_id": record_id, "features": features,
            "limitations": "Single-frame facial geometry cannot establish emotion, intent, honesty, or deception."}

def _wav_samples(raw):
    with wave.open(io.BytesIO(raw), "rb") as wav:
        channels, width, rate, count = wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()
        if width not in (1, 2, 3, 4):
            raise ValueError("Unsupported WAV sample width.")
        if rate < 8000 or rate > 192000 or count <= 0:
            raise ValueError("Unsupported WAV sample rate or empty audio.")
        duration = count / rate
        if duration > 600:
            raise ValueError("Audio is limited to 10 minutes.")
        data = wav.readframes(count)
    import numpy as np
    if width == 1:
        samples = (np.frombuffer(data, dtype=np.uint8).astype(np.float32) - 128.0) / 128.0
    elif width == 2:
        samples = np.frombuffer(data, dtype="<i2").astype(np.float32) / 32768.0
    elif width == 3:
        b = np.frombuffer(data, dtype=np.uint8).reshape(-1, 3)
        vals = b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16)
        vals = np.where(vals & 0x800000, vals - 0x1000000, vals)
        samples = vals.astype(np.float32) / 8388608.0
    else:
        samples = np.frombuffer(data, dtype="<i4").astype(np.float32) / 2147483648.0
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    return samples, rate, duration

def analyze_audio(q):
    raw = _media_bytes(q.get("data"))
    try:
        import numpy as np
    except ImportError as exc:
        raise RuntimeError("NumPy is not installed in this build.") from exc
    samples, rate, duration = _wav_samples(raw)
    if samples.size == 0:
        raise ValueError("Audio contains no samples.")
    rms = float(np.sqrt(np.mean(np.square(samples), dtype=np.float64)))
    peak = float(np.max(np.abs(samples)))
    zcr = float(np.mean(np.signbit(samples[1:]) != np.signbit(samples[:-1]))) if samples.size > 1 else 0.0
    window = samples[:min(samples.size, 8192)]
    spectrum = np.abs(np.fft.rfft(window))
    freqs = np.fft.rfftfreq(window.size, 1.0 / rate)
    centroid = float(np.sum(freqs * spectrum) / np.sum(spectrum)) if np.sum(spectrum) > 0 else 0.0
    features = {
        "duration_seconds": round(duration, 3),
        "sample_rate_hz": rate,
        "channels": "mixed to mono for measurement",
        "rms_amplitude": round(rms, 6),
        "rms_dbfs": round(20 * math.log10(max(rms, 1e-12)), 2),
        "peak_amplitude": round(peak, 6),
        "zero_crossing_rate": round(zcr, 6),
        "spectral_centroid_hz_first_window": round(centroid, 2),
        "interpretation": "Signal measurements only; no speech, emotion, personality, or deception inference."
    }
    record_id = _save_observation("audio_signal", features, duration, q.get("source_name", "WAV audio"))
    return {"ok": True, "record_id": record_id, "features": features,
            "limitations": "Acoustic measurements are affected by microphone, room, codec, language, and recording conditions. They do not establish honesty or deception."}

def handle(q):
    action = q.get("action")
    if action == "health":
        with connect():
            pass
        try:
            import importlib.util
            media_ready = all(importlib.util.find_spec(name) is not None for name in ("mediapipe", "cv2", "numpy"))
        except (ImportError, ValueError):
            media_ready = False
        return {"ok": True, "version": VERSION, "database": "READY",
                "media_features": "READY" if media_ready else "DEPENDENCIES_MISSING",
                "model_status": "NOT TRAINED", "deception_inference": "DISABLED"}
    if action == "dashboard":
        with connect() as c:
            counts = {k: c.execute("select count(*) from " + t).fetchone()[0]
                      for k, t in [("sessions", "sessions"), ("datasets", "datasets"), ("experiments", "experiments")]}
            return {"ok": True, **counts, "model_status": "NOT TRAINED"}
    if action == "analyze_frame":
        return analyze_frame(q)
    if action == "analyze_audio":
        return analyze_audio(q)
    if action in ("create_dataset", "create_experiment"):
        name = str(q.get("name", "")).strip()
        if not name:
            return {"ok": False, "error": "Name is required"}
        with connect() as c:
            if action == "create_dataset":
                cur = c.execute("insert into datasets(name,description,created_at) values(?,?,?)",
                                (name, str(q.get("description", "")), now()))
            else:
                cur = c.execute("insert into experiments(name,model_type,status,created_at) values(?,?,?,?)",
                                (name, str(q.get("model_type", "baseline")), "NOT TRAINED", now()))
            return {"ok": True, "id": cur.lastrowid}
    if action in ("list_datasets", "list_experiments", "list_sessions"):
        table = {"list_datasets": "datasets", "list_experiments": "experiments", "list_sessions": "sessions"}[action]
        with connect() as c:
            return {"ok": True, "items": [dict(r) for r in c.execute("select * from " + table + " order by id desc limit 200")]}
    return {"ok": False, "error": "Unsupported action: " + str(action)}

if __name__ == "__main__":
    try:
        print(json.dumps(handle(json.loads(sys.stdin.read() or "{}")), ensure_ascii=False), flush=True)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), flush=True)
