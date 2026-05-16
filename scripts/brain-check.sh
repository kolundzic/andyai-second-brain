#!/usr/bin/env bash
set -euo pipefail
echo "🧠 AndyAI Second Brain PACK8 check"
[[ -f ANDYAI_CONTEXT.md ]] && echo "Root context: OK"
[[ -f SECOND_BRAIN_CANON.md ]] && echo "Canon: OK"
[[ -f docs/pack8/PACK8_TOC.md ]] && echo "PACK8 TOC: OK"
[[ -x runtime/bin/brain-lifecycle ]] && echo "Lifecycle CLI: OK"
echo "Lifecycle dirs: $(find brain -maxdepth 1 -type d | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -type f -name '*.json' | wc -l | tr -d ' ')"
echo "Docs: $(find docs -type f | wc -l | tr -d ' ')"
