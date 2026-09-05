# 🅰️ AOC — AndyAI Obsidian Cockpit

**Version:** 0.1.0  
**Status:** RECON + CONTRACT PROOF  
**Initial home:** `kolundzic/andyai-second-brain` (module until a dedicated repo is justified)

## Canon

> **OBSIDIAN DISPLAYS AND PROPOSES. ANDYAI GOVERNS AND EXECUTES.**

AOC is the human cockpit for AndyAI. Obsidian may show context, capture notes and surface proposals, but it is not the authoritative memory store, authority layer or execution engine.

## System boundary

```text
ANDY
  |
  v
OBSIDIAN COCKPIT
  | read / display / propose
  v
ANDYAI BRIDGE
  +--> ALOG — continuous trace
  +--> GOM — governed memory
  +--> project repos / capsules
  |
  v
AAA — approval / STOP / authority
  |
  v
AGEG — governed execution
  |
  v
ALM / APOA / adapters
  |
  v
RECEIPT
```

## Proofs

- `canon/AOC-RECON-01A.md` — Obsidian capability + security reconnaissance.
- `canon/AOC-KORMILO-PROOF-01B.md` — KORMILO cockpit contract.
- `contracts/aoc-kormilo-contract-v0.1.json` — machine-readable contract.
- `scripts/validate_kormilo.py` — deterministic validator.
- `fixtures/kormilo-pass.json` — positive proof fixture.
- `fixtures/kormilo-fail-authority.json` — adversarial fixture proving execution authority is rejected.

## Run

```bash
python3 scripts/validate_kormilo.py fixtures/kormilo-pass.json
python3 scripts/validate_kormilo.py fixtures/kormilo-fail-authority.json
```

Expected result: first fixture PASS, second fixture FAIL.

## Next proof

`AOC–OBSIDIAN–READONLY–ADAPTER–01C` — connect the contract to the official Obsidian CLI using only read/search/list operations before any governed write path is considered.
