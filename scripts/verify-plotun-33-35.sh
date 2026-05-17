#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/launch-operator
python3 -m py_compile runtime/lib/launch_operator.py
scripts/launch-operator-smoke.sh >/tmp/verify-plotun-33-35-launch-smoke.log
echo "plotun 33-35 verify passed"
