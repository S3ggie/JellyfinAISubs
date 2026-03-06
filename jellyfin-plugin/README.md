# Jellyfin Plugin (scaffold)

This plugin will add item actions in Jellyfin:
- Generate subtitles with AI (video/other)
- Generate lyrics with AI (audio/music)

It calls the backend API:
- `POST http://<backend>:8099/generate`

Payload example:
```json
{
  "path": "/media/Music/track.flac",
  "format": "auto"
}
```

Current status: scaffold/spec only. Implementation next phase.
