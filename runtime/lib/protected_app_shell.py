from pathlib import Path
from datetime import datetime, timezone
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    return str(p.relative_to(ROOT))

def nav():
    return '<a href="/">Home</a><a href="/help/">Help</a><a href="/knowledge/">Knowledge</a><a href="/login/">Login</a><a href="/app/">App</a>'

def base_html(title, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
body{{margin:0;background:#f7f7f5;color:#111;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.6}}
.wrap{{width:min(1120px,calc(100% - 36px));margin:0 auto}}
.nav{{background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0}}.nav-inner{{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:14px 0}}.nav a{{margin-left:12px;color:#111;text-decoration:none;font-weight:800}}
.hero{{padding:54px 0 20px}}h1{{font-size:clamp(40px,7vw,76px);line-height:.94;letter-spacing:-.075em;margin:16px 0}}.lead{{font-size:20px;max-width:820px;color:#333}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0 60px}}.card{{background:#fff;border:1px solid #ddd;border-radius:24px;padding:22px;box-shadow:0 16px 50px rgba(0,0,0,.05)}}.chip{{display:inline-flex;margin:4px;padding:8px 10px;border-radius:999px;background:#eee;font-weight:800;font-size:13px}}.danger{{background:#fff1f1;border-color:#f0b4b4}}.ok{{background:#f2fff5;border-color:#b8e4c2}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
<nav class="nav"><div class="wrap nav-inner"><strong>🅰️ AndyAI Protected App</strong><div>{nav()}</div></div></nav>
<main class="wrap">{body}</main></body></html>"""

def build_login():
    body = """<section class="hero"><span class="chip">Auth prototype</span><h1>Login to your protected Second Brain.</h1><p class="lead">This page is a prototype for Supabase Auth login. Real authentication will be activated only after tenant/RLS boundaries are verified.</p></section><section class="grid"><article class="card"><h2>Planned login</h2><p>Email magic link / password / approved provider.</p><p>No open production signup until tenant policy is approved.</p></article><article class="card danger"><h2>Safety rule</h2><p>Service role key never appears in browser code. App shell never bypasses RLS.</p></article></section>"""
    return write("public/login/index.html", base_html("Login — AndyAI Second Brain", body))

def build_access_denied():
    body = """<section class="hero"><span class="chip">Protected boundary</span><h1>Access denied.</h1><p class="lead">This route explains that private app data requires authenticated tenant access and approved role permissions.</p></section><section class="card danger"><h2>Why blocked?</h2><p>No tenant session, expired session, insufficient role, or policy denial.</p></section>"""
    return write("public/access-denied/index.html", base_html("Access Denied — AndyAI Second Brain", body))

def build_app():
    body = """<section class="hero"><span class="chip">Protected app shell prototype</span><h1>Your private Second Brain workspace.</h1><p class="lead">This is the first protected app shell mock. It shows the future private workspace layout while real data remains blocked until Auth, RLS, storage, privacy, logic-layer and human approval gates are verified.</p></section><section class="grid"><article class="card ok"><h2>Tenant status</h2><p>Tenant: demo workspace</p><p>Role: owner/operator prototype</p><p>Boundary: tenant-scoped only</p></article><article class="card"><h2>Ask Brain</h2><p>Private dialog panel placeholder.</p></article><article class="card"><h2>Uploads</h2><p>Future Supabase Storage intake entry.</p></article><article class="card"><h2>Memory</h2><p>Tenant-scoped memory list placeholder.</p></article><article class="card"><h2>Audit</h2><p>Session and workflow audit activity placeholder.</p></article><article class="card"><h2>Approvals</h2><p>Human approval queue placeholder.</p></article></section>"""
    return write("public/app/index.html", base_html("App — AndyAI Second Brain", body))

def patch_home():
    p = ROOT / "public/index.html"
    if not p.exists():
        return
    text = p.read_text(errors="ignore")
    if 'href="/login/"' not in text and 'href="/help/"' in text:
        text = text.replace('<a href="/help/">Help</a>', '<a href="/help/">Help</a>\n        <a href="/login/">Login</a>')
    p.write_text(text)

def report():
    data = {
        "kind": "andyai.second_brain.auth_tenant_gate",
        "generated_at": utc_now(),
        "ok": True,
        "routes": ["/login/", "/app/", "/access-denied/"],
        "status": "protected_app_shell_prototype_ready",
        "real_client_data_allowed": False,
        "requires_before_real_data": ["Supabase Auth", "RLS verified", "tenant session verified", "storage policy verified", "privacy firewall", "logic-layer firewall", "human approval"]
    }
    out = ROOT / "brain/auth/reports/auth-tenant-gate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / "brain/auth/reports/auth-tenant-gate.md"
    md.write_text("# Auth Tenant Gate Report\n\n- Login prototype created.\n- Protected app shell prototype created.\n- Access denied page created.\n- Real client data remains blocked.\n")
    return data

def build_all():
    build_login()
    build_access_denied()
    build_app()
    patch_home()
    return report()

def bundle():
    build_all()
    target = ROOT / "brain/auth/exports/auth-tenant-gate-pack.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    items = [
        "public/login/index.html",
        "public/app/index.html",
        "public/access-denied/index.html",
        "docs/auth/AUTH_PROVIDER_INTERFACE.md",
        "docs/tenant/TENANT_SESSION_BOUNDARY.md",
        "docs/tenant/ROLE_MATRIX.md",
        "docs/app-shell/PROTECTED_APP_SHELL_BLUEPRINT.md",
        "brain/auth/reports/auth-tenant-gate.json",
        "brain/auth/reports/auth-tenant-gate.md"
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in items:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": str(target.relative_to(ROOT))}

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="protected-app-shell")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("report")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build_all(), indent=2))
    elif args.command == "report":
        print(json.dumps(report(), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
