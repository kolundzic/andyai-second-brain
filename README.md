# 🅰️ AndyAI Second Brain

A governed AI work-memory layer for people, projects, repositories, decisions, evidence and reusable skills.

## Core Formula

**RAG finds fragments.**  
**Second Brain preserves work continuity.**

Serbian:

**RAG pronalazi fragmente.**  
**Drugi mozak čuva kontinuitet rada.**

## What It Is

AndyAI Second Brain is structured work memory for human-AI collaboration.

It helps answer:

- Where did we stop?
- What is the current project status?
- What proof do we have?
- What decision was made?
- What is the next action?
- What may AI do, and what requires human approval?

## Core Components

- PARA workspace: Projects, Areas, Resources, Archives
- Root context file
- Project context files
- Progressive context router
- Evidence-backed memory
- Decision logs
- Markdown skills
- Human approval gates
- Repo memory bridge
- Client memory bridge
- Meeting memory bridge
- Signal canonizer
- Export/delete/inspect controls

## Practical Use

This repo is the memory spine for AndyAI work: projects, repos, client flows, meetings, signals, book material and verified delivery.

## TAP-TAP Simplification

1. First TAP: unzip the package.
2. Second TAP: run the terminal script.

The terminal output uses a semafor:

- 🟢 passed/safe
- 🟡 warning/non-blocking
- 🔴 blocking failure/STOP

## Human Authority Rule

AI may organize, suggest, draft, inspect and verify. Human approval is required for publishing, deleting canon, changing production, sending client materials or executing high-impact actions.

## PACK2 — Working Brain Runtime Layer

PACK2 adds the first local runtime layer:

```bash
./runtime/bin/brain index
./runtime/bin/brain memory-create "Title" "Body"
./runtime/bin/brain decision-record "Decision" "Reason"
./runtime/bin/brain evidence-link "Claim" "Evidence"
./runtime/bin/brain repo-status
./runtime/bin/brain report
```

Rule: runtime outputs are local-first and need human review before becoming canonical truth.

## 🤜💥 PACK3 — Real Brain Operations Layer

PACK3 adds practical local operations to AndyAI Second Brain: inbox intake, context routing, brain search, project snapshots, repo snapshots, evidence cards, decision cards, approval queue, lifecycle status, canon signals, client briefs, meeting debriefs, report cards, ops dashboard and export bundle.

```bash
./runtime/bin/brain inbox-add "New signal" "Raw note or source text"
./runtime/bin/brain search "TAP-TAP"
./runtime/bin/brain project-snapshot "andyai-second-brain" --status active --next "PACK4"
./runtime/bin/brain approval-request "Publish brief" "Send client-ready brief" --risk medium
./runtime/bin/brain dashboard
./runtime/bin/brain export-bundle
```

## 🤜💥 PACK4 — Brain Query / Retrieval / Context Assembly Layer

PACK4 adds a local retrieval and context assembly runtime.

Example commands:

```bash
runtime/bin/brain-query index
runtime/bin/brain-query search "second brain runtime"
runtime/bin/brain-query bundle "what should the agent read before PACK5?"
runtime/bin/brain-query handoff "prepare next AndyAI Second Brain strike"
runtime/bin/brain-query answer-draft "what changed in PACK4?"
runtime/bin/brain-query report
```

Canon sentence:

> Search finds files. Retrieval finds relevance. Context assembly prepares action.

## PACK5 — Agent Handoff / Mission Context / Action Preparation Layer

PACK5 turns retrieval context into mission-ready handoff packages. It adds mission request schemas, agent handoff schemas, action plan schemas, risk and permission policies, human approval checklists, mission QA, and the `runtime/bin/brain-mission` CLI.

Canon: Search finds files. Retrieval finds relevance. Context assembly prepares action. PACK5 prepares a governed mission.

