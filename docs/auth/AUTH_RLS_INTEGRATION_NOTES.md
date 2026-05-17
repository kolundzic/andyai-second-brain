# Auth / RLS Integration Notes

Supabase Auth identifies the user.
Profiles map user to tenant.
RLS limits tenant-scoped rows.
Application shell only displays data allowed by RLS.

The app UI is not the authority. Database policies are the authority.
