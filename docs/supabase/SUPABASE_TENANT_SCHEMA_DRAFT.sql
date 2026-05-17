-- Supabase tenant schema draft
create table if not exists tenants (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now()
);

create table if not exists client_reports (
  id uuid primary key default gen_random_uuid(),
  tenant_id uuid references tenants(id),
  user_id uuid,
  title text not null,
  status text not null default 'draft',
  created_at timestamptz default now()
);
