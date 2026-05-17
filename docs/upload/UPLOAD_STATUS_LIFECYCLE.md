# Upload Status Lifecycle

Normal states:

```text
received
metadata_created
privacy_prescan_pending
logic_prescan_pending
storage_ready
processing_queued
processed
memory_candidate
approved_for_memory
```

Blocked states:

```text
rejected_file_type
rejected_size
privacy_blocked
logic_blocked
operator_review_required
```
