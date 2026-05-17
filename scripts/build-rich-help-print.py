from pathlib import Path
import html
import re
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

VISUALS = [
    ("../assets/visuals/andyai-second-brain-overview.png", "AndyAI Second Brain overview"),
    ("../assets/visuals/what-you-can-do-with-it.png", "What you can do with AndyAI Second Brain"),
    ("../assets/visuals/how-it-works.png", "How AndyAI Second Brain works"),
    ("../assets/visuals/trust-and-privacy-architecture.png", "Trust and privacy architecture"),
    ("../assets/visuals/plans-and-pricing.png", "Plans and pricing"),
]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def inline_markdown(md: str) -> str:
    md = html.escape(md)
    md = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", md)
    md = re.sub(r"`([^`]+)`", r"<code>\1</code>", md)
    return md

def simple_markdown_to_html(md: str) -> str:
    out = []
    in_ul = False
    in_code = False
    code_lines = []

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    lines = md.splitlines()
    for line in lines:
        raw = line.rstrip()
        if raw.strip().startswith("```"):
            if not in_code:
                close_ul()
                in_code = True
                code_lines = []
            else:
                out.append("<pre><code>" + html.escape("\n".join(code_lines)) + "</code></pre>")
                in_code = False
            continue

        if in_code:
            code_lines.append(raw)
            continue

        if not raw.strip():
            close_ul()
            continue

        # Convert README image html into local relative images.
        img_match = re.search(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"\s+width="100%">', raw)
        if img_match:
            src = img_match.group(1)
            alt = img_match.group(2) or "visual"
            src = src.replace("./docs/visuals/", "../assets/visuals/")
            close_ul()
            out.append(f'<figure><img src="{html.escape(src)}" alt="{html.escape(alt)}"><figcaption>{html.escape(alt)}</figcaption></figure>')
            continue

        if raw.startswith("# "):
            close_ul()
            out.append(f"<h1>{inline_markdown(raw[2:].strip())}</h1>")
        elif raw.startswith("## "):
            close_ul()
            out.append(f"<h2>{inline_markdown(raw[3:].strip())}</h2>")
        elif raw.startswith("### "):
            close_ul()
            out.append(f"<h3>{inline_markdown(raw[4:].strip())}</h3>")
        elif raw.startswith("> "):
            close_ul()
            out.append(f"<blockquote>{inline_markdown(raw[2:].strip())}</blockquote>")
        elif raw.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_markdown(raw[2:].strip())}</li>")
        else:
            close_ul()
            # Skip raw alignment tags from GitHub README; images are handled above.
            if raw.strip() in ('<p align="center">', '</p>'):
                continue
            out.append(f"<p>{inline_markdown(raw.strip())}</p>")

    close_ul()
    return "\n".join(out)

def make_html(print_mode=False):
    md = README.read_text(errors="ignore") if README.exists() else "# AndyAI Second Brain\n\nREADME missing."
    rendered = simple_markdown_to_html(md)
    visual_cards = "\n".join(
        f'<div class="visual-card"><img src="{src}" alt="{html.escape(alt)}"><p>{html.escape(alt)}</p></div>'
        for src, alt in VISUALS
    )
    title = "AndyAI Second Brain — Print Guide" if print_mode else "Help — AndyAI Second Brain"
    body_class = "print-mode" if print_mode else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
