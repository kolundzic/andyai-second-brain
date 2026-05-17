# Processing Job Queue Model

Each upload may create a processing job.

Job types:

- extract_text
- classify_document
- privacy_scan
- logic_scan
- summarize
- prepare_memory_candidate
- generate_report_draft

Job statuses:

- queued
- running
- passed
- blocked
- failed
- needs_operator_review
