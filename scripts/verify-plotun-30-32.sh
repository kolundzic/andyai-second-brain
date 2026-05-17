#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Stage-aware verifier:
# PACK30 files must pass immediately.
# PACK31/32 checks only run after their required files exist.

test -x runtime/bin/vercel-operator
python3 -m py_compile runtime/lib/vercel_operator.py
runtime/bin/vercel-operator check >/tmp/verify-plotun-vercel-check.log

if [[ -x runtime/bin/client-portal && -f runtime/lib/client_portal.py ]]; then
  python3 -m py_compile runtime/lib/client_portal.py
fi

if [[ -x scripts/client-portal-smoke.sh && -f public/client-portal/index.html ]]; then
  scripts/client-portal-smoke.sh >/tmp/verify-plotun-client-portal.log
fi

if [[ -x scripts/verify-supabase-readiness.sh \
      && -f docs/supabase/SUPABASE_TENANT_SCHEMA_DRAFT.sql \
      && -f docs/supabase/SUPABASE_RLS_POLICY_DRAFT.sql \
      && -f docs/supabase/SUPABASE_OPERATOR_CHECKLIST.md ]]; then
  scripts/verify-supabase-readiness.sh >/tmp/verify-plotun-supabase.log
else
  echo "supabase readiness check skipped until PACK32 files exist" >/tmp/verify-plotun-supabase.log
fi

echo "plotun 30-32 verify passed"
