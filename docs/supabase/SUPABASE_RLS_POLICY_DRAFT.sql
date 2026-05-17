-- Supabase RLS policy draft
alter table client_reports enable row level security;

create policy "tenant users can read own tenant reports"
on client_reports for select
using (tenant_id::text = current_setting('request.jwt.claims', true)::jsonb->>'tenant_id');
