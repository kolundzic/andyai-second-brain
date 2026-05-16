#!/usr/bin/env bash
set -euo pipefail
required=("README.md" "ANDYAI_CONTEXT.md" "SECOND_BRAIN_CANON.md" "docs/PACK3_TOC.md" "docs/REAL_BRAIN_OPERATIONS_MODEL.md" "runtime/bin/brain" "runtime/docs/REAL_BRAIN_OPERATIONS.md" "schemas/operation-card.schema.json" "skills/real-brain-operations.md")
for f in "${required[@]}"; do [[ -e "$f" ]] || { echo "Missing required file: $f"; exit 1; }; done
chmod +x runtime/bin/brain scripts/brain-check.sh 2>/dev/null || true
python3 -m json.tool schemas/operation-card.schema.json >/dev/null
./runtime/bin/brain index >/tmp/andyai_second_brain_verify_index.log
./runtime/bin/brain report >/tmp/andyai_second_brain_verify_report.log
./scripts/brain-check.sh >/tmp/andyai_second_brain_check.log
echo "✅ AndyAI Second Brain PACK3 verification passed."
