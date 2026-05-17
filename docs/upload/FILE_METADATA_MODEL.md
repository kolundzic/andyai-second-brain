# File Metadata Model

Metadata must be created before processing.

| Field | Meaning |
|---|---|
| original_file_name | user-facing name |
| normalized_file_name | safe internal name |
| extension | file extension |
| mime_type | detected type |
| size_bytes | size |
| sha256 | integrity/fingerprint placeholder |
| tenant_id | workspace boundary |
| owner_id | uploader |
| classification | unclassified/private/public-demo |
| privacy_status | needs_scan / passed / blocked |
| logic_status | needs_scan / passed / blocked |
