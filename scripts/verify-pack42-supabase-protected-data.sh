#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f docs/pack42/PACK42_TOC.md
test -f docs/supabase/SUPABASE_CONNECTION_GUIDE.md
test -f docs/supabase/ENVIRONMENT_VARIABLE_MAP.md
test -f supabase/migrations/001_tenant_memory_foundation.sql
test -f supabase/policies/rls_policy_drafts.sql
test -f supabase/storage/storage_bucket_policy.md
test -f docs/security/SUPABASE_SERVICE_ROLE_BOUNDARY.md
test -f docs/security/SUPABASE_ANON_KEY_SAFETY.md
test -f docs/supabase/SUPABASE_LOCAL_SETUP_CHECKLIST.md
test -f docs/supabase/SUPABASE_DEPLOYMENT_CHECKLIST.md

grep -q "enable row level security" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "memory_items" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "approval_events" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "service role key must never" docs/security/SUPABASE_SERVICE_ROLE_BOUNDARY.md
grep -q "RLS enabled" docs/supabase/SUPABASE_DEPLOYMENT_CHECKLIST.md

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*[A-Za-z0-9]" public docs README.md 2>/dev/null | grep -v "SUPABASE_SERVICE_ROLE_KEY=" >/dev/null; then
  echo "Possible real service role key found in public/docs."
  exit 1
fi

echo "pack42 supabase protected data verify passed"
