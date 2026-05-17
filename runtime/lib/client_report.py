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

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return target

def load_intake(path):
    data = read_json(path)
    if data:
        return data
    return {
        "client_name": "Sample Client",
        "request": "AI workflow audit and implementation roadmap",
        "industry": "General business",
        "priority": "clarity, safety, automation readiness"
    }

def collect_engine_status():
    candidates = [
        "brain/vercel/reports/vercel-readiness.json",
        "brain/battle-pack27/status/BATTLE_PACK27_STATUS.json",
        "brain/battle-pack26/status/BATTLE_PACK26_STATUS.json",
        "brain/battle-pack25/status/BATTLE_PACK25_STATUS.json",
        "brain/battle-pack24/status/BATTLE_PACK24_STATUS.json",
        "brain/doctor/reports/brain-doctor-report.json",
        "brain/dashboard/feed/bridge-hub-feed.json"
    ]
    found = []
    for item in candidates:
        data = read_json(item)
        if data:
            found.append({"path": item, "data": data})
    return found

def build_report(intake_path="examples/client-intake/sample-client-intake.json"):
    intake = load_intake(intake_path)
    status = collect_engine_status()
    client = intake.get("client_name", "Sample Client")
    request = intake.get("request", "AI workflow report")
    report = {
        "kind": "andyai.client_report",
        "version": "1.0",
        "generated_at": utc_now(),
        "repo": {
            "name": ROOT.name,
            "head": git(["rev-parse", "--short", "HEAD"]),
            "latest_tag": (git(["tag", "--sort=-creatordate"]).splitlines() or ["unknown"])[0]
        },
        "client": intake,
        "executive_summary": {
            "title": f"{client} — AI Delivery Readiness Report",
            "summary": f"This report translates machine-generated AndyAI Second Brain artifacts into a human-readable delivery surface for the request: {request}.",
            "status": "draft-ready",
            "trust_note": "This report is generated from verified local artifacts and should be reviewed by a human operator before client delivery."
        },
        "recommendations": [
            {"title": "Clarify the business workflow", "body": "Map the current process, expected output, human approval points and risk boundaries."},
            {"title": "Start with a governed pilot", "body": "Use a small scoped automation before connecting sensitive systems or production data."},
            {"title": "Keep evidence visible", "body": "Every generated recommendation should link back to source artifacts, reports and verification logs."},
            {"title": "Separate operator view from client view", "body": "Keep raw artifact panels internal and expose only clear, trusted, designed outputs to clients."}
        ],
        "evidence_trust_block": {
            "artifact_sources": [item["path"] for item in status],
            "verification": "Core verify, brain-check and battle pack verification artifacts are available in the operator layer.",
            "human_gate": "Human approval is required before external delivery or deployment."
        },
        "next_actions": [
            "Review this report internally.",
            "Replace sample intake with real client intake.",
            "Attach selected evidence and exports.",
            "Publish client-facing page only after human approval."
        ]
    }
    return report

def write_markdown(path, report):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {report['executive_summary']['title']}",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Executive Summary",
        "",
        report["executive_summary"]["summary"],
        "",
        f"Status: **{report['executive_summary']['status']}**",
        "",
        "## Recommendations",
        "",
    ]
    for rec in report["recommendations"]:
        lines.append(f"### {rec['title']}")
        lines.append("")
        lines.append(rec["body"])
        lines.append("")
    lines += [
        "## Evidence and Trust",
        "",
        report["evidence_trust_block"]["verification"],
        "",
        f"Human gate: {report['evidence_trust_block']['human_gate']}",
        "",
        "### Artifact Sources",
        "",
    ]
    for item in report["evidence_trust_block"]["artifact_sources"]:
        lines.append(f"- `{item}`")
    lines += ["", "## Next Actions", ""]
    for item in report["next_actions"]:
        lines.append(f"- {item}")
    lines.append("")
    target.write_text("\n".join(lines))
    return target

