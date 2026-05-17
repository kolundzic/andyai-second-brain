# Memory Index Scaffold

Memory Index transforms safe intake metadata and approved content candidates into structured memory records.

Pipeline:

```text
upload intake
  ↓
memory candidate
  ↓
classification
  ↓
evidence link
  ↓
search index
  ↓
timeline event
  ↓
human-approved recall/export
```

Rule: uploaded content is not automatically trusted memory.
