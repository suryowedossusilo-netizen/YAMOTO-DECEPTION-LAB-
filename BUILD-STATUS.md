# Build and feature status

- [x] React/TypeScript frontend and Tauri 2 desktop shell are present.
- [x] Local Python JSON engine and SQLite persistence are implemented.
- [x] MediaPipe Face Mesh still-image facial geometry extraction is implemented.
- [x] Sampled video facial geometry extraction is implemented (up to five minutes).
- [x] WAV acoustic signal measurements are implemented.
- [x] Image and audio bytes are processed in memory; video is temporarily staged for decoding and removed after processing.
- [x] Dataset, experiment, and observation records are stored locally.
- [x] Deception inference is explicitly disabled; model state remains NOT TRAINED.
- [ ] Windows installer: waiting for the latest Windows CI workflow and verification of its .exe artifact.
- [ ] Full end-to-end Windows runtime smoke test on a clean Windows 11 x64 machine.
- [ ] Scientific deception classifier: intentionally not implemented; no suitable validated dataset and protocol are available.

Do not mark a feature complete solely because source code was committed. Verify CI, tests, and packaged runtime before release.
