#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/upload-intake build >/tmp/upload-intake-build.log
runtime/bin/upload-intake bundle >/tmp/upload-intake-bundle.log
test -f public/upload/index.html
test -f brain/upload/reports/upload-intake-pipeline.json
test -f brain/upload/exports/upload-intake-pipeline-pack.zip
grep -q "real_confidential_uploads_allowed" brain/upload/reports/upload-intake-pipeline.json
grep -q "Upload enters through a protected corridor" public/upload/index.html
grep -q "private-uploads" docs/storage/SUPABASE_STORAGE_BUCKET_MAP.md
echo "upload intake smoke passed"
