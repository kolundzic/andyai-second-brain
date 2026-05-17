#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -f public/help/index.html
test -f public/help/print.html
test -f scripts/build-rich-help-print.py
grep -q "PDF-ready" public/help/index.html
grep -q "../assets/visuals/andyai-second-brain-overview.png" public/help/index.html
grep -q "Visual guide" public/help/index.html
grep -q "Print version" public/help/index.html
grep -q "@media print" public/help/print.html
python3 -m py_compile scripts/build-rich-help-print.py
echo "rich help print polish verify passed"
