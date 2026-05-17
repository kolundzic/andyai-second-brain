#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
scripts/build-knowledge-front-page.sh >/tmp/pack41-knowledge-build.log
test -f public/knowledge/index.html
test -f brain/knowledge/reports/knowledge-front-page.json
test -f brain/knowledge/exports/knowledge-front-page-pack.zip
test -f docs/learning-paths/BEGINNER_LEARNING_PATH.md
test -f docs/learning-paths/OPERATOR_LEARNING_PATH.md
test -f docs/learning-paths/BUILDER_LEARNING_PATH.md
test -f docs/learning-paths/BUSINESS_LEARNING_PATH.md
test -f docs/resources/RESOURCE_CARDS.md
test -f docs/evidence/EVIDENCE_STATUS_LEGEND.md
test -f docs/lifecycle/LIFECYCLE_TAG_SYSTEM.md
grep -q "Knowledge Front Page" README.md
grep -q "living knowledge front page" public/knowledge/index.html
echo "pack41 knowledge front page verify passed"
