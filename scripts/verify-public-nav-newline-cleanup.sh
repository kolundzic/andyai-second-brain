#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f public/index.html
test -f scripts/fix-public-nav-newline.py
python3 -m py_compile scripts/fix-public-nav-newline.py

if grep -F '\\n        <a href="/help/"' public/index.html >/dev/null 2>&1; then
  echo "Literal escaped newline found before Help link."
  exit 1
fi

if grep -F '\\n' public/index.html | grep -E 'Help|Knowledge|Health' >/dev/null 2>&1; then
  echo "Literal escaped newline found near public navigation."
  exit 1
fi

grep -q 'href="/help/"' public/index.html
echo "public nav newline cleanup verify passed"
