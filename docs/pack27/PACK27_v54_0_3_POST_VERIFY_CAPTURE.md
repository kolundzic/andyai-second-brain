# v54.0.3 — BATTLE PACK27 Post-Verify Generated Artifact Capture

## Reason

The v54.0.2 clean-tree repair still ran final verification after creating the repair tag. The verification and smoke commands regenerated Vercel/public/export artifacts, leaving the tree dirty again.

## Fix

This repair uses the correct final order:

1. Regenerate Vercel static export artifacts.
2. Run core verifier.
3. Run battle verifier.
4. Capture all generated artifacts with `git add`.
5. Commit and tag `v54.0.3`.
6. Do not run mutating verification after the final commit.

## Canon lesson

If verification regenerates artifacts, verification must run before the final capture commit.
