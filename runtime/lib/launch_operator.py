import argparse
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN = "https://brain.andyai.ai"

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return str(target.relative_to(ROOT))

def status():
    data = {
        "kind": "andyai.second_brain.public_status",
        "generated_at": utc_now(),
        "domain": DOMAIN,
        "status": "public-launch-candidate",
        "routes": ["/", "/client/", "/client-portal/", "/health/", "/status/status.json", "/trust/", "/faq/"],
        "privacy_gate": "required-before-public-output",
        "human_approval": "required-before-client-delivery"
    }
    path = ROOT / "public/status/status.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return data

def health():
    html = """<!doctype html>
<html><head><meta charset="utf-8"><title>AndyAI Second Brain Health</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f6f7f8;color:#111;margin:32px}.card{background:#fff;border:1px solid #ddd;border-radius:18px;padding:24px;max-width:900px}.ok{color:#137333;font-weight:700}</style></head>
<body><section class="card"><h1>AndyAI Second Brain — Health</h1><p class="ok">Public static surface online.</p><p>Domain: <code>brain.andyai.ai</code></p><p>Privacy and human approval gates remain part of the production boundary.</p></section></body></html>"""
    return {"ok": True, "file": write("public/health/index.html", html)}

def robots():
    return {"ok": True, "file": write("public/robots.txt", "User-agent: *\nAllow: /\nSitemap: https://brain.andyai.ai/sitemap.xml\n")}

def sitemap():
    routes = ["", "client/", "client-portal/", "health/", "trust/", "faq/"]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for route in routes:
        body.append(f"  <url><loc>{DOMAIN}/{route}</loc></url>")
    body.append("</urlset>\n")
    return {"ok": True, "file": write("public/sitemap.xml", "\n".join(body))}

def trust():
    html = """<!doctype html>
<html><head><meta charset="utf-8"><title>AndyAI Second Brain Trust</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f6f7f8;color:#111;margin:32px}.card{background:#fff;border:1px solid #ddd;border-radius:18px;padding:24px;max-width:960px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}.item{border:1px solid #ddd;border-radius:14px;padding:16px}</style></head>
<body><section class="card"><h1>Trust is the product boundary.</h1><p>AndyAI Second Brain separates public code, private client data, operator evidence, deployment artifacts, secrets, reports, and human-approved delivery surfaces.</p><div class="grid"><div class="item"><b>Privacy Firewall</b><br>Output is scanned before public delivery.</div><div class="item"><b>Human Approval</b><br>Client-facing output requires review.</div><div class="item"><b>Evidence</b><br>Reports connect to audit trails.</div><div class="item"><b>Boundaries</b><br>GitHub, Vercel and Supabase have separate roles.</div></div></section></body></html>"""
    return {"ok": True, "file": write("public/trust/index.html", html)}

def faq():
    html = """<!doctype html>
<html><head><meta charset="utf-8"><title>AndyAI Second Brain FAQ</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f6f7f8;color:#111;margin:32px}.card{background:#fff;border:1px solid #ddd;border-radius:18px;padding:24px;max-width:960px}h2{margin-top:28px}</style></head>
<body><section class="card"><h1>AndyAI Second Brain — FAQ</h1><h2>What is it?</h2><p>A governed AI work-memory and delivery layer for projects, reports, evidence and client-facing outputs.</p><h2>Is everything public?</h2><p>No. Public pages show approved surfaces. Private data belongs behind auth, RLS and approval gates.</p><h2>Why TAP-TAP?</h2><p>TAP-TAP makes production repeatable, versioned, verified and auditable.</p></section></body></html>"""
    return {"ok": True, "file": write("public/faq/index.html", html)}

def readiness():
    data = status()
    health()
    robots()
    sitemap()
    trust()
    faq()
    report = {
        "kind": "andyai.second_brain.launch_readiness",
        "generated_at": utc_now(),
        "domain": DOMAIN,
        "ok": True,
        "routes": data["routes"],
        "notes": [
            "Static public surface exists.",
            "Trust page exists.",
            "FAQ exists.",
            "Health page exists.",
            "Privacy gate remains mandatory for sensitive output."
        ]
    }
    out = ROOT / "brain/launch/reports/launch-readiness.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / "brain/launch/reports/launch-readiness.md"
    md.write_text("# AndyAI Second Brain Launch Readiness\n\n- Domain: https://brain.andyai.ai\n- Status: public launch candidate\n- Privacy boundary: active\n- Human approval: required\n")
    return report

def bundle():
    readiness()
    target = ROOT / "brain/launch/exports/public-launch-dossier.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    items = [
        "brain/launch/reports/launch-readiness.json",
        "brain/launch/reports/launch-readiness.md",
        "public/health/index.html",
        "public/status/status.json",
        "public/robots.txt",
        "public/sitemap.xml",
        "public/trust/index.html",
        "public/faq/index.html",
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in items:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": str(target.relative_to(ROOT))}

def main():
    parser = argparse.ArgumentParser(prog="launch-operator")
    sub = parser.add_subparsers(dest="command", required=True)
    for cmd in ["status", "health", "robots", "sitemap", "trust", "faq", "readiness", "bundle"]:
        sub.add_parser(cmd)
    args = parser.parse_args()
    if args.command == "status":
        print(json.dumps(status(), indent=2))
    elif args.command == "health":
        print(json.dumps(health(), indent=2))
    elif args.command == "robots":
        print(json.dumps(robots(), indent=2))
    elif args.command == "sitemap":
        print(json.dumps(sitemap(), indent=2))
    elif args.command == "trust":
        print(json.dumps(trust(), indent=2))
    elif args.command == "faq":
        print(json.dumps(faq(), indent=2))
    elif args.command == "readiness":
        print(json.dumps(readiness(), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
