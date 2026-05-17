#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/artifact-viewer
test -f runtime/lib/artifact_viewer.py
test -x scripts/artifact-viewer-smoke.sh
scripts/artifact-viewer-smoke.sh >/tmp/verify-battle-pack26-smoke.log
python3 -m py_compile runtime/lib/artifact_viewer.py
echo "battle pack26 verify passed"
