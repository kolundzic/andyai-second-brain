# Public Nav Finalizer-Safe Repair

## Problem

A visible `\n` appeared in the public navigation between `Health` and `Help`.

A first cleanup attempt can still end red if post-verify generated reports or source patching leave the tree dirty after tag/commit.

## v82.0.3 Fix

This repair follows a stricter finalizer-safe pattern:

1. Accept possible dirty leftovers from v82.0.2.
2. Clean rendered public HTML and generator sources.
3. Write a repair report.
4. Run the repair verifier.
5. Run core verification.
6. Stage all final artifacts after verification.
7. Commit once.
8. Tag only after final capture.
9. Require clean working tree.

## Rule

The final tag must be created after the final generated reports are captured, not before.
