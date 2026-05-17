#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/vercel-export
test -f runtime/lib/vercel_export.py
test -x scripts/vercel-static-smoke.sh
scripts/vercel-static-smoke.sh >/tmp/verify-battle-pack27-smoke.log
python3 -m py_compile runtime/lib/vercel_export.py
echo "battle pack27 verify passed"
