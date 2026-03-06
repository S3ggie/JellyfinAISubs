# ai-subs backend

Unified CLI + API service.

## CLI

```bash
ai-subs generate /media/file.m4a
ai-subs generate /media/file.m4a --format lrc
ai-subs generate /media/file.mkv --format srt
ai-subs generate /media/file.m4a --no-isolate-vocals
```

## API

```bash
curl -X POST http://localhost:8099/generate \
  -H 'Content-Type: application/json' \
  -d '{"path":"/media/Music/song.wav","format":"auto","isolate_vocals":true}'
```
