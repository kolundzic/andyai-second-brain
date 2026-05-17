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

def read_json(path):
    target = ROOT / path
    if not target.exists():
        return None
    try:
        return json.loads(target.read_text())
    except Exception as exc:
        return {"error": str(exc), "path": str(path)}

def git(args):
    try:
        result = subprocess.run(["git"] + args, cwd=ROOT, text=True, capture_output=True, check=True)
        return result.stdout.strip()
    except Exception as exc:
        return f"ERROR: {exc}"

def latest_tag():
    tags = git(["tag", "--sort=-creatordate"]).splitlines()
    return tags[0] if tags else "unknown"

def repo_summary():
    return {
        "repo": ROOT.name,
        "path": str(ROOT),
        "head": git(["rev-parse", "--short", "HEAD"]),
        "latest_tag": latest_tag(),
        "remote": git(["remote", "get-url", "origin"]),
        "generated_at": utc_now()
    }

def count_files(folder, suffixes=None):
    base = ROOT / folder
    if not base.exists():
        return 0
    count = 0
    for item in base.rglob("*"):
        if item.is_file() and (suffixes is None or item.suffix.lower() in suffixes):
            count += 1
    return count

def doctor_report():
    return read_json("brain/doctor/reports/brain-doctor-report.json") or {}

def pack_status():
    status_files = [
        "brain/battle-pack24/status/BATTLE_PACK24_STATUS.json",
        "brain/battle-pack25/status/BATTLE_PACK25_STATUS.json",
        "brain/big-plotun-03/status/BIG_PLOTUN_03_STATUS.json",
        "brain/big-plotun-02/status/BIG_PLOTUN_02_STATUS.json",
    ]
    found = []
    for item in status_files:
        data = read_json(item)
        if data:
            found.append({"path": item, "data": data})
    return found

def build_feed():
    doctor = doctor_report()
    packs = pack_status()
    repo = repo_summary()
    counts = {
        "schemas": count_files("schemas", {".json"}),
        "docs": count_files("docs", {".md"}),
        "evidence": count_files("evidence", None),
        "reports": count_files("brain/reports", {".md", ".json"}),
        "exports": count_files("brain", {".zip"})
    }
    cards = [
        {"id": "repo", "title": "Repo", "status": "ok", "data": repo},
        {"id": "doctor", "title": "Brain Doctor", "status": "ok" if doctor.get("ok", False) else "unknown", "data": doctor},
        {"id": "counts", "title": "Artifact Counts", "status": "ok", "data": counts},
        {"id": "packs", "title": "Pack Status", "status": "ok", "data": packs},
    ]
    return {
        "kind": "andyai.bridge_hub.dashboard_feed",
        "version": "1.0",
        "generated_at": utc_now(),
        "repo": repo,
        "cards": cards
    }

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return target

def write_markdown(path, feed):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bridge Hub Dashboard Feed",
        "",
        f"Generated: {feed['generated_at']}",
        "",
        "## Repo",
        "",
        f"- Name: {feed['repo'].get('repo')}",
        f"- HEAD: {feed['repo'].get('head')}",
        f"- Latest tag: {feed['repo'].get('latest_tag')}",
        f"- Remote: {feed['repo'].get('remote')}",
        "",
        "## Cards",
        "",
    ]
    for card in feed["cards"]:
        lines.append(f"### {card['title']}")
        lines.append("")
        lines.append(f"- Status: {card['status']}")
        data = card.get("data")
        if isinstance(data, dict):
            for key in list(data.keys())[:10]:
                value = data[key]
                if isinstance(value, (str, int, float, bool)):
                    lines.append(f"- {key}: {value}")
        elif isinstance(data, list):
            lines.append(f"- Items: {len(data)}")
        lines.append("")
    target.write_text("\n".join(lines))
    return target

def write_html(path, feed):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    cards = []
    for card in feed["cards"]:
        cards.append(f"""
        <section class="card">
          <h2>{escape(card['title'])}</h2>
          <p><strong>Status:</strong> {escape(str(card['status']))}</p>
          <pre>{escape(json.dumps(card.get('data'), indent=2, ensure_ascii=False)[:4000])}</pre>
        </section>
        """)
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>AndyAI Bridge Hub Dashboard Feed</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; background: #f7f7f7; color: #111; }}
    .card {{ background: white; border: 1px solid #ddd; border-radius: 16px; padding: 20px; margin: 16px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }}
    pre {{ overflow:auto; background:#111; color:#f5f5f5; padding:12px; border-radius:12px; }}
  </style>
</head>
<body>
  <h1>AndyAI Bridge Hub Dashboard Feed</h1>
  <p>Generated: {escape(feed['generated_at'])}</p>
  {''.join(cards)}
</body>
</html>
"""
    target.write_text(html)
    return target

def generate_all():
    feed = build_feed()
    json_path = write_json("brain/dashboard/feed/bridge-hub-feed.json", feed)
    md_path = write_markdown("brain/dashboard/reports/bridge-hub-dashboard.md", feed)
    html_path = write_html("brain/dashboard/html/bridge-hub-dashboard.html", feed)
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

def main():
    parser = argparse.ArgumentParser(prog="bridge-feed")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("repo-summary")
    sub.add_parser("pack-status")
    sub.add_parser("doctor-report")
    sub.add_parser("generate-json")
    sub.add_parser("generate-md")
    sub.add_parser("generate-html")
    sub.add_parser("generate-all")
    p_export = sub.add_parser("export")
    p_export.add_argument("--out", default="brain/dashboard/exports/bridge-hub-dashboard-feed.zip")

    args = parser.parse_args()

    if args.command == "repo-summary":
        print(json.dumps(repo_summary(), indent=2, ensure_ascii=False))
    elif args.command == "pack-status":
        print(json.dumps(pack_status(), indent=2, ensure_ascii=False))
    elif args.command == "doctor-report":
        print(json.dumps(doctor_report(), indent=2, ensure_ascii=False))
    elif args.command == "generate-json":
        feed = build_feed()
        path = write_json("brain/dashboard/feed/bridge-hub-feed.json", feed)
        print(json.dumps({"ok": True, "json": rel(path)}, indent=2))
    elif args.command == "generate-md":
        feed = build_feed()
        path = write_markdown("brain/dashboard/reports/bridge-hub-dashboard.md", feed)
        print(json.dumps({"ok": True, "markdown": rel(path)}, indent=2))
    elif args.command == "generate-html":
        feed = build_feed()
        path = write_html("brain/dashboard/html/bridge-hub-dashboard.html", feed)
        print(json.dumps({"ok": True, "html": rel(path)}, indent=2))
    elif args.command == "generate-all":
        print(json.dumps(generate_all(), indent=2, ensure_ascii=False))
    elif args.command == "export":
        print(json.dumps(export_bundle(args.out), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
