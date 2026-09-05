# AOC–OBSIDIAN–READONLY–ADAPTER–01C — Proof Evidence

**Date:** 2026-09-06  
**Result:** PASS

## Deterministic tests

Command:

```bash
python3 -m unittest -v tests/test_obsidian_readonly_adapter.py
```

Result:

```text
Ran 11 tests in 0.001s
OK
```

Covered cases:

- approved `read`
- approved `search`
- blocked `delete`
- blocked `create`
- blocked arbitrary `command`
- blocked `eval`
- blocked `../` traversal
- blocked absolute paths
- blocked unknown parameters
- fixed executable (`obsidian` only)
- false boolean flags are not emitted

## Dry-run proof

Input:

```bash
python3 scripts/obsidian_readonly_adapter.py read --vault AndyAI --params '{"path":"Projects/AOC.md"}' --dry-run
```

Output:

```json
["obsidian", "vault=AndyAI", "read", "path=Projects/AOC.md"]
```

Adversarial input using `delete` returned `BLOCKED: command is not read-only or not approved: delete`.

## Boundary

This proof validates the adapter and contract. It is not yet a live-vault proof because the test environment does not contain Andy's running Obsidian desktop/vault.
