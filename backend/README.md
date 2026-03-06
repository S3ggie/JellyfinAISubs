# ai-subs backend

Unified CLI + API service.

## CLI

```bash
ai-subs generate /media/file.m4a
ai-subs generate /media/file.mkv --format srt
```

## API

```bash
curl -X POST http://localhost:8099/generate \
  -H 'Content-Type: application/json' \
  -d '{"path":"/media/Music/song.wav"}'
```
