#!/usr/bin/env bash
set -euo pipefail
[[ -f README.md ]]
[[ -f ANDYAI_CONTEXT.md ]]
[[ -f SECOND_BRAIN_CANON.md ]]
[[ -f docs/PACK7_TRUST_LEDGER_TOC.md ]]
[[ -x runtime/bin/brain-trust ]]
[[ -d brain/trust-ledger ]]
[[ -d brain/audit-events ]]
[[ -d brain/decision-accountability ]]
[[ -d brain/approval-audit ]]
[[ -d brain/execution-audit ]]
[[ -d brain/evidence-ledger ]]
[[ -d brain/integrity ]]
[[ -f schemas/audit-event.schema.json ]]
[[ -f schemas/decision-accountability.schema.json ]]
[[ -f schemas/trust-ledger-record.schema.json ]]
python3 -m json.tool schemas/audit-event.schema.json >/dev/null
python3 -m json.tool schemas/decision-accountability.schema.json >/dev/null
python3 -m json.tool schemas/trust-ledger-record.schema.json >/dev/null
bash -n scripts/brain-check.sh
python3 -m py_compile runtime/bin/brain-trust
