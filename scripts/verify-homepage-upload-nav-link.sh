#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f public/index.html
test -f public/upload/index.html
test -f scripts/patch-homepage-upload-nav.py
test -f brain/web/reports/homepage-upload-nav-link-patch.json

python3 -m py_compile scripts/patch-homepage-upload-nav.py

grep -q 'href="/upload/"' public/index.html
grep -q 'Upload enters through a protected corridor' public/upload/index.html
grep -q 'Homepage navigation must expose Upload' brain/web/reports/homepage-upload-nav-link-patch.json

if grep -F '\\n' public/index.html | grep -E 'Upload|Help|Health|Login|App' >/dev/null 2>&1; then
  echo "Visible escaped newline found near nav after Upload patch."
  exit 1
fi

echo "homepage upload nav link verify passed"
