#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/vercel-operator refresh >/tmp/vercel-operator-smoke-refresh.log
runtime/bin/vercel-operator check >/tmp/vercel-operator-smoke-check.log
runtime/bin/vercel-operator preview-command >/tmp/vercel-operator-smoke-preview.log
runtime/bin/vercel-operator deploy-command >/tmp/vercel-operator-smoke-deploy.log
runtime/bin/vercel-operator bundle >/tmp/vercel-operator-smoke-bundle.log
test -f brain/vercel-operator/reports/vercel-operator-readiness.json
test -f brain/vercel-operator/exports/vercel-operator-readiness.zip
echo "vercel-operator smoke passed"
