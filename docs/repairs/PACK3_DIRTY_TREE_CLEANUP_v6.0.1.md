# PACK3 Dirty Tree Cleanup Repair — v6.0.1

## Purpose

PACK3 reached `v6.0.0 — Real Brain Operations Lock`, but the final clean-tree check reported a dirty working tree after the lock commit/tag sequence.

This repair does **not** move or rewrite `v6.0.0`.
It captures any remaining PACK3-generated files and records a clean hygiene repair as `v6.0.1`.

## Repair Policy

- Preserve successful tags `v4.1.0 → v6.0.0`.
- Do not force-move tags.
- Do not rewrite history.
- Add/commit remaining generated files safely.
- Run available verification scripts.
- Create `v6.0.1` as the dirty-tree cleanup repair tag.

## TAP-TAP Lesson

A master pack can reach its feature lock while still leaving generated artifacts unstaged or modified. The final phase must always include a clean-tree check and a dedicated repair path that avoids rerunning successful versions.
