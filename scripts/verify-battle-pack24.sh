#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/brain-doctor
test -f runtime/lib/brain_doctor.py
test -x scripts/brain-doctor-smoke.sh
scripts/brain-doctor-smoke.sh >/tmp/verify-battle-pack24-smoke.log
python3 -m py_compile runtime/lib/brain_doctor.py
echo "battle pack24 verify passed"
