#!/usr/bin/env bash
set -euo pipefail
echo "🧠 AndyAI Second Brain PACK7 check"
[[ -f ANDYAI_CONTEXT.md ]] && echo "Root context: OK"
[[ -f SECOND_BRAIN_CANON.md ]] && echo "Canon: OK"
[[ -f docs/PACK7_TRUST_LEDGER_TOC.md ]] && echo "PACK7 TOC: OK"
[[ -x runtime/bin/brain-trust ]] && echo "Trust runtime CLI: OK"
echo "Trust dirs: $(find brain -maxdepth 1 -type d | grep -E 'trust|audit|accountability|integrity' | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -maxdepth 1 -type f -name '*.json' | wc -l | tr -d ' ')"
echo "Skills: $(find skills -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
