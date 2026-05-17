import argparse, json, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def generate():
    manifest = {
        "kind": "andyai.client_portal.blueprint",
        "generated_at": utc_now(),
        "routes": ["/client/", "/client-portal/", "/client-portal/reports", "/client-portal/evidence"],
        "auth_boundary": "required-before-real-client-data",
        "human_approval": "required-before-publication"
    }
    out = ROOT / "brain/client-portal/reports/client-portal-manifest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    public = ROOT / "public/client-portal/index.html"
    public.parent.mkdir(parents=True, exist_ok=True)
    public.write_text("""<!doctype html>
<html><head><meta charset="utf-8"><title>AndyAI Client Portal Blueprint</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f6f7f8;margin:32px;color:#111}.card{background:#fff;border:1px solid #ddd;border-radius:18px;padding:24px;max-width:920px}code{background:#eee;padding:2px 6px;border-radius:6px}</style></head>
<body><section class="card"><h1>AndyAI Client Portal Blueprint</h1><p>This is a protected-client-portal readiness surface, not a production client data portal.</p><p><strong>Auth boundary:</strong> required before real client data.</p><p><strong>Human approval:</strong> required before publication.</p><p><a href="/client/">Open sample client report</a></p></section></body></html>""")
    md = ROOT / "brain/client-portal/reports/client-portal-blueprint.md"
    md.write_text("# Client Portal Blueprint\n\nAuth boundary required before real client data.\n")
    return {"ok": True, "manifest": str(out.relative_to(ROOT)), "public": "public/client-portal/index.html"}

def bundle():
    generated = generate()
    target = ROOT / "brain/client-portal/exports/client-portal-blueprint.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in ["brain/client-portal/reports/client-portal-manifest.json", "brain/client-portal/reports/client-portal-blueprint.md", "public/client-portal/index.html"]:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    generated["export"] = str(target.relative_to(ROOT))
    return generated

def main():
    parser = argparse.ArgumentParser(prog="client-portal")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("generate")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "generate":
        print(json.dumps(generate(), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
