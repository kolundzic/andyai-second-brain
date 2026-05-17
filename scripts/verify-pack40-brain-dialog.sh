#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
test -x runtime/bin/brain-dialog
python3 -m py_compile runtime/lib/brain_dialog.py
scripts/brain-dialog-smoke.sh >/tmp/verify-pack40-brain-dialog-smoke.log
test -f docs/dialog/BRAIN_DIALOG_SPEC.md
test -f docs/upload/DOCUMENT_UPLOAD_PROCESSING_SPEC.md
test -f docs/capture/MOBILE_CAMERA_SCAN_SPEC.md
test -f docs/help/RICH_HELP_README_HTML_SPEC.md
test -f docs/memory/MEMORY_INTAKE_MODEL.md
echo "pack40 brain dialog verify passed"
