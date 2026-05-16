#!/usr/bin/env bash
set -euo pipefail
printf "🧠 AndyAI Second Brain PACK5 check\n"
[ -f ANDYAI_CONTEXT.md ] && printf "Root context: OK\n" || exit 1
[ -f SECOND_BRAIN_CANON.md ] && printf "Canon: OK\n" || exit 1
[ -f docs/packs/PACK5_AGENT_HANDOFF_TOC.md ] && printf "PACK5 TOC: OK\n" || exit 1
[ -x runtime/bin/brain-mission ] && printf "Mission CLI: OK\n" || exit 1
[ -f schemas/mission-request.schema.json ] && printf "Mission schema: OK\n" || exit 1
[ -f schemas/agent-handoff.schema.json ] && printf "Handoff schema: OK\n" || exit 1
printf "Skills: %s\n" "$(find skills -type f | wc -l | tr -d ' ')"
printf "Schemas: %s\n" "$(find schemas -type f | wc -l | tr -d ' ')"
printf "Docs: %s\n" "$(find docs -type f | wc -l | tr -d ' ')"
printf "Examples: %s\n" "$(find examples -type f | wc -l | tr -d ' ')"
