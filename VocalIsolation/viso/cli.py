from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


class VisoError(RuntimeError):
    pass


def ensure_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise VisoError(f"Required tool not found in PATH: {name}")


def run_command(cmd: list[str]) -> None:
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        raise VisoError(f"Command failed: {' '.join(cmd)}") from exc


def detect_best_device() -> str:
    """
    Returns the best available device for demucs.

    Notes:
    - For ROCm PyTorch builds, torch.cuda.is_available() is True and torch.version.hip is set.
      Demucs still expects device='cuda'.
    """
    try:
        import torch  # type: ignore

        if torch.cuda.is_available():
            return "cuda"
        mps = getattr(torch.backends, "mps", None)
        if mps and mps.is_available():
            return "mps"
    except Exception:
        pass

    return "cpu"


def resolve_device(requested: str) -> str:
    if requested == "auto":
        return detect_best_device()
    return requested


def default_output_path(input_path: Path) -> Path:
    return input_path.with_name(f"{input_path.stem}-viso.wav")


def extract_audio_to_wav(input_path: Path, wav_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "2",
        "-ar",
        "44100",
        str(wav_path),
    ]
    run_command(cmd)


def run_demucs(input_wav: Path, out_dir: Path, model: str, device: str) -> Path:
    cmd = [
        sys.executable,
        "-m",
        "demucs.separate",
        "-n",
        model,
        "--two-stems=vocals",
        "--device",
        device,
        "-o",
        str(out_dir),
        str(input_wav),
    ]
    run_command(cmd)

    vocals_path = out_dir / model / input_wav.stem / "vocals.wav"
    if not vocals_path.exists():
        raise VisoError(f"Demucs output not found: {vocals_path}")
    return vocals_path


def apply_preset(model: str, preset: str) -> str:
    # Force single-model behavior for all presets.
    # Some demucs names are bags/ensembles; `htdemucs` is a reliable single-model default.
    if model != "htdemucs":
        return model

    if preset == "quality":
        return "htdemucs"
    if preset == "fast":
        return "htdemucs"
    return "htdemucs"


def isolate_vocals(
    input_file: Path,
    output_file: Path | None,
    model: str,
    keep_temp: bool,
    requested_device: str,
) -> Path:
    if not input_file.exists() or not input_file.is_file():
        raise VisoError(f"Input file not found: {input_file}")

    ensure_tool("ffmpeg")

    device = resolve_device(requested_device)

    with tempfile.TemporaryDirectory(prefix="viso-") as tmp:
        tmp_dir = Path(tmp)
        wav_path = tmp_dir / f"{input_file.stem}.wav"
        demucs_out = tmp_dir / "demucs_out"

        extract_audio_to_wav(input_file, wav_path)

        try:
            vocals_src = run_demucs(wav_path, demucs_out, model, device)
        except VisoError:
            if requested_device == "auto" and device != "cpu":
                print(
                    f"viso: {device} failed, retrying on cpu...",
                    file=sys.stderr,
                )
                vocals_src = run_demucs(wav_path, demucs_out, model, "cpu")
            else:
                raise

        final_output = output_file or default_output_path(input_file)
        final_output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(vocals_src, final_output)

        if keep_temp:
            keep_dir = input_file.parent / f"{input_file.stem}-viso-temp"
            if keep_dir.exists():
                shutil.rmtree(keep_dir)
            shutil.copytree(tmp_dir, keep_dir)

        return final_output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="viso",
        description="Isolate vocals from a media file and save as WAV",
    )
    parser.add_argument("input_file", help="Input media file path (audio/video)")
    parser.add_argument("--output", "-o", help="Output WAV file path")
    parser.add_argument("--model", default="htdemucs", help="Demucs model (default: htdemucs)")
    parser.add_argument(
        "--preset",
        choices=["balanced", "quality", "fast"],
        default="balanced",
        help="Model preset. In single-model mode, all presets use htdemucs unless --model is set.",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda", "mps"],
        default="auto",
        help="Compute device for Demucs (default: auto)",
    )
    parser.add_argument("--keep-temp", action="store_true", help="Keep temporary working files")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_file = Path(args.input_file).expanduser().resolve()
    output_file = Path(args.output).expanduser().resolve() if args.output else None

    try:
        resolved_model = apply_preset(args.model, args.preset)
        out = isolate_vocals(
            input_file=input_file,
            output_file=output_file,
            model=resolved_model,
            keep_temp=args.keep_temp,
            requested_device=args.device,
        )
        resolved = resolve_device(args.device)
        print(f"Vocal isolation complete ({resolved}, model={resolved_model}): {out}")
        return 0
    except VisoError as exc:
        print(f"viso error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
