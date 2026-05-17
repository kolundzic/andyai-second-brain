import argparse
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def rel(path):
    return str(path.relative_to(ROOT))

def git(args):
    try:
        result = subprocess.run(["git"] + args, cwd=ROOT, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except Exception as exc:
        return f"ERROR: {exc}"

def copy_if_exists(src, dst):
    source = ROOT / src
    target = ROOT / dst
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        shutil.copy2(source, target)
        return rel(target)
    return None

def build_manifest():
    return {
        "kind": "andyai.vercel_static_export",
        "version": "1.0",
        "generated_at": utc_now(),
        "repo": {
            "name": ROOT.name,
            "head": git(["rev-parse", "--short", "HEAD"]),
            "remote": git(["remote", "get-url", "origin"])
        },
        "files": []
    }

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return target

def write_public_index(manifest):
    target = PUBLIC / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    file_rows = []
    for item in manifest["files"]:
        file_rows.append(f"<li><a href='{escape(item)}'>{escape(item)}</a></li>")
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AndyAI Second Brain — Public Control Panel</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:#f6f7f8; color:#111; margin:32px; }}
    .hero {{ background:white; border:1px solid #ddd; border-radius:18px; padding:24px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin-top:18px; }}
    .card {{ background:white; border:1px solid #ddd; border-radius:16px; padding:18px; }}
    a {{ color:#0b57d0; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    code {{ background:#eee; border-radius:6px; padding:2px 5px; }}
  </style>
</head>
<body>
  <section class="hero">
    <h1>AndyAI Second Brain — Public Control Panel</h1>
    <p>Generated: {escape(manifest['generated_at'])}</p>
    <p>HEAD: <code>{escape(manifest['repo']['head'])}</code></p>
  </section>
  <section class="grid">
    <div class="card"><h2>Local Artifact Viewer</h2><p><a href="artifacts/viewer/index.html">Open viewer</a></p></div>
    <div class="card"><h2>Bridge Dashboard</h2><p><a href="artifacts/dashboard/bridge-hub-dashboard.html">Open dashboard</a></p></div>
    <div class="card"><h2>JSON Manifest</h2><p><a href="manifest.json">Open manifest</a></p></div>
  </section>
  <section class="card">
    <h2>Exported files</h2>
    <ul>{''.join(file_rows)}</ul>
  </section>
</body>
</html>
"""
    target.write_text(html)
    return target

def export_public():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest()

    copies = [
        ("brain/viewer/html/index.html", "public/artifacts/viewer/index.html"),
        ("brain/viewer/index/artifact-index.json", "public/artifacts/viewer/artifact-index.json"),
        ("brain/viewer/reports/artifact-viewer.md", "public/artifacts/viewer/artifact-viewer.md"),
        ("brain/dashboard/html/bridge-hub-dashboard.html", "public/artifacts/dashboard/bridge-hub-dashboard.html"),
        ("brain/dashboard/feed/bridge-hub-feed.json", "public/artifacts/dashboard/bridge-hub-feed.json"),
        ("brain/dashboard/reports/bridge-hub-dashboard.md", "public/artifacts/dashboard/bridge-hub-dashboard.md"),
        ("brain/doctor/reports/brain-doctor-report.json", "public/artifacts/doctor/brain-doctor-report.json"),
        ("brain/doctor/reports/brain-doctor-report.md", "public/artifacts/doctor/brain-doctor-report.md"),
    ]
    for src, dst in copies:
        copied = copy_if_exists(src, dst)
        if copied:
            manifest["files"].append(str(Path(copied).relative_to("public")))

    index = write_public_index(manifest)
    manifest["files"].insert(0, "index.html")
    manifest_path = write_json("public/manifest.json", manifest)
    return {"ok": True, "index": rel(index), "manifest": rel(manifest_path), "files": manifest["files"]}

def readiness():
    export = export_public()
    checks = {
        "public_index": (ROOT / "public/index.html").exists(),
        "manifest": (ROOT / "public/manifest.json").exists(),
        "vercel_json": (ROOT / "vercel.json").exists(),
        "viewer": (ROOT / "public/artifacts/viewer/index.html").exists(),
        "dashboard": (ROOT / "public/artifacts/dashboard/bridge-hub-dashboard.html").exists()
    }
    ok = all(checks.values())
    report = {
        "ok": ok,
        "checked_at": utc_now(),
        "checks": checks,
        "export": export
    }
    write_json("brain/vercel/reports/vercel-readiness.json", report)
    md = ROOT / "brain/vercel/reports/vercel-readiness.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text("# Vercel Readiness Report\n\n" + "\n".join([f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in checks.items()]) + "\n")
    return report

def export_bundle(path):
    export_public()
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in (ROOT / "public").rglob("*"):
            if item.is_file():
                archive.write(item, item.relative_to(ROOT))
    return {"ok": True, "export": rel(target)}

def main():
    parser = argparse.ArgumentParser(prog="vercel-export")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("export-public")
    sub.add_parser("readiness")
    sub.add_parser("preview-command")
    p_bundle = sub.add_parser("bundle")
    p_bundle.add_argument("--out", default="brain/vercel/exports/vercel-static-export.zip")
    args = parser.parse_args()

    if args.command == "export-public":
        print(json.dumps(export_public(), indent=2, ensure_ascii=False))
    elif args.command == "readiness":
        result = readiness()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["ok"] else 1)
    elif args.command == "preview-command":
        print("cd public && python3 -m http.server 4173")
    elif args.command == "bundle":
        print(json.dumps(export_bundle(args.out), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
