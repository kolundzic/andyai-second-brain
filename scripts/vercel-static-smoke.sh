#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/vercel-export export-public >/tmp/vercel-static-smoke-export.log
runtime/bin/vercel-export readiness >/tmp/vercel-static-smoke-readiness.log
runtime/bin/vercel-export bundle >/tmp/vercel-static-smoke-bundle.log
test -f public/index.html
test -f public/manifest.json
test -f vercel.json
test -f public/artifacts/viewer/index.html
test -f public/artifacts/dashboard/bridge-hub-dashboard.html
python3 - <<'PY'
import json
json.load(open("public/manifest.json"))
json.load(open("vercel.json"))
PY
echo "vercel static smoke passed"
