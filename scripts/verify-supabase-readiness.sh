#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -f docs/supabase/SUPABASE_TENANT_SCHEMA_DRAFT.sql
test -f docs/supabase/SUPABASE_RLS_POLICY_DRAFT.sql
test -f docs/supabase/SUPABASE_OPERATOR_CHECKLIST.md
echo "supabase readiness verify passed"
