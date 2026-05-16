# TAP-TAP Timing Precision Standard

Timing is operational intelligence, not decoration.

PACK8 proved that second-level timing can technically exist but still be weak when packs complete very quickly. PACK9 upgrades the standard:

- Use millisecond precision.
- Record per-version duration.
- Record total duration.
- Record slowest and fastest phase.
- Estimate next pack duration.
- Keep timing explicit and boring under `set -u`.
- Avoid clever one-liners.
- Preserve timing evidence for Bridge Hub and Second Brain.

Canonical line:

> Timing must be useful, not merely present.
