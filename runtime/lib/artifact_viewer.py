import argparse
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[2]

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

def collect_files(folder, suffixes=None, limit=500):
    base = ROOT / folder
    out = []
    if not base.exists():
        return out
    for item in sorted(base.rglob("*")):
        if item.is_file() and (suffixes is None or item.suffix.lower() in suffixes):
            out.append({
                "path": rel(item),
                "name": item.name,
                "size": item.stat().st_size,
                "type": item.suffix.lower().lstrip(".") or "file"
            })
            if len(out) >= limit:
                break
    return out

def build_index():
    latest_tags = [x for x in git(["tag", "--sort=-creatordate"]).splitlines()[:20] if x.strip()]
    return {
        "kind": "andyai.artifact_viewer.index",
        "version": "1.0",
        "generated_at": utc_now(),
        "repo": {
            "name": ROOT.name,
            "path": str(ROOT),
            "head": git(["rev-parse", "--short", "HEAD"]),
            "remote": git(["remote", "get-url", "origin"]),
            "latest_tags": latest_tags
        },
        "sections": [
            {"id": "dashboard", "title": "Dashboard Artifacts", "items": collect_files("brain/dashboard", {".json", ".md", ".html", ".zip"})},
            {"id": "doctor", "title": "Doctor Artifacts", "items": collect_files("brain/doctor", {".json", ".md", ".zip"})},
            {"id": "reports", "title": "Reports", "items": collect_files("brain/reports", {".json", ".md"})},
            {"id": "evidence", "title": "Evidence", "items": collect_files("evidence", None)},
            {"id": "exports", "title": "Exports", "items": collect_files("brain", {".zip"})},
            {"id": "release_notes", "title": "Release Notes", "items": collect_files("release-notes", {".md"})},
            {"id": "schemas", "title": "Schemas", "items": collect_files("schemas", {".json"})},
        ]
    }

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return target

def write_markdown(path, index):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# AndyAI Artifact Viewer",
        "",
        f"Generated: {index['generated_at']}",
        "",
        "## Repo",
        "",
        f"- Name: {index['repo']['name']}",
        f"- HEAD: {index['repo']['head']}",
        f"- Remote: {index['repo']['remote']}",
        "",
    ]
    for section in index["sections"]:
        lines.append(f"## {section['title']}")
        lines.append("")
        if not section["items"]:
            lines.append("- No artifacts found.")
        for item in section["items"][:100]:
            lines.append(f"- `{item['path']}` — {item['size']} bytes")
        lines.append("")
    target.write_text("\n".join(lines))
    return target

def write_html(path, index):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    cards = []
    for section in index["sections"]:
        rows = []
        for item in section["items"][:200]:
            href = "../" * 2 + item["path"] if path.count("/") >= 2 else item["path"]
            rows.append(
                f"<tr><td><a href='../../{escape(item['path'])}'>{escape(item['path'])}</a></td>"
                f"<td>{escape(item['type'])}</td><td>{item['size']}</td></tr>"
            )
        if not rows:
            rows.append("<tr><td colspan='3'>No artifacts found.</td></tr>")
        cards.append(f"""
        <section class="card">
          <h2>{escape(section['title'])}</h2>
          <table>
            <thead><tr><th>Path</th><th>Type</th><th>Bytes</th></tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </section>
        """)
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AndyAI Local Artifact Control Panel</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 28px; background: #f6f7f8; color: #111; }}
    h1 {{ font-size: 32px; margin-bottom: 4px; }}
    .meta {{ color: #555; margin-bottom: 24px; }}
    .card {{ background: white; border: 1px solid #ddd; border-radius: 16px; padding: 18px; margin: 16px 0; box-shadow: 0 2px 12px rgba(0,0,0,0.05); }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ text-align: left; border-bottom: 1px solid #eee; padding: 8px; font-size: 14px; }}
    a {{ color: #0b57d0; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    code {{ background: #eee; padding: 2px 5px; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>AndyAI Local Artifact Control Panel</h1>
  <div class="meta">
    Generated: {escape(index['generated_at'])}<br>
    Repo: {escape(index['repo']['name'])} · HEAD: <code>{escape(index['repo']['head'])}</code>
  </div>
  {''.join(cards)}
</body>
</html>
"""
    target.write_text(html)
    return target

def generate_all():
    index = build_index()
    json_path = write_json("brain/viewer/index/artifact-index.json", index)
    md_path = write_markdown("brain/viewer/reports/artifact-viewer.md", index)
    html_path = write_html("brain/viewer/html/index.html", index)
    return {"ok": True, "json": rel(json_path), "markdown": rel(md_path), "html": rel(html_path)}

def export_bundle(path):
    generated = generate_all()
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for key in ["json", "markdown", "html"]:
            p = ROOT / generated[key]
            archive.write(p, p.relative_to(ROOT))
    generated["export"] = rel(target)
    return generated

def open_panel():
    panel = ROOT / "brain/viewer/html/index.html"
    if not panel.exists():
        generate_all()
    if sys.platform == "darwin":
        subprocess.run(["open", str(panel)], check=False)
    else:
        print(panel)
    return {"ok": True, "html": rel(panel)}

def main():
    parser = argparse.ArgumentParser(prog="artifact-viewer")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("collect")
    sub.add_parser("generate-json")
    sub.add_parser("generate-md")
    sub.add_parser("generate-html")
    sub.add_parser("generate-all")
    sub.add_parser("open")
    p_export = sub.add_parser("export")
    p_export.add_argument("--out", default="brain/viewer/exports/artifact-viewer-export.zip")

    args = parser.parse_args()

    if args.command == "collect":
        print(json.dumps(build_index(), indent=2, ensure_ascii=False))
    elif args.command == "generate-json":
        index = build_index()
        path = write_json("brain/viewer/index/artifact-index.json", index)
        print(json.dumps({"ok": True, "json": rel(path)}, indent=2))
    elif args.command == "generate-md":
        index = build_index()
        path = write_markdown("brain/viewer/reports/artifact-viewer.md", index)
        print(json.dumps({"ok": True, "markdown": rel(path)}, indent=2))
    elif args.command == "generate-html":
        index = build_index()
        path = write_html("brain/viewer/html/index.html", index)
        print(json.dumps({"ok": True, "html": rel(path)}, indent=2))
    elif args.command == "generate-all":
        print(json.dumps(generate_all(), indent=2, ensure_ascii=False))
    elif args.command == "export":
        print(json.dumps(export_bundle(args.out), indent=2, ensure_ascii=False))
    elif args.command == "open":
        print(json.dumps(open_panel(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
