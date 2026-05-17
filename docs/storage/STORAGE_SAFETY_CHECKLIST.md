# Storage Safety Checklist

Before production upload:

- private bucket exists
- RLS/tenant boundary reviewed
- storage path does not expose PII
- service role key is server-only
- upload size limits configured
- unsupported file types blocked
- privacy pre-scan enabled
- logic-layer pre-scan enabled
- audit event recorded
- human approval boundary documented
