# 🧠 Working Brain Runtime Layer

The Working Brain Runtime Layer is the first practical runtime for AndyAI Second Brain.

It does not replace human judgment. It creates local, inspectable files that help humans and AI agents preserve work continuity.

## Runtime Loop

```text
intake → classify → route → write → verify → report → human review
```

## Local-First Rule

All runtime actions write to local files first. Publishing, deleting canon, changing production, or sending client material requires human approval.

## Practical Commands

```bash
./runtime/bin/brain index
./runtime/bin/brain memory-create "Title" "Body"
./runtime/bin/brain decision-record "Decision" "Reason"
./runtime/bin/brain evidence-link "Claim" "Evidence"
./runtime/bin/brain repo-status
./runtime/bin/brain report
```
