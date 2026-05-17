#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/bridge-feed repo-summary >/tmp/dashboard-feed-smoke-repo.log
runtime/bin/bridge-feed pack-status >/tmp/dashboard-feed-smoke-pack.log
runtime/bin/bridge-feed doctor-report >/tmp/dashboard-feed-smoke-doctor.log
runtime/bin/bridge-feed generate-json >/tmp/dashboard-feed-smoke-json.log
runtime/bin/bridge-feed generate-md >/tmp/dashboard-feed-smoke-md.log
runtime/bin/bridge-feed generate-html >/tmp/dashboard-feed-smoke-html.log
runtime/bin/bridge-feed export >/tmp/dashboard-feed-smoke-export.log
test -f brain/dashboard/feed/bridge-hub-feed.json
test -f brain/dashboard/reports/bridge-hub-dashboard.md
test -f brain/dashboard/html/bridge-hub-dashboard.html
test -f brain/dashboard/exports/bridge-hub-dashboard-feed.zip
python3 - <<'PY'
import json
json.load(open("brain/dashboard/feed/bridge-hub-feed.json"))
PY
echo "dashboard-feed smoke passed"
