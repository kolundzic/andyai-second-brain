# Vercel Export Runbook

## Commands

```bash
runtime/bin/vercel-export export-public
runtime/bin/vercel-export readiness
runtime/bin/vercel-export preview-command
runtime/bin/vercel-export bundle
scripts/vercel-static-smoke.sh
scripts/verify-battle-pack27.sh
```

## Local preview

```bash
cd public
python3 -m http.server 4173
```

## Production boundary

Do not deploy production without human approval.
