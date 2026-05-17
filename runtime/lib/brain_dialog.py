from pathlib import Path
from datetime import datetime, timezone
import json
import zipfile
import html

ROOT = Path(__file__).resolve().parents[2]

SUPPORTED_TYPES = [
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt", ".md",
    ".png", ".jpg", ".jpeg", ".webp"
]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def asset(name):
    return f"/assets/visuals/{name}"

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return str(target.relative_to(ROOT))

def read_readme():
    p = ROOT / "README.md"
    if not p.exists():
        return "# AndyAI Second Brain\n\nREADME missing."
    return p.read_text(errors="ignore")

def rich_help_html():
    readme = read_readme()
    escaped = html.escape(readme)
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Help — AndyAI Second Brain</title>
<style>
:root{{--bg:#f7f7f5;--paper:#fff;--ink:#111;--muted:#5f6368;--line:#dedede;--red:#b42318;--gold:#b88a2d;}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);line-height:1.6}}
.wrap{{width:min(1120px,calc(100% - 36px));margin:0 auto}}.nav{{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10}}.nav-inner{{display:flex;justify-content:space-between;align-items:center;padding:14px 0;gap:12px}}a{{color:inherit}}.btn{{display:inline-flex;padding:10px 14px;border:1px solid var(--line);border-radius:999px;text-decoration:none;font-weight:800;background:#fff}}.btn.primary{{background:var(--red);color:#fff;border-color:var(--red)}}.hero{{padding:56px 0 24px}}h1{{font-size:clamp(38px,6vw,72px);line-height:.95;letter-spacing:-.07em;margin:16px 0}}.lead{{font-size:20px;color:#333;max-width:850px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0}}.card{{background:#fff;border:1px solid var(--line);border-radius:28px;padding:22px;box-shadow:0 16px 50px rgba(0,0,0,.05)}}img{{width:100%;border-radius:22px;border:1px solid var(--line)}}pre{{white-space:pre-wrap;background:#111;color:#fff;border-radius:24px;padding:20px;overflow:auto}}.chips{{display:flex;gap:8px;flex-wrap:wrap}}.chip{{padding:8px 10px;border-radius:999px;background:#f1f1f1;font-weight:800;font-size:13px}}@media(max-width:850px){{.grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<nav class="nav"><div class="wrap nav-inner"><strong>🅰️ AndyAI Second Brain Help</strong><div><a class="btn" href="/">Home</a> <a class="btn primary" href="/dialog/">Ask Your Brain</a></div></div></nav>
<main class="wrap">
<section class="hero">
<div class="chips"><span class="chip">Beginner help</span><span class="chip">Visual guide</span><span class="chip">README enriched</span></div>
<h1>Help: how to understand and use your Second Brain.</h1>
<p class="lead">This page turns the README into a richer, visual help center for general users. Start here if you want to understand what the product does, why privacy matters, and how the dialog/upload workflow will work.</p>
</section>
<section class="grid">
<div class="card"><img src="{asset('andyai-second-brain-overview.png')}" alt="Overview"></div>
<div class="card"><h2>What is this?</h2><p>AndyAI Second Brain is a governed AI workbench for memory, context, files, questions, reports, privacy checks and safe delivery.</p><div class="chips"><span class="chip">Ask</span><span class="chip">Upload</span><span class="chip">Remember</span><span class="chip">Analyze</span><span class="chip">Deliver</span></div></div>
<div class="card"><img src="{asset('what-you-can-do-with-it.png')}" alt="What you can do"></div>
<div class="card"><img src="{asset('how-it-works.png')}" alt="How it works"></div>
<div class="card"><img src="{asset('trust-and-privacy-architecture.png')}" alt="Trust"></div>
<div class="card"><img src="{asset('plans-and-pricing.png')}" alt="Pricing"></div>
</section>
<section class="card"><h2>Full README text</h2><pre>{escaped}</pre></section>
</main>
</body></html>"""
    return write("public/help/index.html", html_doc)

def dialog_html():
    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ask Your Second Brain</title>
<style>
:root{{--bg:#f7f7f5;--paper:#fff;--ink:#111;--muted:#5f6368;--line:#dedede;--red:#b42318;--gold:#b88a2d;}}
*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(180deg,#fff,var(--bg));font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink)}}.wrap{{width:min(1180px,calc(100% - 36px));margin:0 auto}}.nav{{background:#fff;border-bottom:1px solid var(--line)}}.nav-inner{{display:flex;justify-content:space-between;align-items:center;padding:14px 0}}.btn{{display:inline-flex;padding:10px 14px;border:1px solid var(--line);border-radius:999px;text-decoration:none;font-weight:800;background:#fff;color:#111}}.primary{{background:var(--red);color:#fff;border-color:var(--red)}}h1{{font-size:clamp(38px,7vw,76px);line-height:.95;letter-spacing:-.07em;margin:34px 0 12px}}.lead{{font-size:20px;color:#333;max-width:800px}}.app{{display:grid;grid-template-columns:1.1fr .9fr;gap:18px;margin:28px 0 60px}}.card{{background:#fff;border:1px solid var(--line);border-radius:28px;padding:22px;box-shadow:0 16px 50px rgba(0,0,0,.05)}}.chat{{background:#111;color:#fff;border-radius:28px;padding:18px;min-height:520px}}.bubble{{padding:13px 15px;border-radius:18px;margin:12px 0;max-width:92%}}.user{{background:#fff;color:#111;margin-left:auto}}.brain{{background:#2a2a2a;color:#fff}}.input{{display:flex;gap:10px;margin-top:18px;background:#fff;color:#111;border-radius:18px;padding:12px}}.input span{{flex:1;color:#777}}.upload{{border:2px dashed #cfcfcf;background:#fafafa;border-radius:24px;padding:20px;text-align:center}}.chips{{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}}.chip{{padding:8px 10px;border-radius:999px;background:#f1f1f1;font-weight:800;font-size:13px}}.scan{{background:#111;color:#fff;border-radius:24px;padding:18px;margin-top:14px}}ul{{line-height:1.9;color:#333}}.scan ul{{color:#ddd}}@media(max-width:900px){{.app{{grid-template-columns:1fr}}}}
</style></head>
<body>
<nav class="nav"><div class="wrap nav-inner"><strong>🅰️ Ask Your Second Brain</strong><div><a class="btn" href="/">Home</a> <a class="btn" href="/help/">Help</a></div></div></nav>
<main class="wrap">
<h1>Ask, upload, scan, remember, analyze.</h1>
<p class="lead">This prototype shows the future interaction window where your documents, ideas, notes and questions meet the governed Second Brain.</p>
<div class="app">
<section class="chat">
<div class="bubble user">Upload these invoices and compare them with last month.</div>
<div class="bubble brain">I can read the files, classify them, extract dates and amounts, compare them by month, and prepare a report. Privacy and logic-layer checks apply before export.</div>
<div class="bubble user">Scan this paper contract with my phone camera.</div>
<div class="bubble brain">Camera scan will capture the document, organize it, extract key fields, and attach it to the correct memory/project bucket.</div>
<div class="bubble user">Find everything related to Kurokawa meeting and pricing.</div>
<div class="bubble brain">I can search by meaning, timeline, client, event, topic and previous decision history.</div>
<div class="input"><span>Ask your Second Brain...</span><strong>↵</strong></div>
</section>
<aside class="card">
<h2>Upload zone</h2>
<div class="upload"><strong>Drop files here</strong><br>PDF, Word, Excel, CSV, TXT, images and screenshots</div>
<ul>
<li>Classify by client, project, event or date</li>
<li>Extract summaries and key fields</li>
<li>Compare documents across time</li>
<li>Generate reports and printable outputs</li>
<li>Keep sensitive outputs behind gates</li>
</ul>
<div class="scan">
<h2>📷 Mobile camera scan</h2>
<ul>
<li>Scan paper documents</li>
<li>Capture receipts, contracts and notes</li>
<li>Attach scanned content to memory</li>
<li>Prepare OCR / extraction pipeline later</li>
</ul>
</div>
<div class="chips"><span class="chip">PDF</span><span class="chip">Word</span><span class="chip">Excel</span><span class="chip">Camera</span><span class="chip">Voice soon</span></div>
</aside>
</div>
</main></body></html>"""
    return write("public/dialog/index.html", html_doc)

def capture_html():
    html_doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Camera Scan — AndyAI Second Brain</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif;margin:0;background:#f7f7f5;color:#111}.wrap{width:min(980px,calc(100% - 36px));margin:0 auto;padding:40px 0}.card{background:#fff;border:1px solid #ddd;border-radius:28px;padding:24px;box-shadow:0 16px 50px rgba(0,0,0,.05)}h1{font-size:clamp(38px,7vw,72px);line-height:.95;letter-spacing:-.07em}.phone{border:12px solid #111;border-radius:42px;padding:22px;background:#222;color:#fff;min-height:420px;display:grid;place-items:center;text-align:center}.btn{display:inline-flex;padding:12px 16px;border-radius:999px;background:#b42318;color:#fff;text-decoration:none;font-weight:800}</style></head>
<body><main class="wrap"><a href="/" class="btn">← Home</a><h1>Mobile camera scan preview.</h1><p>Future layer: scan paper documents, receipts, contracts, notes and whiteboards, then attach them to memory for classification, search, analysis and report generation.</p><div class="card"><div class="phone"><div><h2>📷 Scan document</h2><p>Camera capture placeholder</p><p>OCR / extraction / classification comes next.</p></div></div></div></main></body></html>"""
    return write("public/capture/index.html", html_doc)

def update_home_menu():
    p = ROOT / "public/index.html"
    if not p.exists():
        return {"ok": False, "reason": "public/index.html missing"}
    text = p.read_text()
    if 'href="/help/"' not in text:
        text = text.replace('<a href="/health/">Health</a>', '<a href="/health/">Health</a>
        <a href="/help/">Help</a>')
    if 'href="/dialog/"' not in text:
        text = text.replace('<a class="btn dark" href="#dialog">Try the concept</a>', '<a class="btn dark" href="/dialog/">Ask Your Brain</a>')
    if 'href="/capture/"' not in text and "Talk with your 2nd Brain by voice." in text:
        text = text.replace("Talk with your 2nd Brain by voice.", "Talk with your 2nd Brain by voice — and scan documents with mobile camera.")
    p.write_text(text)
    return {"ok": True, "file": "public/index.html"}

def patch_homepage_builder():
    p = ROOT / "runtime/lib/homepage_builder.py"
    if not p.exists():
        return {"ok": False, "reason": "homepage_builder missing"}
    text = p.read_text()
    if 'href="/help/"' not in text:
        text = text.replace('<a href="/health/">Health</a>', '<a href="/health/">Health</a>
        <a href="/help/">Help</a>')
    if 'href="/dialog/"' not in text:
        text = text.replace('<a class="btn dark" href="#dialog">Try the concept</a>', '<a class="btn dark" href="/dialog/">Ask Your Brain</a>')
    p.write_text(text)
    return {"ok": True, "file": "runtime/lib/homepage_builder.py"}

def report():
    result = {
        "kind": "andyai.second_brain.brain_dialog_upload_memory",
        "generated_at": utc_now(),
        "ok": True,
        "pages": ["public/dialog/index.html", "public/help/index.html", "public/capture/index.html"],
        "supported_types": SUPPORTED_TYPES,
        "capabilities": [
            "ask your second brain",
            "upload zone prototype",
            "memory intake model",
            "mobile camera scan preview",
            "pdf word excel processing spec",
            "search sort compare print spec",
            "rich help README HTML"
        ],
        "trust_boundary": "privacy, trust, logic-layer and human approval gates remain required"
    }
    out = ROOT / "brain/dialog/reports/brain-dialog-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\\n")
    md = ROOT / "brain/dialog/reports/brain-dialog-report.md"
    md.write_text("# Brain Dialog Report\\n\\n- Dialog page created.\\n- Upload zone created.\\n- Camera scan preview created.\\n- Rich Help page created from README.\\n- Menu Help link integrated.\\n")
    return result

def build_all():
    dialog_html()
    rich_help_html()
    capture_html()
    update_home_menu()
    patch_homepage_builder()
    return report()

def bundle():
    build_all()
    target = ROOT / "brain/dialog/exports/brain-dialog-upload-memory-pack.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    items = [
        "public/dialog/index.html",
        "public/help/index.html",
        "public/capture/index.html",
        "public/index.html",
        "brain/dialog/reports/brain-dialog-report.json",
        "brain/dialog/reports/brain-dialog-report.md",
        "docs/dialog/BRAIN_DIALOG_SPEC.md",
        "docs/upload/DOCUMENT_UPLOAD_PROCESSING_SPEC.md",
        "docs/capture/MOBILE_CAMERA_SCAN_SPEC.md",
        "docs/help/RICH_HELP_README_HTML_SPEC.md"
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in items:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": str(target.relative_to(ROOT))}

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="brain-dialog")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("help")
    sub.add_parser("dialog")
    sub.add_parser("capture")
    sub.add_parser("report")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build_all(), indent=2))
    elif args.command == "help":
        print(json.dumps({"ok": True, "file": rich_help_html()}, indent=2))
    elif args.command == "dialog":
        print(json.dumps({"ok": True, "file": dialog_html()}, indent=2))
    elif args.command == "capture":
        print(json.dumps({"ok": True, "file": capture_html()}, indent=2))
    elif args.command == "report":
        print(json.dumps(report(), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
