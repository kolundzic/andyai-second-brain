#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TMP_SAFE="/tmp/andyai_git_remote_allowlist_safe.txt"
TMP_UNSAFE="/tmp/andyai_real_email_detection_unsafe.txt"

cat > "$TMP_SAFE" <<'TXT'
Git remote: git@github.com:kolundzic/andyai-second-brain.git
TXT

cat > "$TMP_UNSAFE" <<'TXT'
Contact: private.person@example.com
TXT

SAFE_RESULT="$(runtime/bin/privacy-firewall scan "$TMP_SAFE")"
UNSAFE_RESULT="$(runtime/bin/privacy-firewall scan "$TMP_UNSAFE")"

python3 - "$SAFE_RESULT" "$UNSAFE_RESULT" <<'PY'
import json, sys
safe = json.loads(sys.argv[1])
unsafe = json.loads(sys.argv[2])
if safe.get("findings_count") != 0:
    raise SystemExit(f"safe git remote false positive still detected: {safe}")
if unsafe.get("findings_count", 0) < 1:
    raise SystemExit(f"real email was not detected: {unsafe}")
print("privacy allowlist regression passed")
PY
