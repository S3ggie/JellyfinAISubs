# Jellyfin Plugin Packaging + Repo Manifest

This repo includes a plugin scaffold and a repository manifest template.

## 1) Build plugin zip

From `jellyfin-plugin/AI.Subs.Jellyfin` on a machine with .NET SDK:

```bash
dotnet restore
dotnet publish -c Release -o ../../artifacts/plugin
cd ../../artifacts/plugin
zip -r AI.Subs.Jellyfin_0.1.0.0.zip .
sha256sum AI.Subs.Jellyfin_0.1.0.0.zip
```

## 2) Publish zip to GitHub release

Create release `v0.1.0` and upload `AI.Subs.Jellyfin_0.1.0.0.zip`.

## 3) Create plugin catalog manifest URL

Copy `repo-manifest/manifest.template.json` to `repo-manifest/manifest.json` and replace:
- `<SHA256_OF_ZIP>` with actual hash
- URL/version/targetAbi if needed

Host this JSON somewhere public (GitHub Pages or raw URL).

## 4) Install in Jellyfin

- Dashboard -> Plugins -> Repositories -> Add
- Name: `AI Subs Jellyfin`
- URL: `<your hosted manifest.json URL>`
- Save, refresh catalog, install plugin

## 5) Configure plugin

Set backend URL to your Docker backend service, e.g.:

`http://your-server-ip:8099`
