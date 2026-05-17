# Upload Data Contract

Every upload request should produce a structured intake record.

Required fields:

- tenant_id
- owner_id
- original_file_name
- file_type
- file_size_bytes
- storage_bucket
- storage_path
- status
- privacy_status
- logic_status
- processing_job_id
- created_at

Rule: file bytes are never treated as trusted memory directly.
