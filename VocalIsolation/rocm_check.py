#!/usr/bin/env python3
"""Quick local check for AMD/ROCm readiness for viso."""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys


def run(cmd: list[str]) -> str:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return out.strip()
    except Exception as exc:
        return f"unavailable ({exc})"


print("== viso AMD/ROCm readiness ==")
print("python:", sys.version.split()[0])
print("ffmpeg:", shutil.which("ffmpeg") or "missing")
print("rocminfo:", shutil.which("rocminfo") or "missing")
print("rocm-smi:", shutil.which("rocm-smi") or "missing")

if shutil.which("rocminfo"):
    print("\nrocminfo (first lines):")
    print("\n".join(run(["rocminfo"]).splitlines()[:12]))

if importlib.util.find_spec("torch") is None:
    print("\ntorch: missing")
    raise SystemExit(0)

import torch  # type: ignore

print("\ntorch:", torch.__version__)
print("torch.cuda.is_available:", torch.cuda.is_available())
print("torch.version.hip:", getattr(torch.version, "hip", None))
print("torch.version.cuda:", getattr(torch.version, "cuda", None))
