# Tenant Session Boundary

A session must resolve:

- user_id
- tenant_id
- role
- workspace status
- allowed features
- data boundary

No tenant_id means no private app data access.

Tenant boundary rule:

A user can only access tenant-scoped rows allowed by RLS and role policy.
