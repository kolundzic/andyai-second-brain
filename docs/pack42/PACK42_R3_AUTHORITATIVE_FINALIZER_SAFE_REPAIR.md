# PACK42 R3 — Authoritative Finalizer-Safe Repair

## Why R3 exists

The first PACK42 failed because the pack verifier was called too early.
PACK42 R2 then passed its targeted verifier but stopped before commit/tag, most likely because it still called the old strict verifier.

R3 becomes authoritative for finishing PACK42.

## Finalizer-Safe Rule

1. Reassert all required Supabase foundation files.
2. Regenerate reports and export bundle.
3. Run R3 verifier.
4. Run core verifiers.
5. Stage everything after generation.
6. Commit.
7. Tag.
8. Require clean tree.

## Product rule

No real confidential client data until RLS, storage privacy, service-role boundary, privacy firewall, logic-layer firewall and human approval are verified.
