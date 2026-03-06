from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .core import generate

app = FastAPI(title="AI-Subs Backend", version="0.1.0")


class GenerateRequest(BaseModel):
    path: str
    format: str = "auto"
    model: str = "small"
    device: str = "cpu"
    language: str | None = None
    isolate_vocals: bool = True


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/generate")
def generate_endpoint(req: GenerateRequest) -> dict:
    try:
        out = generate(
            path=Path(req.path).expanduser().resolve(),
            out_format=req.format,
            model=req.model,
            device=req.device,
            language=req.language,
            isolate_vocals=req.isolate_vocals,
        )
        return {"ok": True, "output": str(out)}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
