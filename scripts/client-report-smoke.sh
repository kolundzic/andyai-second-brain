#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/client-report build >/tmp/client-report-smoke-build.log
runtime/bin/client-report generate-json >/tmp/client-report-smoke-json.log
runtime/bin/client-report generate-md >/tmp/client-report-smoke-md.log
runtime/bin/client-report generate-html >/tmp/client-report-smoke-html.log
runtime/bin/client-report export-public >/tmp/client-report-smoke-public.log
runtime/bin/client-report bundle >/tmp/client-report-smoke-bundle.log
test -f brain/client/feed/client-report.json
test -f brain/client/reports/client-report.md
test -f brain/client/html/client-report.html
test -f public/client/index.html
test -f brain/client/exports/client-report-delivery.zip
python3 - <<'PY'
import json
json.load(open("brain/client/feed/client-report.json"))
json.load(open("examples/client-intake/sample-client-intake.json"))
PY
echo "client-report smoke passed"
