#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/brain-doctor validate-json examples/doctor-valid/sample-valid.json >/tmp/brain-doctor-smoke-valid.log
if runtime/bin/brain-doctor validate-json examples/doctor-invalid/sample-invalid.json >/tmp/brain-doctor-smoke-invalid.log 2>&1; then
  echo "invalid json unexpectedly passed"
  exit 1
fi
runtime/bin/brain-doctor scan-schemas >/tmp/brain-doctor-smoke-schemas.log
runtime/bin/brain-doctor scan-reports >/tmp/brain-doctor-smoke-reports.log
runtime/bin/brain-doctor scan-evidence >/tmp/brain-doctor-smoke-evidence.log
runtime/bin/brain-doctor tag-snapshot >/tmp/brain-doctor-smoke-tags.log
runtime/bin/brain-doctor generate-report >/tmp/brain-doctor-smoke-report.log
runtime/bin/brain-doctor export-evidence >/tmp/brain-doctor-smoke-export.log
test -f brain/doctor/reports/brain-doctor-report.md
test -f brain/doctor/reports/brain-doctor-report.json
test -f brain/doctor/exports/brain-doctor-evidence.zip
echo "brain-doctor smoke passed"
