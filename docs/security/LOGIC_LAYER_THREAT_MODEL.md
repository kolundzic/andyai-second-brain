# Logic Layer Threat Model

Prompt injection is no longer only a prompt problem.

In an agentic system, instruction risk can enter through memory, RAG chunks, metadata, tool context, logs, public exports, previous sessions and imported artifacts.

AndyAI Second Brain must protect the full chain:

Input → Memory → Retrieval → Context Assembly → Authority Check → Policy Gate → Tool Gate → Human Approval → Execution → Evidence Log → Audit → Public Export Gate
