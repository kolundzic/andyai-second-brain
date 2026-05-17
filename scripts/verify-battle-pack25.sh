#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/bridge-feed
test -f runtime/lib/bridge_feed.py
test -x scripts/dashboard-feed-smoke.sh
scripts/dashboard-feed-smoke.sh >/tmp/verify-battle-pack25-smoke.log
python3 -m py_compile runtime/lib/bridge_feed.py
echo "battle pack25 verify passed"
