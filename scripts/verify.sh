#!/usr/bin/env bash
set -euo pipefail

required_files=(
  README.md
  ANDYAI_CONTEXT.md
  SECOND_BRAIN_CANON.md
  docs/MASTER_TOC.md
  docs/PARA_WORKSPACE.md
  docs/PROJECT_CONTEXT_STANDARD.md
  docs/EVIDENCE_BACKED_MEMORY.md
  docs/HUMAN_APPROVAL_GATE.md
  docs/REPO_MEMORY_BRIDGE.md
  docs/CLIENT_MEMORY_BRIDGE.md
  docs/CONTEXT_ROUTER_SPEC.md
  skills/context-router.md
  skills/evidence-memory-update.md
  schemas/repo-memory.schema.json
  schemas/client-memory.schema.json
  examples/sample-repo-memory.md
)

for file in "${required_files[@]}"; do
  if [ ! -s "$file" ]; then
    echo "❌ Missing or empty required file: $file"
    exit 1
  fi
done

if ! grep -q "RAG pronalazi fragmente" README.md; then
  echo "❌ Canon formula missing from README.md"
  exit 1
fi

if ! grep -q "Human approval" docs/HUMAN_APPROVAL_GATE.md; then
  echo "❌ Human approval gate missing expected phrase"
  exit 1
fi

echo "✅ AndyAI Second Brain verification passed."
