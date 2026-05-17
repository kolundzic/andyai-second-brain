# Supabase Storage Bucket Policy

## Buckets

- `private-uploads`
- `processed-artifacts`
- `public-demo-assets`

## Rules

- `private-uploads` is never public.
- user uploads must be tenant-scoped.
- public demo assets must contain no client confidential data.
- generated exports require privacy + logic-layer + human approval gates.
- service role operations must stay server-side only.