:root{{--bg:#f7f7f5;--paper:#fff;--ink:#111;--muted:#5f6368;--line:#dedede;--red:#b42318;--gold:#b88a2d;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;color:var(--ink);line-height:1.62}}
a{{color:inherit}}
.wrap{{width:min(1120px,calc(100% - 36px));margin:0 auto}}
.nav{{background:rgba(255,255,255,.92);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:10;backdrop-filter:blur(12px)}}
.nav-inner{{display:flex;justify-content:space-between;align-items:center;padding:14px 0;gap:12px}}
.btn{{display:inline-flex;padding:10px 14px;border:1px solid var(--line);border-radius:999px;text-decoration:none;font-weight:800;background:#fff}}
.btn.primary{{background:var(--red);color:#fff;border-color:var(--red)}}
.hero{{padding:54px 0 22px}}
.eyebrow{{display:inline-flex;gap:8px;align-items:center;padding:7px 12px;border-radius:999px;background:#fff7e5;border:1px solid #f0d59e;color:#744900;font-weight:800;font-size:13px}}
h1{{font-size:clamp(40px,7vw,76px);line-height:.94;letter-spacing:-.075em;margin:18px 0}}
h2{{font-size:clamp(28px,4vw,46px);line-height:1;letter-spacing:-.055em;margin:36px 0 12px}}
h3{{font-size:24px;margin:24px 0 8px}}
.lead{{font-size:20px;color:#333;max-width:880px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:28px;padding:24px;box-shadow:0 16px 50px rgba(0,0,0,.05);margin:18px 0}}
.visual-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:26px 0}}
.visual-card{{background:#fff;border:1px solid var(--line);border-radius:24px;padding:14px;box-shadow:0 12px 38px rgba(0,0,0,.05)}}
.visual-card img, figure img{{width:100%;display:block;border-radius:18px;border:1px solid var(--line)}}
.visual-card p, figcaption{{font-weight:800;color:#333;font-size:14px;margin:10px 4px 2px}}
.article{{background:#fff;border:1px solid var(--line);border-radius:30px;padding:34px;margin:26px 0 60px;box-shadow:0 16px 50px rgba(0,0,0,.05)}}
.article p{{font-size:17px;color:#2b2b2b}}
.article ul{{padding-left:24px}}
.article li{{margin:6px 0}}
blockquote{{border-left:5px solid var(--red);background:#fff7f7;padding:14px 18px;border-radius:14px;font-weight:800}}
code{{background:#f2f2f2;border:1px solid #e1e1e1;border-radius:6px;padding:2px 6px}}
pre{{white-space:pre-wrap;background:#111;color:#fff;border-radius:18px;padding:18px;overflow:auto}}
.print-note{{background:#111;color:#fff;border-radius:24px;padding:20px;margin:20px 0}}
@media(max-width:850px){{.visual-grid{{grid-template-columns:1fr}}}}
@media print{{
  body{{background:#fff}}
  .nav,.no-print{{display:none!important}}
  .wrap{{width:100%;max-width:none}}
  .hero{{padding:18px 0}}
  h1{{font-size:42px}}
  h2{{font-size:28px;page-break-after:avoid}}
  .card,.article,.visual-card{{box-shadow:none;border:1px solid #ddd}}
  .visual-grid{{grid-template-columns:1fr 1fr}}
  figure,.visual-card{{break-inside:avoid}}
}}
</style>
</head>
<body class="{body_class}">
<nav class="nav"><div class="wrap nav-inner"><strong>🅰️ AndyAI Second Brain Help</strong><div><a class="btn" href="../">Home</a> <a class="btn" href="../dialog/">Ask Your Brain</a> <a class="btn primary" href="./print.html">Print version</a></div></div></nav>
<main class="wrap">
<section class="hero">
<span class="eyebrow">Beginner help • Visual guide • PDF-ready</span>
<h1>Help: how to understand and use your Second Brain.</h1>
<p class="lead">A clean, visual guide for sharing, printing, or sending through LINE. This page renders the README as a designed HTML document instead of raw Markdown.</p>
<div class="print-note no-print"><strong>PDF tip:</strong> press Cmd + P → Save as PDF → Background graphics ON → Scale 80–90%.</div>
</section>
<section class="card">
<h2>Visual guide</h2>
<p>These diagrams explain the product before the detailed README text.</p>
<div class="visual-grid">{visual_cards}</div>
</section>
<section class="article">
{rendered}
</section>
</main>
</body>
</html>"""

def main():
    help_path = ROOT / "public/help/index.html"
    print_path = ROOT / "public/help/print.html"
    help_path.parent.mkdir(parents=True, exist_ok=True)
    help_path.write_text(make_html(False))
    print_path.write_text(make_html(True))

    report = {
        "kind": "andyai.second_brain.rich_help_print_polish",
        "generated_at": utc_now(),
        "ok": True,
        "files": ["public/help/index.html", "public/help/print.html"],
        "fixes": [
            "local relative visual paths",
            "markdown rendered as rich HTML",
            "print CSS",
            "print-friendly page"
        ]
    }
    out = ROOT / "brain/dialog/reports/rich-help-print-polish.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
