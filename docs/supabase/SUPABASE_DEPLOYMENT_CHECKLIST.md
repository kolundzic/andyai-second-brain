# Supabase Deployment Checklist

Before production:

- RLS enabled on all tenant/client tables
- no service role key in public files
- storage buckets private by default
- audit logs enabled
- approval events enabled
- privacy firewall passed
- logic-layer firewall passed
- Vercel env vars separated public/server-only
- human approval before real client data
