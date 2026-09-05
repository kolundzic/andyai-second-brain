# 🅰️ AOC–OBSIDIAN–READONLY–ADAPTER–01C

**Date:** 2026-09-06  
**Status:** EXECUTABLE PROOF — PASS

## Goal

Prove that AOC can call the official Obsidian CLI for useful cockpit reads while structurally denying write, delete, arbitrary command, plugin-control and developer/eval surfaces.

## Canon

> **READ FIRST. PROPOSE SECOND. GOVERN WRITE SEPARATELY.**

The adapter is not a generic shell wrapper. It accepts a small typed request and constructs a fixed argv list using `shell=False`.

## Official CLI basis

Obsidian's official CLI supports both safe read/list operations and powerful mutation/developer operations. 01C therefore uses an explicit allow-list rather than trying to blacklist shell strings after the fact.

Approved command families in 01C:

- `vault`
- `files`, `folders`, `file`, `read`
- `search`, `search:context`
- `backlinks`, `links`, `outline`
- `properties`, `property:read`
- `tags`, `tag`
- `tasks`

Explicitly denied examples:

- file writes: `create`, `append`, `prepend`, `move`, `rename`, `delete`
- task mutation: `task`
- property mutation: `property:set`, `property:remove`
- arbitrary command surfaces: `command`, `eval`
- plugin mutation: `plugin:enable`, `plugin:install`, `plugin:reload`, etc.
- developer control: `dev:*`, `devtools`
- restore/publish/sync mutation paths

## Additional boundary checks

- no raw shell string is accepted
- executable is fixed to `obsidian`; callers cannot substitute another binary
- subprocess runs with `shell=False`
- absolute paths are rejected
- `..` traversal is rejected
- control characters are rejected
- only per-command approved parameters are accepted
- command timeout is fixed by contract
- output remains a proposal/read surface; human authority is unchanged

## Proof

Run:

```bash
python3 -m unittest -v tests/test_obsidian_readonly_adapter.py
```

Expected: all tests PASS.

Also inspect a dry-run without requiring Obsidian to be installed:

```bash
python3 scripts/obsidian_readonly_adapter.py read \
  --vault AndyAI \
  --params '{"path":"Projects/AOC.md"}' \
  --dry-run
```

Expected argv:

```json
["obsidian", "vault=AndyAI", "read", "path=Projects/AOC.md"]
```

Adversarial example:

```bash
python3 scripts/obsidian_readonly_adapter.py delete \
  --params '{"path":"Canon.md"}' \
  --dry-run
```

Expected: `BLOCKED`.

## What 01C proves — and does not prove

It proves the **adapter contract and enforcement logic** are executable and reject known mutation surfaces.

It does not yet prove a live Mac/HP vault connection because this execution environment does not contain Andy's running Obsidian desktop and vault. The next live-fire step should run this exact adapter against the real vault with read-only commands first.

## Next

`AOC–KORMILO–LIVE–VAULT–01D`

Use 01C to read a bounded set of vault notes and assemble the existing `AOC_KORMILO_CONTRACT_01B` payload. No write path is introduced.
