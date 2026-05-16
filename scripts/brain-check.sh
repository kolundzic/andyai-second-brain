#!/usr/bin/env bash
set -euo pipefail
printf "🧠 AndyAI Second Brain PACK6 check\n"
[[ -f ANDYAI_CONTEXT.md ]] && echo "Root context: OK"
[[ -f SECOND_BRAIN_CANON.md ]] && echo "Canon: OK"
[[ -f docs/PACK6_TOC.md ]] && echo "PACK6 TOC: OK"
[[ -x runtime/bin/brain-exec ]] && echo "Execution runtime CLI: OK"
echo "Execution plans: $(find brain/execution-plans -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Execution evidence: $(find brain/execution-evidence -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Execution approvals: $(find brain/execution-approvals -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -type f | wc -l | tr -d ' ')"
echo "Skills: $(find skills -type f | wc -l | tr -d ' ')"
