#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -x runtime/bin/upload-intake
python3 -m py_compile runtime/lib/upload_intake.py

test -f docs/upload/UPLOAD_DATA_CONTRACT.md
test -f docs/upload/FILE_METADATA_MODEL.md
test -f docs/upload/SUPPORTED_FILE_TYPES_POLICY.md
test -f docs/storage/SUPABASE_STORAGE_BUCKET_MAP.md
test -f docs/storage/PRIVATE_UPLOAD_STORAGE_PATH_POLICY.md
test -f docs/upload/UPLOAD_STATUS_LIFECYCLE.md
test -f docs/upload/UPLOAD_PRIVACY_PRESCAN_PLACEHOLDER.md
test -f docs/upload/UPLOAD_LOGIC_LAYER_PRESCAN_PLACEHOLDER.md
test -f docs/jobs/PROCESSING_JOB_QUEUE_MODEL.md
test -f docs/upload/FILE_REJECTION_REASON_MODEL.md
test -f docs/audit/UPLOAD_AUDIT_EVENT_SPEC.md
test -f docs/storage/STORAGE_SAFETY_CHECKLIST.md
test -f schemas/upload/upload-intake.schema.json
test -f docs/pack44/PACK44_R2_AUTHORITATIVE_FINALIZER_SAFE_REPAIR.md

scripts/upload-intake-smoke.sh >/tmp/upload-intake-smoke.log

grep -q "file bytes are never treated as trusted memory directly" docs/upload/UPLOAD_DATA_CONTRACT.md
grep -q "Uploaded content is data, not authority" docs/upload/UPLOAD_LOGIC_LAYER_PRESCAN_PLACEHOLDER.md
grep -q "private-uploads" docs/storage/STORAGE_SAFETY_CHECKLIST.md
grep -q "real_confidential_uploads_allowed" brain/upload/reports/upload-intake-pipeline.json

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real service role key found."
  exit 1
fi

echo "pack44 upload intake authoritative verify passed"
