#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p public/knowledge brain/knowledge/reports brain/knowledge/exports
if ! grep -q "## Knowledge Front Page" README.md; then
cat >> README.md <<'MARK'

## Knowledge Front Page

AndyAI Second Brain treats this repository as a living knowledge front page, not just a code/document folder.

Start by audience:

- [Beginner Learning Path](./docs/learning-paths/BEGINNER_LEARNING_PATH.md)
- [Operator Learning Path](./docs/learning-paths/OPERATOR_LEARNING_PATH.md)
- [Builder Learning Path](./docs/learning-paths/BUILDER_LEARNING_PATH.md)
- [Business Learning Path](./docs/learning-paths/BUSINESS_LEARNING_PATH.md)

Knowledge maps:

- [Knowledge Domain Map](./docs/knowledge-front-page/KNOWLEDGE_DOMAIN_MAP.md)
- [Resource Cards](./docs/resources/RESOURCE_CARDS.md)
- [Evidence Status Legend](./docs/evidence/EVIDENCE_STATUS_LEGEND.md)
- [Lifecycle Tag System](./docs/lifecycle/LIFECYCLE_TAG_SYSTEM.md)
- [Export-Ready Document Map](./docs/exports/EXPORT_READY_DOCUMENT_MAP.md)
- [Operator Help Index](./docs/operator/OPERATOR_HELP_INDEX.md)

Public knowledge route: `/knowledge/`
MARK
fi
cat > public/knowledge/index.html <<'HTML'
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Knowledge Front Page — AndyAI Second Brain</title><style>body{margin:0;background:#f7f7f5;color:#111;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6}.wrap{width:min(1120px,calc(100% - 36px));margin:0 auto}.nav{background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0}.nav-inner{display:flex;justify-content:space-between;align-items:center;padding:14px 0}.btn{display:inline-flex;padding:10px 14px;border-radius:999px;border:1px solid #ddd;text-decoration:none;font-weight:800;background:#fff;color:#111}.hero{padding:56px 0 24px}h1{font-size:clamp(40px,7vw,76px);line-height:.94;letter-spacing:-.075em;margin:16px 0}.lead{font-size:20px;color:#333;max-width:860px}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0 60px}.card{background:#fff;border:1px solid #ddd;border-radius:24px;padding:22px;box-shadow:0 16px 50px rgba(0,0,0,.05)}code{background:#f2f2f2;padding:2px 6px;border-radius:6px}.chip{display:inline-flex;margin:4px;padding:8px 10px;border-radius:999px;background:#eee;font-weight:800;font-size:13px}@media(max-width:850px){.grid{grid-template-columns:1fr}}</style></head><body><nav class="nav"><div class="wrap nav-inner"><strong>🅰️ Knowledge Front Page</strong><div><a class="btn" href="/">Home</a> <a class="btn" href="/help/">Help</a> <a class="btn" href="/dialog/">Dialog</a></div></div></nav><main class="wrap"><section class="hero"><span class="chip">README gateway</span><span class="chip">Learning paths</span><span class="chip">Evidence map</span><span class="chip">Export-ready docs</span><h1>The repo as a living knowledge front page.</h1><p class="lead">AndyAI Second Brain organizes what is canonical, what is draft, what is prototype, what can be exported, and how beginners, operators, builders and business users should enter the system.</p></section><section class="grid"><article class="card"><h3>README Gateway</h3><p><code>README.md</code></p><p>First visible intelligence surface.</p></article><article class="card"><h3>Learning Paths</h3><p>Beginner, Operator, Builder and Business paths.</p></article><article class="card"><h3>Evidence & Lifecycle</h3><p>Canonical, verified, draft, prototype, blueprint and archived status.</p></article><article class="card"><h3>Export Map</h3><p>PDF/DOCX/HTML handoff paths for partners, clients and operators.</p></article><article class="card"><h3>Operator Help</h3><p>Daily checks, route checks and safety gates.</p></article><article class="card"><h3>Resource Cards</h3><p>Important docs classified by audience, lifecycle, evidence and export status.</p></article></section></main></body></html>
HTML
cat > brain/knowledge/reports/knowledge-front-page.json <<JSON
{"kind":"andyai.second_brain.knowledge_front_page","generated_at":"$(date -u +"%Y-%m-%dT%H:%M:%SZ")","ok":true,"canon":"README is the first visible intelligence surface of the repository.","public_route":"/knowledge/"}
JSON
cat > brain/knowledge/reports/knowledge-front-page.md <<'MD'
# Knowledge Front Page Report

- README gateway upgraded.
- Learning paths created.
- Resource cards created.
- Public `/knowledge/` route generated.
MD
zip -qr brain/knowledge/exports/knowledge-front-page-pack.zip public/knowledge docs/knowledge-front-page docs/learning-paths docs/resources docs/evidence docs/lifecycle docs/operator docs/exports docs/visual-maps brain/knowledge/reports
