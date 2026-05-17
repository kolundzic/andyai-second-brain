#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/client-portal generate >/tmp/client-portal-smoke-generate.log
runtime/bin/client-portal bundle >/tmp/client-portal-smoke-bundle.log
test -f public/client-portal/index.html
test -f brain/client-portal/reports/client-portal-manifest.json
test -f brain/client-portal/exports/client-portal-blueprint.zip
echo "client-portal smoke passed"
