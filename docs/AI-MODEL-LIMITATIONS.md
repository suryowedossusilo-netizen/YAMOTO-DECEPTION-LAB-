# AI model limitations and validation policy

## No lie-detection claim
YAMOTO DECEPTION LAB is a research observation tool, not a lie detector. Facial geometry, gaze, posture, gestures, voice acoustics, stress, or nervousness do not establish deception. The application must not output a person's truthfulness score or label a person as lying.

## What the current feature extractors do
- MediaPipe Face Mesh returns normalized facial landmark geometry for one still frame.
- The audio module returns basic signal measurements from WAV audio.
- These outputs are descriptive measurements, not emotion recognition or psychological diagnoses.
- Results can vary with camera angle, lighting, occlusion, skin/face presentation, microphone, room, language, codec, and recording quality.

## Requirements before any predictive research
Any future predictive experiment requires:
1. Documented informed consent and lawful, licensed data.
2. A clearly defined research question and label provenance.
3. Participant-independent train/validation/test splits to prevent identity leakage.
4. Preregistered metrics, confidence intervals, calibration and subgroup/error analysis.
5. Independent review, reproducible code, and explicit limitations.
6. No deployment for employment, policing, education, healthcare, access control, or other consequential decisions.

Until all requirements are met, model state remains NOT TRAINED and deception inference remains DISABLED.
