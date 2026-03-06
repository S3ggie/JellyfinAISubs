from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

from .core import generate


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="ai-subs")
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Generate subtitle/lyric file")
    g.add_argument("path")
    g.add_argument("--format", choices=["auto", "srt", "lrc"], default="auto")
    g.add_argument("--model", default="small")
    g.add_argument("--device", default="cpu")
    g.add_argument("--language")

    s = sub.add_parser("serve", help="Run API server")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8099)

    return p


def main() -> int:
    args = build_parser().parse_args()

    if args.cmd == "generate":
        out = generate(
            path=Path(args.path).expanduser().resolve(),
            out_format=args.format,
            model=args.model,
            device=args.device,
            language=args.language,
        )
        print(out)
        return 0

    if args.cmd == "serve":
        uvicorn.run("aisubs.api:app", host=args.host, port=args.port, reload=False)
        return 0

    return 1
