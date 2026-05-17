#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f docs/security/LOGIC_LAYER_THREAT_MODEL.md
test -f docs/security/LPCI_DEFENSE_CANON.md
test -f docs/security/MEMORY_INJECTION_RISK_MATRIX.md
test -f docs/security/RAG_CHUNK_TRUST_CLASSIFIER_SPEC.md
test -f docs/security/METADATA_INSTRUCTION_DETECTOR_SPEC.md
test -f docs/security/TOOL_CALL_AUTHORITY_GATE.md
test -f docs/security/CROSS_SESSION_TRIGGER_AUDIT.md
test -f docs/security/PUBLIC_EXPORT_LPCI_GATE.md
test -f docs/security/SECOND_BRAIN_LOGIC_LAYER_DEFENSE_REPORT.md
test -x runtime/bin/logic-layer-firewall
python3 -m py_compile runtime/lib/logic_layer_firewall.py
scripts/logic-layer-firewall-smoke.sh >/tmp/verify-pack38-smoke.log
echo "pack38 logic-layer defense verify passed"
