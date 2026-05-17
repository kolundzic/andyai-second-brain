# Supabase Connection Guide

Supabase provides the protected data layer for AndyAI Second Brain.

It stores tenant/workspace data, profiles, memory items, documents, uploads, processing jobs, audit logs and approval events.

## Connection rule

Use anon key only in browser-safe code.
Use service role key only in trusted backend/operator code.
Never expose service role key in public HTML, browser JavaScript, screenshots, docs with real values, or GitHub.
