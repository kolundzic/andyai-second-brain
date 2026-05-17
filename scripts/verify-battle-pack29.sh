#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/privacy-firewall
test -f runtime/lib/privacy_firewall.py
test -x scripts/privacy-firewall-smoke.sh
scripts/privacy-firewall-smoke.sh >/tmp/verify-battle-pack29-smoke.log
python3 -m py_compile runtime/lib/privacy_firewall.py
echo "battle pack29 verify passed"
