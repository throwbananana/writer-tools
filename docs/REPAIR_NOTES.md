# Repair Notes

## Scope

This overlay intentionally focuses on project hygiene and delivery risk:

- dependency reproducibility
- developer tooling
- CI bootstrapping
- smoke-test coverage
- temporary-file cleanup

It does **not** attempt a blind business-logic refactor of the Tk desktop application, because the current repository is already large and has GUI, export, AI, and audio concerns mixed together.

## Why the smoke test targets `ProjectManager`

`writer_app.core.models.ProjectManager` is a good first validation point because it exercises:

- project creation
- serialization
- deserialization
- baseline data integrity

without requiring GUI handles, OS tray access, microphone devices, or text-to-speech engines.

## Recommended follow-up work

1. Split audio-related tests from pure-core tests.
2. Introduce a second CI stage for GUI-safe unit tests.
3. Add a separate workflow for packaging or PyInstaller validation.
4. Decide whether audio should stay in default runtime dependencies or move behind an optional install target.
