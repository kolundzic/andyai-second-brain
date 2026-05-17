#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/launch-operator status >/tmp/launch-operator-status.log
runtime/bin/launch-operator health >/tmp/launch-operator-health.log
runtime/bin/launch-operator robots >/tmp/launch-operator-robots.log
runtime/bin/launch-operator sitemap >/tmp/launch-operator-sitemap.log
runtime/bin/launch-operator trust >/tmp/launch-operator-trust.log
runtime/bin/launch-operator faq >/tmp/launch-operator-faq.log
runtime/bin/launch-operator readiness >/tmp/launch-operator-readiness.log
runtime/bin/launch-operator bundle >/tmp/launch-operator-bundle.log
test -f public/health/index.html
test -f public/status/status.json
test -f public/robots.txt
test -f public/sitemap.xml
test -f public/trust/index.html
test -f public/faq/index.html
test -f brain/launch/exports/public-launch-dossier.zip
echo "launch-operator smoke passed"
