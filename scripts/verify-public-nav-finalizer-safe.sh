#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f public/index.html
test -f scripts/fix-public-nav-newline-finalizer-safe.py
python3 -m py_compile scripts/fix-public-nav-newline-finalizer-safe.py
python3 scripts/fix-public-nav-newline-finalizer-safe.py >/tmp/v82-0-3-nav-cleanup-report.log

if grep -F '\\n' public/index.html | grep -E 'Health|Help|Knowledge|Pricing|Ask Your Brain' >/dev/null 2>&1; then
  echo "Visible escaped newline still found near public navigation."
  exit 1
fi

grep -q 'href="/help/"' public/index.html
echo "public nav finalizer-safe verify passed"
