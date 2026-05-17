#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/privacy-firewall scan public >/tmp/privacy-firewall-smoke-public.log
runtime/bin/privacy-firewall public-gate >/tmp/privacy-firewall-smoke-gate.log || true
runtime/bin/privacy-firewall classify examples/privacy-safe/sample-safe-client-data.json >/tmp/privacy-firewall-smoke-classify-safe.log
runtime/bin/privacy-firewall classify examples/privacy-unsafe/sample-unsafe-client-data.txt >/tmp/privacy-firewall-smoke-classify-unsafe.log
runtime/bin/privacy-firewall redact examples/privacy-unsafe/sample-unsafe-client-data.txt --out brain/privacy/redacted/smoke-redacted.txt >/tmp/privacy-firewall-smoke-redact.log
runtime/bin/privacy-firewall quarantine examples/privacy-unsafe/sample-unsafe-client-data.txt >/tmp/privacy-firewall-smoke-quarantine.log
runtime/bin/privacy-firewall audit >/tmp/privacy-firewall-smoke-audit.log
runtime/bin/privacy-firewall safe-export >/tmp/privacy-firewall-smoke-export.log
test -f brain/privacy/audit/privacy-audit.json
test -f brain/privacy/reports/privacy-audit.md
test -f brain/privacy/redacted/smoke-redacted.txt
test -f brain/privacy/exports/public-safe-privacy-export.zip
python3 - <<'PY'
import json
json.load(open("brain/privacy/audit/privacy-audit.json"))
PY
echo "privacy-firewall smoke passed"
