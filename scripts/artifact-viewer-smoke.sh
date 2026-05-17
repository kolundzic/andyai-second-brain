#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/artifact-viewer collect >/tmp/artifact-viewer-smoke-collect.log
runtime/bin/artifact-viewer generate-json >/tmp/artifact-viewer-smoke-json.log
runtime/bin/artifact-viewer generate-md >/tmp/artifact-viewer-smoke-md.log
runtime/bin/artifact-viewer generate-html >/tmp/artifact-viewer-smoke-html.log
runtime/bin/artifact-viewer export >/tmp/artifact-viewer-smoke-export.log
test -f brain/viewer/index/artifact-index.json
test -f brain/viewer/reports/artifact-viewer.md
test -f brain/viewer/html/index.html
test -f brain/viewer/exports/artifact-viewer-export.zip
python3 - <<'PY'
import json
json.load(open("brain/viewer/index/artifact-index.json"))
PY
echo "artifact-viewer smoke passed"
