#!/usr/bin/env bash
set -euo pipefail
required=(
  README.md
  ANDYAI_CONTEXT.md
  SECOND_BRAIN_CANON.md
  docs/toc/PACK2_v2.1_to_v4.0_TOC.md
  docs/runtime/WORKING_BRAIN_RUNTIME_LAYER.md
  runtime/bin/brain
  runtime/lib/common.sh
  runtime/templates/memory-entry.md
  runtime/templates/decision.md
  runtime/templates/evidence-link.md
  schemas/runtime-command.schema.json
  schemas/runtime-memory-entry.schema.json
  skills/runtime-brain-index.md
  examples/sample-runtime-session.md
)
for f in "${required[@]}"; do
  [[ -f "$f" ]] || { echo "Missing $f"; exit 1; }
done
[[ -x runtime/bin/brain ]] || { echo "runtime/bin/brain not executable"; exit 1; }
[[ -x scripts/brain-check.sh ]] || { echo "scripts/brain-check.sh not executable"; exit 1; }
echo "✅ AndyAI Second Brain PACK2 verification passed."
