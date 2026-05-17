# Supabase Anon Key Safety

The anon key is browser-safe only when Row Level Security is enabled and strict tenant-scoped policies exist.

The anon key is not a privacy boundary by itself.

Real boundary:

- RLS enabled
- tenant-scoped policies
- server-only service role
- audit logs
- approval gates
