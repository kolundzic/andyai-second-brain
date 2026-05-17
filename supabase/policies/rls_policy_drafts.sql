-- RLS Policy Drafts
-- Review carefully before applying to production.

create policy "profiles_select_own_tenant"
on public.profiles for select
using (
  id = auth.uid()
  or tenant_id in (select tenant_id from public.profiles where id = auth.uid())
);

create policy "memory_items_select_tenant"
on public.memory_items for select
using (
  tenant_id in (select tenant_id from public.profiles where id = auth.uid())
);

create policy "documents_select_tenant"
on public.documents for select
using (
  tenant_id in (select tenant_id from public.profiles where id = auth.uid())
);

create policy "uploads_select_tenant"
on public.uploads for select
using (
  tenant_id in (select tenant_id from public.profiles where id = auth.uid())
);

create policy "audit_logs_select_tenant"
on public.audit_logs for select
using (
  tenant_id in (select tenant_id from public.profiles where id = auth.uid())
);
