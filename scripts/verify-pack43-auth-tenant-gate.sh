#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -x runtime/bin/protected-app-shell
python3 -m py_compile runtime/lib/protected_app_shell.py

test -f docs/auth/AUTH_PROVIDER_INTERFACE.md
test -f docs/app-shell/PROTECTED_APP_SHELL_BLUEPRINT.md
test -f docs/tenant/TENANT_SESSION_BOUNDARY.md
test -f docs/tenant/ROLE_MATRIX.md
test -f docs/app-shell/PROTECTED_ROUTE_MAP.md
test -f docs/auth/SIGNUP_INVITATION_POLICY.md
test -f docs/tenant/TENANT_SWITCHER_SPEC.md
test -f docs/operator/OPERATOR_ADMIN_SPLIT.md
test -f docs/app-shell/CLIENT_WORKSPACE_VIEW_SPEC.md
test -f docs/auth/AUTH_RLS_INTEGRATION_NOTES.md
test -f docs/auth/SESSION_AUDIT_EVENT_SPEC.md

scripts/protected-app-smoke.sh >/tmp/protected-app-smoke.log

grep -q "No tenant_id means no private app data access" docs/tenant/TENANT_SESSION_BOUNDARY.md
grep -q "service-role operations are never user-role operations" docs/tenant/ROLE_MATRIX.md
grep -q "RLS" docs/auth/AUTH_RLS_INTEGRATION_NOTES.md
grep -q "real_client_data_allowed" brain/auth/reports/auth-tenant-gate.json

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real service role key found."
  exit 1
fi

echo "pack43 auth tenant gate verify passed"
