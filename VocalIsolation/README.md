# VocalIsolation

`viso` is a CLI tool that isolates vocals from a media file and exports a WAV output.

## Goal

Run:

```bash
viso input.mp4
```

And get:

```text
input-viso.wav
```

The output file contains isolated vocals from the source media.

## How it works

1. Uses `ffmpeg` to convert/extract the input media to a temporary WAV.
2. Uses `demucs` with `--two-stems=vocals` to separate vocals.
3. Copies the resulting `vocals.wav` to `<input_basename>-viso.wav` next to the original file.

## Requirements

- Python 3.10+
- `ffmpeg` installed and available in PATH
- Python package `demucs`

## Install

```bash
pip install -e .
```

## Usage

```bash
viso <filename>.<container_extension>
```

Examples:

```bash
viso song.mp3
viso clip.mp4
viso interview.mkv
```

Optional flags:

```bash
viso input.mp4 --preset quality --device auto --output ./my-vocals.wav
viso input.mp4 --model htdemucs_ft --device cpu
viso input.mp4 --device cuda
viso input.mp4 --keep-temp
```

## Notes

- First run may be slower while Demucs model weights download.
- CPU is always supported.
- `--preset balanced|quality|fast` is available for workflow consistency.
  - Single-model mode is enforced: presets resolve to `htdemucs` by default.
  - Use `--model <name>` if you want to explicitly try another Demucs model.
- `--device auto` chooses the best available backend (`cuda`/ROCm, then MPS, else CPU).
- If GPU backend fails in `auto`, viso retries on CPU automatically.
- On AMD Linux, ROCm-enabled PyTorch typically appears as `cuda` to Demucs.
- Output is always WAV for predictable downstream workflows.
