# JellyfinAISubs

End-to-end project for AI-generated subtitles/lyrics with Jellyfin integration.

## What this repo contains

- `backend/` → portable Python service + CLI (`ai-subs`) that generates:
  - `.lrc` for audio/music items
  - `.srt` for video/other items
- `jellyfin-plugin/` → Jellyfin plugin scaffold + repo-manifest template for install catalog
- `deploy/` → Docker Compose for running the backend on a server
- `scripts/bootstrap.sh` → one-command Docker bootstrap

## One-command run (recommended)

```bash
./scripts/bootstrap.sh
```

Then test:

```bash
curl -X POST http://localhost:8099/generate \
  -H 'Content-Type: application/json' \
  -d '{"path":"/media/Movies/movie.mkv","format":"auto"}'
```

## Quick start (backend only)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e .
ai-subs generate "/media/track.wav" --format lrc
ai-subs generate "/media/track.wav" --format lrc --no-isolate-vocals
ai-subs serve --host 0.0.0.0 --port 8099
```

## Docker notes

`deploy/docker-compose.yml` mounts `/srv/media` from host to `/media` in container.
Update this path to match your server media root.

## API endpoint

- `POST /generate`

Example request body:

```json
{
  "path": "/media/Music/song.flac",
  "format": "auto",
  "model": "small",
  "device": "cpu",
  "isolate_vocals": true
}
```
