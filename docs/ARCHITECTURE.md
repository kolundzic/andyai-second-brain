# Architecture — AndyAI Second Brain

## System Idea

AndyAI Second Brain is a governed work-memory layer.

It combines:

- context filesystem
- memory schema
- evidence registry
- skill registry
- decision log
- progressive context loading
- repo/project/client bridges
- human approval policy
- export/delete/inspect controls

## Flow

```text
User Signal
   ↓
Signal Classifier
   ↓
Context Router
   ↓
Project / Area / Resource / Archive
   ↓
Evidence Link
   ↓
Skill Execution
   ↓
Human Approval
   ↓
Memory Update
   ↓
Report / Next Action
```

## Progressive Context Loading

The agent starts with `ANDYAI_CONTEXT.md`, then opens only the relevant project, skill, evidence, decision, or report file.

This prevents context dumping and preserves precision.