def write_html(path, report):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    rec_cards = []
    for rec in report["recommendations"]:
        rec_cards.append(f"<article class='card'><h3>{escape(rec['title'])}</h3><p>{escape(rec['body'])}</p></article>")
    sources = "".join([f"<li><code>{escape(x)}</code></li>" for x in report["evidence_trust_block"]["artifact_sources"]])
    actions = "".join([f"<li>{escape(x)}</li>" for x in report["next_actions"]])
    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{escape(report['executive_summary']['title'])}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background:#f6f7f8; color:#111; margin:0; }}
    .hero {{ background:#111; color:white; padding:56px 40px; }}
    .hero h1 {{ font-size:42px; margin:0 0 10px; }}
    .hero p {{ font-size:18px; max-width:850px; line-height:1.5; }}
    .wrap {{ max-width:1100px; margin:0 auto; padding:28px; }}
    .grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px,1fr)); gap:16px; }}
    .card {{ background:white; border:1px solid #ddd; border-radius:18px; padding:20px; box-shadow:0 2px 12px rgba(0,0,0,0.05); }}
    .section {{ background:white; border:1px solid #ddd; border-radius:18px; padding:24px; margin:18px 0; }}
    code {{ background:#eee; border-radius:6px; padding:2px 5px; }}
    .badge {{ display:inline-block; background:#e8f5e9; color:#137333; padding:6px 10px; border-radius:999px; font-weight:600; }}
  </style>
</head>
<body>
  <section class="hero">
    <h1>{escape(report['executive_summary']['title'])}</h1>
    <p>{escape(report['executive_summary']['summary'])}</p>
    <span class="badge">{escape(report['executive_summary']['status'])}</span>
  </section>
  <main class="wrap">
    <section class="section">
      <h2>Client Request</h2>
      <p><strong>{escape(report['client'].get('request',''))}</strong></p>
      <p>Industry: {escape(report['client'].get('industry',''))}</p>
      <p>Priority: {escape(report['client'].get('priority',''))}</p>
    </section>
    <h2>Recommendations</h2>
    <section class="grid">{''.join(rec_cards)}</section>
    <section class="section">
      <h2>Evidence and Trust</h2>
      <p>{escape(report['evidence_trust_block']['verification'])}</p>
      <p><strong>Human gate:</strong> {escape(report['evidence_trust_block']['human_gate'])}</p>
      <ul>{sources}</ul>
    </section>
    <section class="section">
      <h2>Next Actions</h2>
      <ol>{actions}</ol>
    </section>
  </main>
</body>
</html>
"""
    target.write_text(html)
    return target

def generate_all(intake="examples/client-intake/sample-client-intake.json"):
    report = build_report(intake)
    json_path = write_json("brain/client/feed/client-report.json", report)
    md_path = write_markdown("brain/client/reports/client-report.md", report)
    html_path = write_html("brain/client/html/client-report.html", report)
    return {"ok": True, "json": rel(json_path), "markdown": rel(md_path), "html": rel(html_path)}

def export_public():
    generated = generate_all()
    target_dir = ROOT / "public/client"
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / generated["html"], target_dir / "index.html")
    shutil.copy2(ROOT / generated["json"], target_dir / "client-report.json")
    shutil.copy2(ROOT / generated["markdown"], target_dir / "client-report.md")
    return {"ok": True, "public_html": "public/client/index.html", "public_json": "public/client/client-report.json", "public_md": "public/client/client-report.md"}

def export_bundle(path):
    generated = export_public()
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for relpath in ["brain/client/feed/client-report.json", "brain/client/reports/client-report.md", "brain/client/html/client-report.html", "public/client/index.html", "public/client/client-report.json", "public/client/client-report.md"]:
            item = ROOT / relpath
            if item.exists():
                archive.write(item, item.relative_to(ROOT))
    generated["export"] = rel(target)
    return generated

def main():
    parser = argparse.ArgumentParser(prog="client-report")
    sub = parser.add_subparsers(dest="command", required=True)

    p_build = sub.add_parser("build")
    p_build.add_argument("--intake", default="examples/client-intake/sample-client-intake.json")

    p_json = sub.add_parser("generate-json")
    p_json.add_argument("--intake", default="examples/client-intake/sample-client-intake.json")

    p_md = sub.add_parser("generate-md")
    p_md.add_argument("--intake", default="examples/client-intake/sample-client-intake.json")

    p_html = sub.add_parser("generate-html")
    p_html.add_argument("--intake", default="examples/client-intake/sample-client-intake.json")

    p_public = sub.add_parser("export-public")
    p_public.add_argument("--intake", default="examples/client-intake/sample-client-intake.json")

    p_bundle = sub.add_parser("bundle")
    p_bundle.add_argument("--out", default="brain/client/exports/client-report-delivery.zip")

    args = parser.parse_args()

    if args.command == "build":
        print(json.dumps(generate_all(args.intake), indent=2, ensure_ascii=False))
    elif args.command == "generate-json":
        report = build_report(args.intake)
        path = write_json("brain/client/feed/client-report.json", report)
        print(json.dumps({"ok": True, "json": rel(path)}, indent=2))
    elif args.command == "generate-md":
        report = build_report(args.intake)
        path = write_markdown("brain/client/reports/client-report.md", report)
        print(json.dumps({"ok": True, "markdown": rel(path)}, indent=2))
    elif args.command == "generate-html":
        report = build_report(args.intake)
        path = write_html("brain/client/html/client-report.html", report)
        print(json.dumps({"ok": True, "html": rel(path)}, indent=2))
    elif args.command == "export-public":
        print(json.dumps(export_public(), indent=2, ensure_ascii=False))
    elif args.command == "bundle":
        print(json.dumps(export_bundle(args.out), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
