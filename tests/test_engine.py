import base64
import json
import os
import struct
import subprocess
import sys
import wave
from pathlib import Path

ENGINE = Path(__file__).parents[1] / "engine" / "yamoto_engine.py"

def call(tmp_path, action, **kw):
    env = os.environ.copy()
    env["YAMOTO_DATA_DIR"] = str(tmp_path)
    p = subprocess.run([sys.executable, str(ENGINE)], input=json.dumps({"action": action, **kw}),
                       text=True, capture_output=True, env=env, check=True)
    return json.loads(p.stdout)

def test_health_and_dashboard(tmp_path):
    r = call(tmp_path, "health")
    assert r["ok"] and r["model_status"] == "NOT TRAINED"
    assert r["deception_inference"] == "DISABLED"
    assert call(tmp_path, "dashboard")["sessions"] == 0

def test_dataset_create_and_list(tmp_path):
    assert call(tmp_path, "create_dataset", name="Pilot")["ok"]
    assert call(tmp_path, "list_datasets")["items"][0]["name"] == "Pilot"

def test_experiment_stays_untrained(tmp_path):
    assert call(tmp_path, "create_experiment", name="Baseline")["ok"]
    assert call(tmp_path, "list_experiments")["items"][0]["status"] == "NOT TRAINED"

def test_audio_signal_measurement_and_persistence(tmp_path):
    wav_path = tmp_path / "sample.wav"
    with wave.open(str(wav_path), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000)
        f.writeframes(b"".join(struct.pack("<h", int(8000)) for _ in range(16000)))
    data = base64.b64encode(wav_path.read_bytes()).decode("ascii")
    result = call(tmp_path, "analyze_audio", data=data, source_name="test.wav")
    assert result["ok"] and result["features"]["duration_seconds"] == 1.0
    assert result["features"]["rms_amplitude"] > 0
    records = call(tmp_path, "list_sessions")["items"]
    assert records[0]["kind"] == "audio_signal"

def test_video_action_is_registered_and_rejects_invalid_container(tmp_path):
    result = call(tmp_path, "analyze_video", data=base64.b64encode(b"not a video").decode("ascii"))
    assert result["ok"] is False
    assert "error" in result

def test_invalid_media_rejected(tmp_path):
    result = call(tmp_path, "analyze_audio", data="not-base64")
    assert result["ok"] is False
    assert "error" in result
