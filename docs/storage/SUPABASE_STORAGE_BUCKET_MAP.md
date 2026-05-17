# Supabase Storage Bucket Map

| Bucket | Access | Purpose |
|---|---|---|
| private-uploads | private | raw user uploads |
| processed-artifacts | private | extracted/summarized artifacts |
| public-demo-assets | public-safe only | non-confidential demo assets |

Rule: `private-uploads` is never public.
