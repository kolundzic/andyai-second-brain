-- AndyAI Second Brain — Supabase Protected Data Foundation
-- Draft migration. Review before applying to production.

create extension if not exists "uuid-ossp";

create table if not exists public.tenants (
  id uuid primary key default uuid_generate_v4(),
  name text not null,
  slug text unique not null,
  status text not null default 'active',
  created_at timestamptz not null default now()
);

create table if not exists public.profiles (
  id uuid primary key,
  tenant_id uuid references public.tenants(id) on delete cascade,
  email text,
  display_name text,
  role text not null default 'member',
  created_at timestamptz not null default now()
);

create table if not exists public.memory_items (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade not null,
  owner_id uuid,
  title text not null,
  body text,
  source_type text not null default 'manual',
  lifecycle text not null default 'draft',
  evidence_status text not null default 'generated',
  visibility text not null default 'private',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.documents (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade not null,
  owner_id uuid,
  title text not null,
  file_name text,
  file_type text,
  storage_path text,
  classification text not null default 'unclassified',
  privacy_status text not null default 'needs_review',
  logic_status text not null default 'needs_scan',
  created_at timestamptz not null default now()
);

create table if not exists public.uploads (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade not null,
  owner_id uuid,
  document_id uuid references public.documents(id) on delete set null,
  file_name text not null,
  storage_path text not null,
  status text not null default 'received',
  created_at timestamptz not null default now()
);

create table if not exists public.processing_jobs (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade not null,
  upload_id uuid references public.uploads(id) on delete cascade,
  job_type text not null,
  status text not null default 'queued',
  result jsonb,
  error text,
  created_at timestamptz not null default now(),
  finished_at timestamptz
);

create table if not exists public.audit_logs (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade,
  actor_id uuid,
  action text not null,
  target_type text,
  target_id uuid,
  metadata jsonb,
  created_at timestamptz not null default now()
);

create table if not exists public.approval_events (
  id uuid primary key default uuid_generate_v4(),
  tenant_id uuid references public.tenants(id) on delete cascade not null,
  actor_id uuid,
  target_type text not null,
  target_id uuid,
  decision text not null,
  reason text,
  created_at timestamptz not null default now()
);

alter table public.tenants enable row level security;
alter table public.profiles enable row level security;
alter table public.memory_items enable row level security;
alter table public.documents enable row level security;
alter table public.uploads enable row level security;
alter table public.processing_jobs enable row level security;
alter table public.audit_logs enable row level security;
alter table public.approval_events enable row level security;
