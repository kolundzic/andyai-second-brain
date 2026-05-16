#!/usr/bin/env bash
set -euo pipefail
echo "🧠 AndyAI Second Brain PACK2 check"
[[ -f ANDYAI_CONTEXT.md ]] && echo "Root context: OK" || exit 1
[[ -f SECOND_BRAIN_CANON.md ]] && echo "Canon: OK" || exit 1
[[ -f docs/toc/PACK2_v2.1_to_v4.0_TOC.md ]] && echo "PACK2 TOC: OK" || exit 1
[[ -x runtime/bin/brain ]] && echo "Runtime CLI: OK" || exit 1
echo "Runtime docs: $(find docs/runtime -type f | wc -l | tr -d ' ')"
echo "Runtime templates: $(find runtime/templates -type f | wc -l | tr -d ' ')"
echo "Skills: $(find skills -maxdepth 1 -type f | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -maxdepth 1 -type f | wc -l | tr -d ' ')"
echo "Examples: $(find examples -maxdepth 1 -type f | wc -l | tr -d ' ')"
