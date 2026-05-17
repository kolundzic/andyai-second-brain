#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f docs/supabase/SUPABASE_CONNECTION_GUIDE.md
test -f docs/supabase/ENVIRONMENT_VARIABLE_MAP.md
test -f docs/supabase/SUPABASE_PROTECTED_DATA_FOUNDATION_STATUS.md
test -f docs/security/SUPABASE_SERVICE_ROLE_BOUNDARY.md
test -f docs/security/SUPABASE_ANON_KEY_SAFETY.md
test -f supabase/migrations/001_tenant_memory_foundation.sql
test -f supabase/policies/rls_policy_drafts.sql
test -f supabase/storage/storage_bucket_policy.md
test -f docs/pack42/PACK42_R3_AUTHORITATIVE_FINALIZER_SAFE_REPAIR.md

grep -q "enable row level security" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "public.tenants" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "public.profiles" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "memory_items" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "documents" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "uploads" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "processing_jobs" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "audit_logs" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "approval_events" supabase/migrations/001_tenant_memory_foundation.sql
grep -q "tenant_id in" supabase/policies/rls_policy_drafts.sql
grep -q "private-uploads" supabase/storage/storage_bucket_policy.md
grep -q "Real confidential client data is still blocked" docs/supabase/SUPABASE_PROTECTED_DATA_FOUNDATION_STATUS.md

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real Supabase service role key found."
  exit 1
fi

echo "pack42 supabase authoritative verify passed"
