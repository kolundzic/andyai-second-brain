#!/usr/bin/env bash
set -euo pipefail

[[ -f "ANDYAI_CONTEXT.md" ]] || { echo "Missing ANDYAI_CONTEXT.md"; exit 1; }
[[ -f "SECOND_BRAIN_CANON.md" ]] || { echo "Missing SECOND_BRAIN_CANON.md"; exit 1; }
[[ -f "docs/PACK4_QUERY_RETRIEVAL_CONTEXT_ASSEMBLY_TOC.md" ]] || { echo "Missing PACK4 TOC"; exit 1; }
[[ -x "runtime/bin/brain-query" ]] || { echo "Missing executable runtime/bin/brain-query"; exit 1; }
[[ -f "runtime/lib/brain_query_runtime.py" ]] || { echo "Missing brain query runtime"; exit 1; }
[[ -f "schemas/query-request.schema.json" ]] || { echo "Missing query request schema"; exit 1; }
[[ -f "schemas/retrieval-result.schema.json" ]] || { echo "Missing retrieval result schema"; exit 1; }
[[ -f "schemas/context-bundle.schema.json" ]] || { echo "Missing context bundle schema"; exit 1; }
[[ -f "skills/query-brain.md" ]] || { echo "Missing query-brain skill"; exit 1; }
[[ -f "skills/assemble-context.md" ]] || { echo "Missing assemble-context skill"; exit 1; }
[[ -f "skills/answer-with-evidence.md" ]] || { echo "Missing answer-with-evidence skill"; exit 1; }

python3 -m py_compile runtime/lib/brain_query_runtime.py

echo "✅ AndyAI Second Brain PACK4 verification passed."
