# WavToSubtitle

`wavsub` is a CLI tool to transcribe WAV audio and export subtitle files.

## Goal

Run:

```bash
wavsub input.wav
```

And get:

- `input.srt`
- `input.lrc`

## Features

- WAV input (any ffmpeg-readable audio can be added later)
- SRT subtitle export
- LRC lyric export
- Model/device selection for Whisper backend

## Requirements

- Python 3.10+
- `faster-whisper`

## Install

```bash
pip install -e .
```

## Usage

```bash
wavsub <file.wav>
```

Examples:

```bash
wavsub song.wav
wavsub speech.wav --format srt
wavsub song.wav --model medium --device cpu --format both
```

## Options

- `--format {srt,lrc,both}` (default: `both`)
- `--model` (default: `small`)
- `--device {auto,cpu,cuda}` (default: `auto`)
- `--language` (optional language hint, e.g. `en`)

