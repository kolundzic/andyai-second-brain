#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/memory-index build >/tmp/memory-index-build.log
runtime/bin/memory-index bundle >/tmp/memory-index-bundle.log
test -f public/memory/index.html
test -f public/timeline/index.html
test -f brain/memory/reports/memory-index.json
test -f brain/memory/exports/memory-index-search-timeline-pack.zip
grep -q "Searchable memory prototype" public/memory/index.html
grep -q "Memory has time" public/timeline/index.html
grep -q "real_confidential_memory_allowed" brain/memory/reports/memory-index.json
echo "memory index smoke passed"
