#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -x runtime/bin/memory-index
python3 -m py_compile runtime/lib/memory_index.py

test -f docs/pack45/PACK45_TOC.md
test -f docs/memory/MEMORY_INDEX_SCAFFOLD.md
test -f docs/memory/MEMORY_RECORD_CONTRACT.md
test -f docs/search/SEARCH_QUERY_MODEL.md
test -f docs/timeline/TIMELINE_EVENT_MODEL.md
test -f docs/memory/PROJECT_CLIENT_TOPIC_TAG_MODEL.md
test -f docs/evidence/EVIDENCE_LINK_MODEL.md
test -f docs/memory/MEMORY_CLASSIFICATION_POLICY.md
test -f docs/search/SEARCH_RESULT_RANKING_DRAFT.md
test -f docs/search/SAFE_RECALL_BOUNDARY.md
test -f docs/search/COMPARE_DOCUMENTS_SPEC.md
test -f docs/search/SORT_FILTER_DATE_RANGE_SPEC.md
test -f schemas/memory/memory-record.schema.json

scripts/memory-index-smoke.sh >/tmp/memory-index-smoke.log

grep -q "search must never cross tenant boundaries" docs/search/SEARCH_QUERY_MODEL.md
grep -q "permission match comes before relevance" docs/search/SEARCH_RESULT_RANKING_DRAFT.md
grep -q "Safe recall" public/memory/index.html
grep -q "real_confidential_memory_allowed" brain/memory/reports/memory-index.json
grep -q '"recall_allowed": false' brain/memory/reports/memory-index.json

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real service role key found."
  exit 1
fi

echo "pack45 memory index verify passed"
