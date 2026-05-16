#!/usr/bin/env bash
set -euo pipefail

echo "🧠 AndyAI Second Brain check"
echo "Root context: $(test -f ANDYAI_CONTEXT.md && echo OK || echo MISSING)"
echo "Canon: $(test -f SECOND_BRAIN_CANON.md && echo OK || echo MISSING)"
echo "Skills: $(find skills -type f -name '*.md' | wc -l | tr -d ' ')"
echo "Schemas: $(find schemas -type f -name '*.json' | wc -l | tr -d ' ')"
echo "Docs: $(find docs -type f -name '*.md' | wc -l | tr -d ' ')"
