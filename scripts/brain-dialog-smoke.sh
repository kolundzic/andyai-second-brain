#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/brain-dialog build >/tmp/brain-dialog-build.log
runtime/bin/brain-dialog bundle >/tmp/brain-dialog-bundle.log
test -f public/dialog/index.html
test -f public/help/index.html
test -f public/capture/index.html
test -f brain/dialog/reports/brain-dialog-report.json
test -f brain/dialog/exports/brain-dialog-upload-memory-pack.zip
grep -q "Ask Your Second Brain" public/dialog/index.html
grep -q "Drop files here" public/dialog/index.html
grep -q "Mobile camera scan" public/dialog/index.html
grep -q "Full README text" public/help/index.html
grep -q "Camera Scan" public/capture/index.html
grep -q "/help/" public/index.html
echo "brain-dialog smoke passed"
