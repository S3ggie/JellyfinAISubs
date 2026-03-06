# Jellyfin Plugin

This folder now includes a functional plugin backend hook (service endpoint) plus packaging scaffolding.

## Implemented

- Plugin config page (`meta/configPage.html`) to set backend URL
- Plugin API endpoint inside Jellyfin:
  - `POST /AISubs/Generate`
- Endpoint resolves item file path and calls AI-Subs backend `POST /generate`

## Request body for Jellyfin plugin endpoint

```json
{
  "itemId": "<Jellyfin item GUID>",
  "format": "auto",
  "isolateVocals": true
}
```

`format=auto` behavior remains:
- audio/music -> `.lrc`
- video/other -> `.srt`

## Build plugin

```bash
cd AI.Subs.Jellyfin
dotnet restore
dotnet publish -c Release -o ../../artifacts/plugin
```

Package output:

```bash
cd ../../artifacts/plugin
zip -r AI.Subs.Jellyfin_0.1.0.0.zip .
```

Then publish that zip and wire `repo-manifest/manifest.template.json` as described in `../SETUP.md`.
