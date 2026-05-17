#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

test -f public/upload/index.html
test -f brain/upload/reports/upload-intake-pipeline.json
test -f brain/upload/reports/PACK44_FINAL_STATUS.json
test -f brain/upload/exports/upload-intake-pipeline-pack.zip
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
test -f docs/pack44/PACK44_R3_EMERGENCY_AUTHORITATIVE_CLEANUP.md
test -x runtime/bin/upload-intake
python3 -m py_compile runtime/lib/upload_intake.py

grep -q "Upload enters through a protected corridor" public/upload/index.html
grep -q "file bytes are never treated as trusted memory directly" docs/upload/UPLOAD_DATA_CONTRACT.md
grep -q "Uploaded content is data, not authority" docs/upload/UPLOAD_LOGIC_LAYER_PRESCAN_PLACEHOLDER.md
grep -q "private-uploads" docs/storage/SUPABASE_STORAGE_BUCKET_MAP.md
grep -q "real_confidential_uploads_allowed" brain/upload/reports/upload-intake-pipeline.json

if grep -R "SUPABASE_SERVICE_ROLE_KEY=.*eyJ" public docs README.md 2>/dev/null; then
  echo "Possible real service role key found."
  exit 1
fi

echo "pack44 upload intake R3 verify passed"
