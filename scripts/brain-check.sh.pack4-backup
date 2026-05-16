#!/usr/bin/env bash
set -euo pipefail

echo "🧠 AndyAI Second Brain PACK4 check"
echo "Root context: $([[ -f ANDYAI_CONTEXT.md ]] && echo OK || echo MISSING)"
echo "Canon: $([[ -f SECOND_BRAIN_CANON.md ]] && echo OK || echo MISSING)"
echo "PACK4 TOC: $([[ -f docs/PACK4_QUERY_RETRIEVAL_CONTEXT_ASSEMBLY_TOC.md ]] && echo OK || echo MISSING)"
echo "Brain query CLI: $([[ -x runtime/bin/brain-query ]] && echo OK || echo MISSING)"
echo "Query docs: $(find docs/pack4 -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Skills: $(find skills -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Context bundles: $(find brain/context/bundles -type f 2>/dev/null | wc -l | tr -d ' ')"
