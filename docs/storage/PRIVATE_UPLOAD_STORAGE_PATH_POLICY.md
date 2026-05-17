# Private Upload Storage Path Policy

Recommended path format:

```text
tenant/{tenant_id}/user/{owner_id}/uploads/{upload_id}/{safe_file_name}
```

Rules:

- no raw email in path
- no client name in path unless approved
- no unescaped original filename
- tenant_id must be present
- upload_id must be present
- path must be audit-loggable
