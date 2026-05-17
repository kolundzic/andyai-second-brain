from pathlib import Path
from datetime import datetime, timezone
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return str(p.relative_to(ROOT))

def sample_records():
    return [
        {
            "memory_id": "mem-demo-001",
            "tenant_id": "demo-tenant",
            "owner_id": "demo-user",
            "title": "Upload intake pipeline",
            "summary": "PACK44 introduced a controlled upload corridor with metadata, pre-scans, job queue and audit.",
            "source_type": "upload_intake_report",
            "source_id": "upload-demo-001",
            "evidence_refs": ["brain/upload/reports/upload-intake-pipeline.json"],
            "tags": ["pack44", "upload", "storage", "safety"],
            "classification": "public_demo",
            "lifecycle": "prototype",
            "confidence": 0.91,
            "event_time": utc_now(),
            "recall_allowed": True
        },
        {
            "memory_id": "mem-demo-002",
            "tenant_id": "demo-tenant",
            "owner_id": "demo-user",
            "title": "Protected app shell",
            "summary": "PACK43 introduced login, app shell, access denied page and tenant boundary documentation.",
            "source_type": "auth_tenant_gate_report",
            "source_id": "auth-demo-001",
            "evidence_refs": ["brain/auth/reports/auth-tenant-gate.json"],
            "tags": ["pack43", "auth", "tenant", "app-shell"],
            "classification": "public_demo",
            "lifecycle": "prototype",
            "confidence": 0.9,
            "event_time": utc_now(),
            "recall_allowed": True
        },
        {
            "memory_id": "mem-demo-003",
            "tenant_id": "demo-tenant",
            "owner_id": "demo-user",
            "title": "Client confidential placeholder",
            "summary": "Example of a memory that exists as a blocked placeholder and must not be recalled/exported.",
            "source_type": "policy_demo",
            "source_id": "blocked-demo-001",
            "evidence_refs": [],
            "tags": ["blocked", "privacy"],
            "classification": "client_confidential",
            "lifecycle": "blocked",
            "confidence": 0.5,
            "event_time": utc_now(),
            "recall_allowed": False
        }
    ]

def search(records, query="upload"):
    q = query.lower()
    results = []
    for rec in records:
        haystack = " ".join([rec["title"], rec["summary"], " ".join(rec.get("tags", []))]).lower()
        if q in haystack and rec.get("recall_allowed"):
            results.append(rec)
    return results

