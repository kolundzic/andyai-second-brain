#!/usr/bin/env bash
set -euo pipefail

required=(
  "README.md"
  "ANDYAI_CONTEXT.md"
  "SECOND_BRAIN_CANON.md"
  "docs/ARCHITECTURE.md"
  "docs/PRACTICAL_USE_CASES.md"
  "docs/GOVERNANCE_MODEL.md"
  "docs/MEMORY_POLICY.md"
  "docs/SKILLS_STANDARD.md"
  "docs/ROADMAP.md"
  "brain/projects/.gitkeep"
  "brain/areas/.gitkeep"
  "brain/resources/.gitkeep"
  "brain/archives/.gitkeep"
  "brain/evidence/.gitkeep"
  "brain/decisions/.gitkeep"
  "brain/skills/.gitkeep"
  "brain/reports/.gitkeep"
  "skills/start-project.md"
  "skills/canonize-signal.md"
  "skills/repo-status.md"
  "skills/meeting-debrief.md"
  "skills/taptap-pack-summary.md"
  "skills/client-brief.md"
  "schemas/project-context.schema.json"
  "schemas/memory-entry.schema.json"
  "schemas/evidence-link.schema.json"
  "schemas/skill.schema.json"
  "schemas/decision.schema.json"
  "examples/sample-project-context.md"
  "examples/sample-memory-entry.md"
  "examples/sample-decision-log.md"
  "examples/sample-evidence-report.md"
)

missing=0
for f in "${required[@]}"; do
  if [ ! -f "$f" ]; then
    echo "❌ Missing: $f"
    missing=1
  fi
done

if [ "$missing" -ne 0 ]; then
  echo "❌ Verification failed."
  exit 1
fi

echo "✅ AndyAI Second Brain v0.1.0 verification passed."
