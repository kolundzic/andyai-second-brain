#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/privacy-firewall public-gate >/tmp/andyai-precommit-privacy-gate.log
echo "privacy pre-commit guard passed"
