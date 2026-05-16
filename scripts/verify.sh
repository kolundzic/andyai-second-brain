#!/usr/bin/env bash
set -euo pipefail
required=("README.md" "ANDYAI_CONTEXT.md" "SECOND_BRAIN_CANON.md" "docs/PACK6_TOC.md" "docs/PACK6_GOVERNED_EXECUTION.md" "runtime/bin/brain" "runtime/bin/brain-query" "runtime/bin/brain-mission" "runtime/bin/brain-exec" "schemas/execution-plan.schema.json" "schemas/execution-result.schema.json" "schemas/approval-decision.schema.json" "skills/governed-agent-execution.md")
for f in "${required[@]}"; do [[ -e "$f" ]] || { echo "missing: $f"; exit 1; }; done
python3 -m json.tool schemas/execution-plan.schema.json >/dev/null
python3 -m json.tool schemas/execution-result.schema.json >/dev/null
python3 -m json.tool schemas/approval-decision.schema.json >/dev/null
runtime/bin/brain-exec help >/dev/null
printf "✅ AndyAI Second Brain verification passed.\n"
