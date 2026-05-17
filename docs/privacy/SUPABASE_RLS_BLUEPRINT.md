# Supabase RLS Blueprint

Minimum SaaS table rules:

- Every client-owned table must include `tenant_id`
- Every user-owned table must include `user_id`
- Row Level Security must be enabled before production
- Client users may only read rows matching their tenant/user
- Service role keys never go to browser or GitHub
- Audit tables should record human approval and export events
