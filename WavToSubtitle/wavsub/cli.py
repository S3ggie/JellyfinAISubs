from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


class WavSubError(RuntimeError):
    pass


@dataclass
class Segment:
    start: float
    end: float
    text: str


def fmt_srt_timestamp(seconds: float) -> str:
    ms_total = int(round(max(0.0, seconds) * 1000))
    hrs, rem = divmod(ms_total, 3_600_000)
    mins, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"


def fmt_lrc_timestamp(seconds: float) -> str:
    cs_total = int(round(max(0.0, seconds) * 100))
    mins, rem = divmod(cs_total, 6000)
    secs, cs = divmod(rem, 100)
    return f"[{mins:02}:{secs:02}.{cs:02}]"


def segments_to_srt(segments: list[Segment]) -> str:
    lines: list[str] = []
    for i, seg in enumerate(segments, start=1):
        lines.append(str(i))
        lines.append(f"{fmt_srt_timestamp(seg.start)} --> {fmt_srt_timestamp(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def segments_to_lrc(segments: list[Segment]) -> str:
    lines: list[str] = []
    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        lines.append(f"{fmt_lrc_timestamp(seg.start)}{text}")
    return "\n".join(lines).rstrip() + "\n"


def detect_device(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


def transcribe(input_file: Path, model: str, device: str, language: str | None) -> list[Segment]:
    try:
        from faster_whisper import WhisperModel  # type: ignore
    except Exception as exc:
        raise WavSubError("faster-whisper is not installed") from exc

    resolved_device = detect_device(device)

    try:
        wm = WhisperModel(model, device=resolved_device, compute_type="int8")
        seg_iter, _info = wm.transcribe(str(input_file), language=language, vad_filter=True)
    except Exception as exc:
        raise WavSubError(f"Transcription failed: {exc}") from exc

    segments = [Segment(start=s.start, end=s.end, text=s.text) for s in seg_iter]
    if not segments:
        raise WavSubError("No transcript segments were produced")
    return segments


def default_output_base(input_file: Path) -> Path:
    return input_file.with_suffix("")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="wavsub", description="Generate SRT/LRC subtitles from WAV")
    p.add_argument("input_file", help="Input WAV file")
    p.add_argument("--format", choices=["srt", "lrc", "both"], default="both")
    p.add_argument("--model", default="small", help="Whisper model size/name")
    p.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto")
    p.add_argument("--language", help="Optional language code hint (e.g., en)")
    p.add_argument("--output-base", help="Output base path without extension")
    return p


def main() -> int:
    args = build_parser().parse_args()

    input_file = Path(args.input_file).expanduser().resolve()
    if not input_file.exists() or not input_file.is_file():
        print(f"wavsub error: Input file not found: {input_file}", file=sys.stderr)
        return 1

    output_base = Path(args.output_base).expanduser().resolve() if args.output_base else default_output_base(input_file)

    try:
        segments = transcribe(
            input_file=input_file,
            model=args.model,
            device=args.device,
            language=args.language,
        )

        wrote: list[Path] = []
        if args.format in ("srt", "both"):
            srt_path = output_base.with_suffix(".srt")
            srt_path.write_text(segments_to_srt(segments), encoding="utf-8")
            wrote.append(srt_path)

        if args.format in ("lrc", "both"):
            lrc_path = output_base.with_suffix(".lrc")
            lrc_path.write_text(segments_to_lrc(segments), encoding="utf-8")
            wrote.append(lrc_path)

        print("Generated:")
        for p in wrote:
            print(f"- {p}")
        return 0

    except WavSubError as exc:
        print(f"wavsub error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
