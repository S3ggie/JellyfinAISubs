# PROJECT.md — WavToSubtitle / wavsub CLI

## Project Summary

Build a command-line utility named `wavsub`.

Input:
- `.wav` file

Output:
- `.srt` and/or `.lrc` subtitle files with timestamps

## Architecture

- Language: Python
- Core dependency: `faster-whisper`
- Pipeline:
  1. Validate input path
  2. Transcribe with faster-whisper
  3. Format segments into SRT/LRC
  4. Write outputs beside input (or explicit output base)

## CLI Contract

```bash
wavsub <input.wav> [--format srt|lrc|both] [--model MODEL] [--device auto|cpu|cuda] [--language LANG] [--output-base PATH]
```

Defaults:
- `--format`: `both`
- `--model`: `small`
- `--device`: `auto`

## Error Handling

- Missing input file
- Unsupported file
- Whisper/model load errors
- Empty transcription result

## Initial Scope

- WAV input only
- Segment-level timestamps
- Basic SRT and LRC output

## Future Enhancements

- Word-level timestamps
- VAD and punctuation tuning
- Batch mode (directory/file glob)
- Translation mode (e.g., to English)
