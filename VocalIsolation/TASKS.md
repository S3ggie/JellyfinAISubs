# TASKS.md — VocalIsolation

## Phase 1: Planning

- [x] Define CLI behavior and output contract.
- [x] Choose tech stack (Python + ffmpeg + demucs).
- [x] Define error-handling and defaults.

## Phase 2: Coding

- [x] Create Python package scaffold.
- [x] Implement CLI entrypoint `viso`.
- [x] Implement ffmpeg extraction to temp WAV.
- [x] Implement demucs vocals separation call.
- [x] Add device selection with auto-detect (`--device auto|cpu|cuda|mps`) for AMD/ROCm compatibility.
- [x] Implement final output naming (`<basename>-viso.wav`).
- [x] Implement cleanup + `--keep-temp` support.

## Phase 3: Testing

- [ ] Add unit tests for path and command generation.
- [ ] Add failure-path tests (missing tools, subprocess failures).
- [ ] Add smoke test docs for manual local validation.

## Phase 4: Optimization

- [ ] Add optional device flag (`--device cpu|cuda`).
- [ ] Improve user feedback/progress output.
- [ ] Benchmark model choices and document trade-offs.
- [ ] Optional: avoid unnecessary re-encoding where practical.
