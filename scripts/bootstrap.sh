#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/deploy"
docker compose up -d --build

echo "AI-Subs backend is up on http://localhost:8099"
