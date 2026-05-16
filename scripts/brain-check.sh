#!/usr/bin/env bash
set -euo pipefail
[[ -f ANDYAI_CONTEXT.md ]] && echo "Root context: OK"
[[ -f SECOND_BRAIN_CANON.md ]] && echo "Canon: OK"
[[ -f docs/PACK3_TOC.md ]] && echo "PACK3 TOC: OK"
[[ -x runtime/bin/brain ]] && echo "Runtime CLI: OK"
[[ -f brain/search/brain-index.json ]] && echo "Search index: OK"
[[ -f brain/reports/brain-report.md ]] && echo "Brain report: OK"
echo "Runtime docs: $(find runtime/docs -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Skills: $(find skills -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "Examples: $(find examples -type f 2>/dev/null | wc -l | tr -d ' ')"
