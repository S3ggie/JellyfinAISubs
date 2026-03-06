from __future__ import annotations

import json
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Segment:
    start: float
    end: float
    text: str


def _run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or f"Command failed: {' '.join(cmd)}")
    return p.stdout


def detect_media_kind(path: Path) -> str:
    out = _run([
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        str(path),
    ])
    data = json.loads(out)
    streams = data.get("streams", [])
    has_video = any(s.get("codec_type") == "video" and s.get("disposition", {}).get("attached_pic", 0) == 0 for s in streams)
    return "video" if has_video else "audio"


def extract_audio_wav(input_path: Path, out_wav: Path) -> None:
    _run([
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(out_wav),
    ])


def isolate_vocals_demucs(input_wav: Path, out_wav: Path, demucs_device: str = "cpu") -> None:
    work_dir = out_wav.parent / "demucs_tmp"
    work_dir.mkdir(parents=True, exist_ok=True)
    _run([
        "python",
        "-m",
        "demucs.separate",
        "-n",
        "htdemucs",
        "--two-stems=vocals",
        "--device",
        demucs_device,
        "-o",
        str(work_dir),
        str(input_wav),
    ])
    vocals = work_dir / "htdemucs" / input_wav.stem / "vocals.wav"
    if not vocals.exists():
        raise RuntimeError("Demucs did not produce vocals.wav")
    out_wav.write_bytes(vocals.read_bytes())


def fmt_srt(seconds: float) -> str:
    ms = int(round(max(0.0, seconds) * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def fmt_lrc(seconds: float) -> str:
    cs = int(round(max(0.0, seconds) * 100))
    m, rem = divmod(cs, 6000)
    s, cs = divmod(rem, 100)
    return f"[{m:02}:{s:02}.{cs:02}]"


def segments_to_srt(segments: list[Segment]) -> str:
    lines: list[str] = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{fmt_srt(seg.start)} --> {fmt_srt(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def segments_to_lrc(segments: list[Segment]) -> str:
    out = [f"{fmt_lrc(s.start)}{s.text.strip()}" for s in segments if s.text.strip()]
    return "\n".join(out).rstrip() + "\n"


def transcribe(path: Path, model: str = "small", device: str = "cpu", language: str | None = None) -> list[Segment]:
    from faster_whisper import WhisperModel  # lazy import

    wm = WhisperModel(model, device=device, compute_type="int8")
    segs, _ = wm.transcribe(str(path), language=language, vad_filter=True)
    out = [Segment(float(s.start), float(s.end), (s.text or "").strip()) for s in segs if (s.text or "").strip()]
    if not out:
        raise RuntimeError("No subtitle segments generated")
    return out


def generate(
    path: Path,
    out_format: str = "auto",
    model: str = "small",
    device: str = "cpu",
    language: str | None = None,
    isolate_vocals: bool = True,
) -> Path:
    if not path.exists():
        raise FileNotFoundError(str(path))

    kind = detect_media_kind(path)
    if out_format == "auto":
        out_format = "lrc" if kind == "audio" else "srt"

    with tempfile.TemporaryDirectory(prefix="ai-subs-") as td:
        tmp = Path(td)
        source_wav = tmp / "source.wav"
        extract_audio_wav(path, source_wav)

        asr_input = source_wav
        if out_format == "lrc" and isolate_vocals:
            isolated = tmp / "vocals.wav"
            try:
                isolate_vocals_demucs(source_wav, isolated, demucs_device="cpu")
                asr_input = isolated
            except Exception:
                # graceful fallback to non-isolated audio
                asr_input = source_wav

        segments = transcribe(asr_input, model=model, device=device, language=language)

    output = path.with_suffix(f".{out_format}")

    if out_format == "srt":
        output.write_text(segments_to_srt(segments), encoding="utf-8")
    elif out_format == "lrc":
        output.write_text(segments_to_lrc(segments), encoding="utf-8")
    else:
        raise ValueError("format must be auto|srt|lrc")

    return output
