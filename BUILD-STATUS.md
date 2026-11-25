# Build and feature status

- [x] React/TypeScript frontend and Tauri 2 desktop shell are present.
- [x] Local Python JSON engine and SQLite persistence are implemented.
- [x] MediaPipe Face Mesh single-frame facial geometry extraction is implemented (feature measurements only).
- [x] WAV acoustic signal measurements are implemented (feature measurements only).
- [x] Media observation metadata is stored locally; raw media is not persisted by the engine.
- [x] Deception inference is explicitly disabled; model state remains NOT TRAINED.
- [ ] Windows installer: awaiting a successful CI run and artifact smoke test.
- [ ] Camera/audio workflow UI integration and full end-to-end Windows validation.
- [ ] Scientific deception classifier: intentionally not implemented; no suitable validated dataset/protocol is available.

Do not mark a feature complete solely because source code was committed. Verify CI, tests, and packaged runtime before release.
