# Testing
Run engine tests: `python -m pytest tests -q`. Build frontend: `npm install && npm run build`. Windows release requires a clean Windows runner with Node, Rust, Python, and Tauri prerequisites. Smoke-test installer launch, local database creation, camera permission behavior, and data retention before release.


## Automated Windows release pipeline

The single Windows release workflow performs frontend compilation, Python engine packaging, packaged-engine health checks, Python tests, icon validation, NSIS installer creation, silent install, installed-engine health check, desktop startup smoke test, silent uninstall, SHA-256 generation, and artifact upload.

The GitHub-hosted Windows x64 runner validates installation and startup on the hosted Windows environment. It is not a native Windows 11 client machine; a final Windows 11 x64 acceptance run still requires a registered Windows 11 self-hosted runner or a real Windows 11 test device. Do not label the hosted-runner result as a Windows 11 test.
