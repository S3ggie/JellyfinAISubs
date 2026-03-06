# TASKS.md — WavToSubtitle

## Phase 1: Planning

- [x] Define input/output contract for WAV -> SRT/LRC.
- [x] Select initial stack (`faster-whisper`).
- [x] Define CLI flags and defaults.

## Phase 2: Coding

- [x] Create package scaffold and CLI entrypoint.
- [x] Implement transcription pipeline.
- [x] Implement SRT formatter.
- [x] Implement LRC formatter.
- [x] Implement output file writing and naming.

## Phase 3: Testing

- [x] Add formatter unit tests (timestamps + line formatting).
- [x] Add CLI argument and path tests.
- [x] Add mocked transcription integration test.

## Phase 4: Optimization

- [ ] Add VAD and beam-size controls.
- [ ] Add batch mode.
- [ ] Add word-level subtitle mode.
