#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RUNTIME_DIR="$ROOT_DIR/runtime"
BRAIN_DIR="$ROOT_DIR/brain"
now_utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
slugify(){ echo "$1" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-|-$//g'; }
ensure_runtime_dirs(){ mkdir -p "$RUNTIME_DIR/reports" "$RUNTIME_DIR/index" "$RUNTIME_DIR/logs" "$BRAIN_DIR/evidence" "$BRAIN_DIR/decisions" "$BRAIN_DIR/reports" "$BRAIN_DIR/projects"; }
