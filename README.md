# YAMOTO DECEPTION LAB

A Windows-first, local-first desktop workspace for structured multimodal behavioral research.

> **Research limitation:** This software is not a lie detector. It does not determine whether a person is lying. Nervousness, gaze, gestures, facial expressions, and vocal characteristics are not proof of deception.

## Implemented research features (v0.3.0)
- React + TypeScript + Vite desktop interface and Tauri 2 Windows shell.
- Local Python JSON engine with SQLite persistence in per-user application data.
- Dataset and experiment registry.
- Opt-in camera preview and single-frame MediaPipe Face Mesh geometry extraction.
- WAV signal measurements: duration, RMS amplitude, peak, zero-crossing rate, and spectral centroid.
- Local observations are stored in SQLite; raw media is processed in memory and is not saved by the engine.
- Media features are measurements only. No emotion, personality, intent, honesty, or deception classifier is present.

## Not implemented / not scientifically validated
No deception classifier, trained model, validated deception dataset, participant-independent model evaluation, or scientific accuracy claim is included. A classifier must not be added or described as validated without consented/licensed data, a preregistered protocol, leakage-resistant participant-independent evaluation, and independent review. The current model state is **NOT TRAINED** and deception inference is **DISABLED**.

## Development
Requirements: Node.js 20+, Python 3.11+, Rust stable, and Tauri Windows prerequisites.

```powershell
npm install
python -m pip install -r engine/requirements.txt pytest
npm run dev
```

Build frontend: `npm run build`. Run engine tests: `python -m pytest tests -q`.

## Privacy and research ethics
Obtain informed consent before capturing or processing participant data. Prefer pseudonymous participant IDs. Restrict raw media access, define retention periods, and support deletion. Raw image/audio bytes are processed in memory and not stored by the engine. Observation feature records are stored locally. See [SECURITY.md](SECURITY.md) and [docs/AI-MODEL-LIMITATIONS.md](docs/AI-MODEL-LIMITATIONS.md).

## Release status
A Windows installer is not available until Windows CI succeeds and its generated installer passes smoke tests. See [BUILD-STATUS.md](BUILD-STATUS.md).
