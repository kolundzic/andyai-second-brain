# Environment Variable Map

## Public / browser-safe

```bash
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

## Server-only / never public

```bash
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
SUPABASE_DB_URL=
```

The service role key must never be placed in `public/`, client-side code, screenshots, README examples with real values, or Vercel public variables.
