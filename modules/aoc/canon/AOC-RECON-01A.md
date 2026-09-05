# 🅰️ AOC–RECON–01A — Obsidian Cockpit Reconnaissance

**Date:** 2026-09-05  
**Status:** LOCKED FOR PROOF  

## Question

Can Obsidian become the daily human cockpit for AndyAI without becoming AndyAI's memory authority or execution authority?

## Finding

**YES — with a strict boundary.**

Obsidian is a strong candidate for the human-facing surface because it is local-file based, extensible through plugins, and now exposes an official CLI for scripting and automation. The official CLI can search, read and create notes and can inspect tasks, tags, links and plugin state.

However, Obsidian community plugins are not a trustworthy authority boundary. Obsidian's own security documentation states that community plugins inherit the application's access and cannot be reliably constrained to narrow permissions. For AndyAI this means plugin convenience must never substitute for AAA governance.

## Canonical architecture decision

> **OBSIDIAN DISPLAYS AND PROPOSES. ANDYAI GOVERNS AND EXECUTES.**

### Obsidian may

- display project state
- display ALOG/GOM-derived context
- search and open human-readable notes
- capture daily notes
- surface open decisions
- prepare proposals
- visualize focus / attention
- show planner information

### Obsidian must not independently

- become the canonical memory authority
- decide permissions
- bypass AAA approval
- give a model raw shell authority
- delete or move important files without governed execution
- become the only copy of canonical system state

## Recommended first integration

**Read-first.**

Use the official Obsidian CLI only for deterministic reads during the first live adapter proof:

- search vault
- read known notes
- list relevant metadata
- open a selected note in the UI

No direct model-controlled shell execution. No delete. No arbitrary write. No plugin permission model is treated as security.

## Sync note

Obsidian Sync can use end-to-end encryption for the remote vault, but the local vault itself is not encrypted by Obsidian. AOC therefore treats local disk protection, OS account security and backup as separate responsibilities.

## External evidence

- Official developer docs: https://docs.obsidian.md/
- Official CLI: https://obsidian.md/help/cli
- Official plugin security: https://obsidian.md/help/plugin-security
- Official Sync security: https://obsidian.md/help/Obsidian%20Sync/Security%20and%20privacy
- Community REST/MCP example (recon only, not trusted authority): https://community.obsidian.md/plugins/cli-rest-mcp

## AndyAI links

- **ALOG** — source of continuous trace, not replaced by Obsidian.
- **GOM** — governed memory, not replaced by Obsidian.
- **AAA** — owns authority, approval and STOP.
- **AGEG** — owns governed execution graph.
- **ALM/APOA** — execution bodies/runtimes.
- **Attention Engine** — natural owner of focus/attention visualization logic.
- **ASR** — can later provide proof snapshots / provenance checks.

## Verdict

**AOC = ADOPT AS COCKPIT EXPERIMENT.**  
**DO NOT ADOPT OBSIDIAN AS AUTHORITY PLANE.**
