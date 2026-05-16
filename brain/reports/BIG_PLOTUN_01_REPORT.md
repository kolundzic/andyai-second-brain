# BIG PLOTUN 01 Report

## Range

v22.1.0 → v28.0.0

## Packs

- PACK12 — Operator Execution Evidence / Service Doctor Runtime Layer
- PACK13 — Bridge Hub Control Panel / Live Status / Operator Dashboard Layer
- PACK14 — Second Brain Feedback Loop / Learning Memory / Pattern Reuse Layer

## Repair lesson

The original BIG PLOTUN 01 script failed at v22.1.0 because macOS Bash 3.2 does not support lowercase parameter expansion such as ${pack,,}. This repair uses portable tr-based lowercase conversion.

## Canon

TAP-TAP v2 no longer only ships packs. It builds a factory that sees, measures, remembers and learns from its own production.
