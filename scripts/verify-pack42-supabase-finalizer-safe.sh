#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f supabase/migrations/001_tenant_memory_foundation.sql
test -f supabase/policies/rls_policy_drafts.sql
test -f docs/supabase/SUPABASE_PROTECTED_DATA_FOUNDATION_STATUS.md
test -f docs/pack42/PACK42_FINALIZER_SAFE_REPAIR.md

grep -q "enable row level security" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "memory_items" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "documents" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "uploads" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "approval_events" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "Real confidential client data is still blocked" docs/supabase/SUPABASE_PROTECTED_DATA_FOUNDATION_STATUS.md

# Do not allow real-looking service role values in public/docs.
if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real Supabase service role key found."
  exit 1
fi

echo "pack42 supabase finalizer-safe verify passed"
