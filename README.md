# YAMOTO DECEPTION LAB

A Windows-first desktop workspace for structured multimodal behavioral research.

> **Research limitation:** This software is not a lie detector. It does not determine whether a person is lying. Nervousness, gaze, gestures, facial expressions, and vocal characteristics are not proof of deception.

## Current scope (v0.2.0 scaffold)
- React + TypeScript + Vite desktop interface.
- Tauri 2 desktop shell.
- Python JSON-line engine with local SQLite storage.
- Dataset and experiment registry.
- Webcam preview with explicit browser permission; no recording.
- Video metadata inspection only when OpenCV is installed.
- Model state remains **NOT TRAINED**.

## Not implemented / not validated
MediaPipe inference, facial or pose feature extraction, audio analysis, ML training, deception classification, validated performance metrics, report export, and a signed Windows installer are not implemented or verified. Do not present these as working features.

## Development
Requirements: Node.js 20+, Python 3.11+, Rust stable, and Tauri Windows prerequisites.

```powershell
npm install
python -m pip install -r engine/requirements.txt pytest
npm run dev
```

Build frontend: `npm run build`. Run engine tests: `python -m pytest tests -q`.

## Privacy and research ethics
Obtain informed consent before capturing or processing participant data. Prefer pseudonymous participant IDs. Keep raw media access restricted, define retention periods, and support deletion. Do not infer deception from isolated behavioral cues. See [SECURITY.md](SECURITY.md) and [docs/AI-MODEL-LIMITATIONS.md](docs/AI-MODEL-LIMITATIONS.md).

## Release status
Windows installer and portable package are not available until a Windows CI build succeeds and the produced artifacts pass smoke tests. See [BUILD-STATUS.md](BUILD-STATUS.md).