def build_reports():
    records = sample_records()
    results = search(records, "upload")
    timeline = sorted(records, key=lambda r: r.get("event_time",""))
    data = {
        "kind": "andyai.second_brain.memory_index",
        "generated_at": utc_now(),
        "ok": True,
        "real_confidential_memory_allowed": False,
        "records": records,
        "search_demo": {"query": "upload", "results": results},
        "timeline_demo": timeline,
        "safe_recall_rule": "tenant + permission + privacy + logic + lifecycle + recall_allowed"
    }
    write("brain/memory/reports/memory-index.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    write("brain/memory/reports/memory-index.md", "# Memory Index Report\n\n- Demo memory records created.\n- Search demo created.\n- Timeline demo created.\n- Blocked record demonstrates safe recall boundary.\n")
    return data

def build_public_memory():
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Memory Index — AndyAI Second Brain</title>
<style>
body{margin:0;background:#f7f7f5;color:#111;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6}
.wrap{width:min(1120px,calc(100% - 36px));margin:0 auto}.nav{background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0}.nav-inner{display:flex;justify-content:space-between;align-items:center;padding:14px 0}.nav a{margin-left:12px;color:#111;text-decoration:none;font-weight:800}
.hero{padding:54px 0 20px}h1{font-size:clamp(40px,7vw,76px);line-height:.94;letter-spacing:-.075em;margin:16px 0}.lead{font-size:20px;max-width:850px;color:#333}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0 60px}.card{background:#fff;border:1px solid #ddd;border-radius:24px;padding:22px;box-shadow:0 16px 50px rgba(0,0,0,.05)}.chip{display:inline-flex;margin:4px;padding:8px 10px;border-radius:999px;background:#eee;font-weight:800;font-size:13px}.danger{background:#fff1f1;border-color:#f0b4b4}@media(max-width:850px){.grid{grid-template-columns:1fr}}
</style></head><body>
<nav class="nav"><div class="wrap nav-inner"><strong>🅰️ Memory Index</strong><div><a href="/">Home</a><a href="/app/">App</a><a href="/upload/">Upload</a><a href="/timeline/">Timeline</a></div></div></nav>
<main class="wrap"><section class="hero"><span class="chip">Searchable memory prototype</span><h1>Uploads become searchable, evidence-linked memory.</h1><p class="lead">PACK45 defines how safe upload/intake records become memory candidates, searchable records, timeline events and evidence-linked knowledge.</p></section>
<section class="grid">
<article class="card"><h2>Search</h2><p>Find memory by keyword, tag, lifecycle, date range and evidence status.</p></article>
<article class="card"><h2>Timeline</h2><p>Place events and decisions in order so the user can understand what happened and when.</p></article>
<article class="card"><h2>Evidence</h2><p>Important memory points back to its source report, upload or document.</p></article>
<article class="card danger"><h2>Safe recall</h2><p>Private or blocked memory cannot be recalled/exported without gates.</p></article>
</section></main></body></html>"""
    return write("public/memory/index.html", html)

def build_public_timeline():
    html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Timeline — AndyAI Second Brain</title>
<style>body{margin:0;background:#f7f7f5;color:#111;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6}.wrap{width:min(980px,calc(100% - 36px));margin:0 auto}.nav{background:#fff;border-bottom:1px solid #ddd}.nav-inner{display:flex;justify-content:space-between;padding:14px 0}.nav a{margin-left:12px;color:#111;text-decoration:none;font-weight:800}.hero{padding:54px 0}.item{background:#fff;border:1px solid #ddd;border-radius:22px;padding:20px;margin:14px 0;box-shadow:0 12px 40px rgba(0,0,0,.05)}h1{font-size:clamp(40px,7vw,72px);line-height:.95;letter-spacing:-.07em}</style></head>
<body><nav class="nav"><div class="wrap nav-inner"><strong>🅰️ Timeline</strong><div><a href="/">Home</a><a href="/memory/">Memory</a><a href="/upload/">Upload</a></div></div></nav><main class="wrap"><section class="hero"><h1>Memory has time.</h1><p>Timeline view organizes memory by event, milestone, source and evidence.</p></section><section><article class="item"><h2>PACK42</h2><p>Supabase protected data foundation.</p></article><article class="item"><h2>PACK43</h2><p>Auth / tenant gate / protected app shell.</p></article><article class="item"><h2>PACK44</h2><p>Controlled upload intake pipeline.</p></article><article class="item"><h2>PACK45</h2><p>Memory index, search and timeline layer.</p></article></section></main></body></html>"""
    return write("public/timeline/index.html", html)

def patch_nav():
    for rel in ["public/index.html", "public/app/index.html"]:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(errors="ignore")
        if 'href="/memory/"' not in text:
            if 'href="/upload/"' in text:
                text = text.replace('<a href="/upload/">Upload</a>', '<a href="/upload/">Upload</a><a href="/memory/">Memory</a>')
            elif 'href="/app/"' in text:
                text = text.replace('<a href="/app/">App</a>', '<a href="/app/">App</a><a href="/memory/">Memory</a>')
        if 'href="/timeline/"' not in text and 'href="/memory/"' in text:
            text = text.replace('<a href="/memory/">Memory</a>', '<a href="/memory/">Memory</a><a href="/timeline/">Timeline</a>')
        p.write_text(text)

def build_all():
    build_reports()
    build_public_memory()
    build_public_timeline()
    patch_nav()
    return {"ok": True, "memory": "public/memory/index.html", "timeline": "public/timeline/index.html"}

def bundle():
    build_all()
    target = ROOT / "brain/memory/exports/memory-index-search-timeline-pack.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    items = [
        "public/memory/index.html",
        "public/timeline/index.html",
        "brain/memory/reports/memory-index.json",
        "brain/memory/reports/memory-index.md",
        "docs/memory/MEMORY_RECORD_CONTRACT.md",
        "docs/search/SEARCH_QUERY_MODEL.md",
        "docs/timeline/TIMELINE_EVENT_MODEL.md",
        "docs/evidence/EVIDENCE_LINK_MODEL.md",
        "schemas/memory/memory-record.schema.json"
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in items:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": str(target.relative_to(ROOT))}

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="memory-index")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("search")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build_all(), indent=2))
    elif args.command == "search":
        print(json.dumps(search(sample_records(), "upload"), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
