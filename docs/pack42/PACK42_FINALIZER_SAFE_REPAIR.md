# PACK42 R2 — Finalizer-Safe Repair

## Why this repair exists

PACK42 can complete its main Supabase foundation but still end red if generated reports or ZIP exports change after a tag/commit step.

This repair applies the Finalizer-Safe Rule:

1. verify files exist
2. regenerate final reports/exports
3. run targeted verifier
4. run core verifiers
5. stage everything after all generation
6. commit once
7. tag after final capture
8. require clean tree

## Canon

Static site shows the idea.  
Supabase protects reality.  
RLS protects boundaries.  
Human approval protects responsibility.
