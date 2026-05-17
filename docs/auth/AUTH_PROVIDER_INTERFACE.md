# Auth Provider Interface

The auth provider layer should expose:

- current user
- current tenant
- user role
- session status
- token freshness
- logout
- protected route guard
- audit event writer

Supported provider direction:

- Supabase Auth as first production candidate
- adapter boundary for future providers

Rule: UI must not trust local display state as authority. Server/RLS boundary remains the real data boundary.
