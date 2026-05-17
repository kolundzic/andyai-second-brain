# Safe Recall Boundary

A memory can be recalled only when:

- tenant boundary matches
- role/permission allows read
- privacy_status is passed or approved
- logic_status is passed or approved
- lifecycle is not archived/blocked
- recall_allowed is true

Rule: recall is not the same as export.
