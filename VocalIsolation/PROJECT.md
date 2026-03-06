# PROJECT.md — VocalIsolation / viso CLI

## Project Summary

Build a command-line utility named `viso`.

Input:
- Any ffmpeg-readable media file (video or audio).

Output:
- `<basename>-viso.wav` containing isolated vocals.

## Architecture

- Language: Python
- Core dependencies:
  - System: `ffmpeg`
  - Python: `demucs`
- Pipeline:
  1. Validate input path.
  2. Extract/normalize audio to temp WAV via ffmpeg.
  3. Run Demucs vocal separation.
  4. Copy vocals stem to final output filename.
  5. Clean up temp artifacts unless `--keep-temp` is set.

## CLI Contract

```bash
viso <input_file> [--output OUTPUT.wav] [--model MODEL] [--device auto|cpu|cuda|mps] [--keep-temp]
```

Defaults:
- `--output`: `<input_stem>-viso.wav` in input directory.
- `--model`: `htdemucs`
- `--device`: `auto` (prefers GPU backend when available)

## Error Handling Expectations

- Friendly errors for:
  - missing input
  - unsupported/non-readable input
  - missing ffmpeg
  - missing demucs
  - demucs failure
- Non-zero exit code on failure.

## Initial Implementation Scope

- Single-file processing.
- WAV output only.
- Reliable local CLI execution.

## Future Enhancements

- Batch mode (`viso *.mp4` / directory traversal)
- Device selection (`--device cpu|cuda`)
- Progress display
- Optional stems output (instrumental, drums, etc.)
- Config file and presets
