# 🅰️ AOC — AndyAI Obsidian Cockpit

**Version:** 0.2.0  
**Status:** RECON + KORMILO CONTRACT + READ-ONLY ADAPTER PROOF  
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
- `canon/AOC-OBSIDIAN-READONLY-ADAPTER-01C.md` — strict Obsidian CLI read-only adapter proof.
- `contracts/aoc-obsidian-readonly-contract-v0.1.json` — allowed commands/parameters and denied mutation surfaces.
- `scripts/obsidian_readonly_adapter.py` — typed wrapper using `shell=False` and a fixed `obsidian` executable.
- `tests/test_obsidian_readonly_adapter.py` — positive + adversarial enforcement tests.
- `evidence/AOC-OBSIDIAN-READONLY-ADAPTER-01C-PROOF.md` — captured proof result.

## Run

```bash
python3 scripts/validate_kormilo.py fixtures/kormilo-pass.json
python3 scripts/validate_kormilo.py fixtures/kormilo-fail-authority.json
python3 -m unittest -v tests/test_obsidian_readonly_adapter.py
```

Expected: positive KORMILO fixture PASS; adversarial KORMILO fixture FAIL; 01C adapter tests PASS.

## Current proof

`AOC–OBSIDIAN–READONLY–ADAPTER–01C` — PASS. The official Obsidian CLI is wrapped behind an explicit read-only command/parameter contract.

## Next proof

`AOC–KORMILO–LIVE–VAULT–01D` — run the read-only adapter against a real AndyAI vault and assemble the KORMILO contract from bounded sources.
