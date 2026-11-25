# Architecture
React + TypeScript + Vite provide the desktop UI. Tauri 2 hosts the Windows shell and exposes a narrow command to a local Python process. Python owns SQLite persistence in the per-user app-data directory. Camera preview is opt-in and does not record. This scaffold performs no behavioral inference.
