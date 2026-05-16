# Query / Retrieval / Context Assembly Architecture

PACK4 adds a practical retrieval path:

```text
Question
  ↓
Query Request
  ↓
Search Index
  ↓
Retrieval Scoring
  ↓
Evidence-Aware Results
  ↓
Context Bundle
  ↓
Agent Handoff
  ↓
Action / Answer / Next TAP
```

## Core Rule

The agent should not read the whole brain. It should read the smallest useful context bundle that is sufficient for the next action.

## Progressive Disclosure

1. Read root context.
2. Search relevant project/resource/evidence files.
3. Assemble a compact bundle.
4. Include evidence and decision links.
5. Warn when sources are stale or missing.
6. Ask human approval before high-impact action.
