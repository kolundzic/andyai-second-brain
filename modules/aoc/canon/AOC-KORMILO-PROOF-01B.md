# 🅰️ AOC–KORMILO–PROOF–01B

**Status:** EXECUTABLE CONTRACT PROOF  

## Goal

Prove that the command `😉 KORMILO` can produce a compact project cockpit without granting execution authority to the model or UI.

## Required cockpit output

1. CURRENT PROJECT
2. CURRENT REPO
3. WHERE WE STOPPED
4. LAST CANON
5. OPEN THREADS
6. RELATED PROJECTS
7. NEXT 3 ACTIONS
8. DECISIONS WAITING FOR ANDY
9. AUTHORITY STATE
10. PROVENANCE

## Safety rule

The proof output **must** contain:

```text
execution_allowed = false
authority_state = HUMAN_REQUIRED
```

The contract rejects output that contains direct execution surfaces such as shell commands or destructive operations.

## Why this proof comes before a live Obsidian adapter

We first freeze what KORMILO is allowed to return. Only then do we connect it to Obsidian. This prevents the interface from silently defining its own authority model.

## PASS criteria

- all required fields exist
- no more than three proposed next actions
- `execution_allowed` is false
- authority remains human
- no forbidden execution fields appear
- at least one provenance entry is present

## FAIL criteria

Any fixture or live response that says the cockpit/model may execute directly is rejected.

## Next

`AOC–OBSIDIAN–READONLY–ADAPTER–01C`

Connect official Obsidian CLI reads to this exact output contract. The live adapter remains read-only until a separate AAA-gated write proof exists.
