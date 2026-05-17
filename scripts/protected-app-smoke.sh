#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/protected-app-shell build >/tmp/protected-app-build.log
runtime/bin/protected-app-shell bundle >/tmp/protected-app-bundle.log
test -f public/login/index.html
test -f public/app/index.html
test -f public/access-denied/index.html
test -f brain/auth/reports/auth-tenant-gate.json
test -f brain/auth/exports/auth-tenant-gate-pack.zip
grep -q "Login to your protected Second Brain" public/login/index.html
grep -q "private Second Brain workspace" public/app/index.html
grep -q "Access denied" public/access-denied/index.html
echo "protected app smoke passed"
