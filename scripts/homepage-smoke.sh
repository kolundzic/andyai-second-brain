#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/homepage-builder build >/tmp/homepage-builder-build.log
runtime/bin/homepage-builder report >/tmp/homepage-builder-report.log
runtime/bin/homepage-builder bundle >/tmp/homepage-builder-bundle.log
test -f public/index.html
test -f brain/web/reports/homepage-conversion-report.json
test -f brain/web/exports/homepage-conversion-pack.zip
grep -q "Ask Your Second Brain" public/index.html
grep -q "Talk with your 2nd Brain" public/index.html
grep -q "Plans built for real AI work" public/index.html
grep -q "Trust is the product boundary" public/index.html
echo "homepage smoke passed"
