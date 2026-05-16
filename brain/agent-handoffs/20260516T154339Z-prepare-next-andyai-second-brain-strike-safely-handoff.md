# Agent Handoff

Mission ID: 20260516T154339Z-prepare-next-andyai-second-brain-strike-safely
Goal: Prepare next AndyAI Second Brain strike safely

## Context Summary
This handoff prepares the agent to work on the mission using selected local brain context.

## Relevant Files
- brain/context/handoffs/20260516T153541Z-prepare-pack5-for-andyai-second-brain-agent-handoff.md
- brain/queries/second-brain.json
- brain/context/bundles/20260516T153541Z-query-brain-assemble-context-answer-with-evidence-skills.json
- brain/context/bundles/20260516T153541Z-query-brain-assemble-context-answer-with-evidence-skills.md
- brain/queries/sample-second-brain-search.txt
- brain/context/bundles/20260516T153540Z-andyai-second-brain-current-project-status.md
- brain/context/bundles/20260516T153544Z-source-priority-evidence-decision-project.md
- brain/context/bundles/20260516T153540Z-andyai-second-brain-current-project-status.json

## Allowed Actions
- read repository files
- assemble context
- draft local docs
- run verifiers

## Blocked Actions
- publish externally without approval
- delete canon without approval
- change production without approval

## Stop Conditions
- verifier fails
- tree is dirty unexpectedly
- required approval is missing

## Next Action
Review the mission context and proceed only within allowed actions.
