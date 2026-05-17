#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/client-report
test -f runtime/lib/client_report.py
test -x scripts/client-report-smoke.sh
scripts/client-report-smoke.sh >/tmp/verify-battle-pack28-smoke.log
python3 -m py_compile runtime/lib/client_report.py
echo "battle pack28 verify passed"
