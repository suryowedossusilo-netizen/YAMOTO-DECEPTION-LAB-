# YAMOTO DECEPTION LAB

A Windows-first, local-first desktop workspace for structured multimodal behavioral research.

> **Research limitation:** This software is not a lie detector. It does not determine whether a person is lying. Nervousness, gaze, gestures, facial expressions, and vocal characteristics are not proof of deception.

## Current release

- Application version: **0.2.0**
- Package: Windows x64 NSIS installer
- Installer validation: GitHub Actions build, silent installation, application startup smoke test, bundled engine health check, silent uninstall, and SHA-256 generation passed on a 64-bit Windows CI runner.
- Windows 11 x64 native-machine validation: **not yet completed**.
- The installer is distributed as a GitHub Actions artifact, not as a GitHub Release.

## Installation on Windows

### Requirements

- Windows 10 or Windows 11, 64-bit (x64).
- Approximately 1 GB of free disk space is recommended for the downloaded package and installation.
- Internet access and access to this private GitHub repository to download the installer artifact.

End users do **not** need to install Node.js, Python, Rust, or development dependencies. The packaged installer includes the application and its bundled local engine.

### 1. Download the installer

1. Sign in to GitHub with an account that has access to this repository.
2. Open the [Windows build workflow run #25](https://github.com/suryowedossusilo-netizen/YAMOTO-DECEPTION-LAB-/actions/runs/45602451522).
3. Scroll to the **Artifacts** section at the bottom of the run summary.
4. Download **yamoto-deception-lab-windows-x64**. GitHub downloads it as a ZIP file.
5. Extract the ZIP file. It contains the installer `YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe` and its `.sha256` checksum file.

> GitHub Actions artifacts are temporary downloads and expire according to the retention period configured for the workflow. If this artifact has expired, open the latest successful **Windows build** workflow run and download its artifact instead.

### 2. Verify the installer (recommended)

Open PowerShell in the extracted folder and run:

```powershell
$installer = ".\YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe"
$checksumFile = "$installer.sha256"
$expected = ((Get-Content $checksumFile -Raw).Trim() -split '\\s+')[0]
$actual = (Get-FileHash $installer -Algorithm SHA256).Hash

if ($actual -ne $expected) {
    throw "SHA-256 verification failed. Do not run this installer."
}

Write-Host "SHA-256 verification passed."
```

Only continue if the verification passes.

### 3. Install and launch

1. Double-click `YAMOTO DECEPTION LAB_0.2.0_x64-setup.exe`.
2. Follow the installer prompts and wait for installation to finish.
3. Launch **YAMOTO DECEPTION LAB** from the Windows Start menu or its desktop shortcut, if one was created.
4. Allow camera or microphone access only when needed and only after obtaining the participant's informed consent.

If Windows displays a security warning, verify that the installer came from this repository's successful workflow artifact and that its SHA-256 check passed before deciding whether to continue. Do not bypass a warning for an unverified file.

### 4. Uninstall

1. Close YAMOTO DECEPTION LAB.
2. Open **Settings → Apps → Installed apps** (wording may vary by Windows version).
3. Find **YAMOTO DECEPTION LAB**, select the menu next to it, and choose **Uninstall**.
4. Follow the uninstaller prompts.

Uninstalling the application may not remove user data stored separately in the Windows user profile. Review and back up any research records you need before removing application data. Delete participant data in accordance with your consent and retention policy.

## Implemented research features (v0.2.0)

- React + TypeScript + Vite desktop interface and Tauri 2 Windows shell.
- Local Python JSON engine with SQLite persistence in per-user application data.
- Dataset and experiment registry.
- Opt-in camera preview, single-frame MediaPipe Face Mesh geometry extraction, and sampled video-frame geometry extraction (approximately one frame per second, up to five minutes).
- WAV signal measurements: duration, RMS amplitude, peak, zero-crossing rate, and spectral centroid.
- Local observations are stored in SQLite; raw media is processed in memory and is not saved by the engine. Video is temporarily staged for decoding and removed after processing.
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

## Build and test status

The Windows CI workflow has successfully built the x64 installer and completed automated installation, startup, bundled-engine health, uninstall, and checksum checks on a 64-bit Windows runner. A dedicated Windows 11 x64 native-machine test remains outstanding. See [BUILD-STATUS.md](BUILD-STATUS.md) for implementation and validation details.
