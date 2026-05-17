#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/homepage-builder
python3 -m py_compile runtime/lib/homepage_builder.py
scripts/homepage-smoke.sh >/tmp/verify-pack39-homepage-smoke.log
test -f docs/web/HOMEPAGE_CONVERSION_SPEC.md
test -f docs/dialog/ASK_YOUR_SECOND_BRAIN_SPEC.md
test -f docs/voice/TALK_WITH_YOUR_SECOND_BRAIN_PREVIEW.md
test -f docs/conversion/SUBSCRIPTION_CONVERSION_COPY.md
echo "pack39 homepage conversion verify passed"
