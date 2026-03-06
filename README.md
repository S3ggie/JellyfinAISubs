# JellyfinAISubs

End-to-end project for AI-generated subtitles/lyrics with Jellyfin integration.

## What this repo contains

- `backend/` → portable Python service + CLI (`ai-subs`) that generates:
  - `.lrc` for audio/music items
  - `.srt` for video/other items
- `jellyfin-plugin/` → Jellyfin plugin scaffold to add UI actions and call backend API
- `deploy/` → Docker Compose for running the backend on a server

## Quick start (backend only)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
ai-subs generate "/media/track.wav" --format lrc
ai-subs serve --host 0.0.0.0 --port 8099
```

## Quick start (Docker)

```bash
cd deploy
docker compose up -d --build
```

Backend API endpoint:
- `POST /generate`

