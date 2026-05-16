# Staleness Warning Policy

A retrieved file should be flagged as possibly stale when:

- It belongs to archives.
- It is older than the current locked milestone.
- It conflicts with a newer decision or evidence file.
- It has no date, no source or no confidence field.

PACK4 does not delete stale sources. It warns the user and preserves traceability.
