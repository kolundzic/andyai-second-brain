from pathlib import Path
from datetime import datetime, timezone
import json
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def asset(name):
    return f"/assets/visuals/{name}"

def build_homepage():
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>AndyAI Second Brain — Governed AI Memory, Context & Delivery</title>
  <meta name="description" content="AndyAI Second Brain helps you organize AI work, protect privacy, and turn your data, ideas and questions into trusted reports, dashboards and client-ready delivery.">
  <style>
    :root {{
      --bg:#f7f7f5;
      --paper:#ffffff;
      --ink:#111111;
      --muted:#5f6368;
      --line:#dedede;
      --red:#b42318;
      --gold:#b88a2d;
      --soft:#fff7ed;
      --dark:#171717;
    }}
    * {{ box-sizing:border-box; }}
    body {{
      margin:0;
      background:linear-gradient(180deg,#fff 0%,var(--bg) 100%);
      color:var(--ink);
      font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Arial,sans-serif;
      line-height:1.55;
    }}
    a {{ color:inherit; }}
    .wrap {{ width:min(1180px, calc(100% - 36px)); margin:0 auto; }}
    .nav {{
      position:sticky; top:0; z-index:10;
      background:rgba(255,255,255,.86);
      backdrop-filter:blur(12px);
      border-bottom:1px solid var(--line);
    }}
    .nav-inner {{
      display:flex; align-items:center; justify-content:space-between;
      padding:14px 0;
      gap:18px;
    }}
    .brand {{ display:flex; align-items:center; gap:10px; font-weight:800; letter-spacing:-.03em; }}
    .brand-mark {{
      width:34px;height:34px;border-radius:12px;background:var(--dark);color:#fff;
      display:grid;place-items:center;font-weight:900;
    }}
    .nav-links {{ display:flex; gap:16px; flex-wrap:wrap; font-size:14px; color:var(--muted); }}
    .btn {{
      display:inline-flex; align-items:center; justify-content:center; gap:8px;
      padding:12px 18px; border-radius:999px; border:1px solid var(--line);
      text-decoration:none; font-weight:700; background:#fff;
    }}
    .btn.primary {{ background:var(--red); color:#fff; border-color:var(--red); }}
    .btn.dark {{ background:#111;color:#fff;border-color:#111; }}
    .hero {{ padding:76px 0 42px; }}
    .eyebrow {{
      display:inline-flex; gap:8px; align-items:center;
      padding:7px 12px; border:1px solid #f1d4a2; background:#fff8e8; color:#7a4d00;
      border-radius:999px; font-weight:700; font-size:13px;
    }}
    h1 {{ font-size:clamp(42px,8vw,82px); line-height:.94; letter-spacing:-.075em; margin:22px 0 20px; max-width:980px; }}
    .lead {{ font-size:clamp(18px,2.1vw,24px); color:#333; max-width:820px; margin:0 0 28px; }}
    .hero-actions {{ display:flex; gap:12px; flex-wrap:wrap; margin:28px 0; }}
    .hero-grid {{ display:grid; grid-template-columns:1.15fr .85fr; gap:22px; margin-top:34px; align-items:stretch; }}
    .card {{
      background:var(--paper); border:1px solid var(--line); border-radius:28px; padding:24px;
      box-shadow:0 18px 60px rgba(0,0,0,.06);
    }}
    .hero-img {{ width:100%; border-radius:22px; border:1px solid var(--line); display:block; }}
    .panel-title {{ font-size:20px; font-weight:850; margin:0 0 8px; letter-spacing:-.03em; }}
    .chips {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:14px; }}
    .chip {{ padding:8px 10px; background:#f4f4f4; border-radius:999px; font-size:13px; font-weight:700; color:#333; }}
    section {{ padding:52px 0; }}
    .section-head {{ display:flex; align-items:end; justify-content:space-between; gap:20px; margin-bottom:20px; }}
    h2 {{ font-size:clamp(30px,4vw,52px); line-height:1; letter-spacing:-.06em; margin:0; max-width:820px; }}
    .section-copy {{ color:var(--muted); max-width:720px; font-size:17px; }}
    .grid-3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
    .grid-2 {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
    .feature h3,.price h3 {{ margin:0 0 8px; font-size:22px; letter-spacing:-.03em; }}
    .feature p,.price p {{ color:var(--muted); margin:0; }}
    .visual {{ width:100%; border-radius:28px; border:1px solid var(--line); box-shadow:0 18px 60px rgba(0,0,0,.06); background:#fff; }}
    .dialog-shell {{
      background:#111; color:#fff; border-radius:30px; padding:24px;
      display:grid; grid-template-columns:1fr .9fr; gap:18px;
    }}
    .chat {{
      background:#1e1e1e; border:1px solid #333; border-radius:24px; padding:16px;
      min-height:340px;
    }}
    .bubble {{ padding:12px 14px; border-radius:18px; margin:10px 0; max-width:92%; }}
    .bubble.user {{ background:#fff; color:#111; margin-left:auto; }}
    .bubble.brain {{ background:#2d2d2d; color:#fff; }}
    .inputbar {{ margin-top:16px; background:#fff; color:#111; border-radius:18px; padding:12px; display:flex; justify-content:space-between; gap:10px; }}
    .upload-card {{
      border:1px dashed #666; border-radius:22px; padding:18px; background:#171717;
    }}
    .upload-card ul {{ color:#d8d8d8; }}
    .price {{ position:relative; overflow:hidden; }}
    .price.featured {{ border-color:#e4b75d; background:linear-gradient(180deg,#fff,#fff8e8); }}
    .tag {{ display:inline-block; padding:6px 9px; border-radius:999px; background:#111;color:#fff;font-size:12px;font-weight:800;margin-bottom:14px; }}
    .price-number {{ font-size:42px; font-weight:900; letter-spacing:-.05em; margin:10px 0; }}
    .price ul {{ padding-left:20px; color:#333; }}
    .quote {{
      background:#111; color:#fff; border-radius:30px; padding:32px;
      font-size:clamp(24px,4vw,46px); line-height:1.05; letter-spacing:-.055em; font-weight:850;
    }}
    .footer {{ padding:44px 0; color:var(--muted); border-top:1px solid var(--line); }}
    @media (max-width:900px) {{
      .hero-grid,.dialog-shell,.grid-3,.grid-2 {{ grid-template-columns:1fr; }}
      .nav-links {{ display:none; }}
      section {{ padding:38px 0; }}
    }}
  </style>
</head>
<body>
  <nav class="nav">
    <div class="wrap nav-inner">
      <div class="brand"><div class="brand-mark">🅰️</div><span>AndyAI Second Brain</span></div>
      <div class="nav-links">
        <a href="#what">What it does</a>
        <a href="#dialog">Ask your Brain</a>
        <a href="#trust">Trust</a>
        <a href="#pricing">Pricing</a>
        <a href="/health/">Health</a>\n        <a href="/help/">Help</a>
      </div>
      <a class="btn primary" href="#pricing">Start now</a>
    </div>
  </nav>

  <main>
    <section class="hero">
      <div class="wrap">
        <span class="eyebrow">🧠 Governed AI memory • context • delivery</span>
        <h1>Your AI workbench for memory, ideas, files and trusted delivery.</h1>
        <p class="lead">AndyAI Second Brain helps you talk with your data, organize project knowledge, ask better questions, create reports, protect privacy, and publish only what is approved.</p>
        <div class="hero-actions">
          <a class="btn primary" href="#pricing">Choose a plan</a>
          <a class="btn dark" href="/dialog/">Ask Your Brain</a>
          <a class="btn" href="/trust/">See trust layer</a>
        </div>
        <div class="hero-grid">
          <div class="card">
            <img class="hero-img" src="{asset('andyai-second-brain-overview.png')}" alt="AndyAI Second Brain overview">
          </div>
          <div class="card">
            <p class="panel-title">What this means in plain language</p>
            <p>You bring chats, notes, files, plans and messy ideas. Second Brain organizes them into usable context, prepares AI work, checks risk, and helps deliver clean results as pages, reports, dashboards or client artifacts.</p>
            <div class="chips">
              <span class="chip">Less chaos</span>
              <span class="chip">Better memory</span>
              <span class="chip">Safer output</span>
              <span class="chip">Client-ready</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="what">
      <div class="wrap">
        <div class="section-head">
          <div>
            <h2>What can you do with it?</h2>
            <p class="section-copy">Use it as a personal AI operating desk: remember, search, sort, compare, analyze, print, publish and prepare your next action.</p>
          </div>
        </div>
        <img class="visual" src="{asset('what-you-can-do-with-it.png')}" alt="What you can do with AndyAI Second Brain">
        <div class="grid-3" style="margin-top:18px">
          <div class="card feature"><h3>Organize knowledge</h3><p>Keep chats, notes, files and project context from disappearing into scattered tools.</p></div>
          <div class="card feature"><h3>Analyze and compare</h3><p>Ask questions across time, events, topics, documents and decisions.</p></div>
          <div class="card feature"><h3>Deliver safely</h3><p>Turn raw AI output into reports, client pages and approved public surfaces.</p></div>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <h2>From request to verified outcome.</h2>
        <p class="section-copy">The system guides work through context, memory, agent preparation, generation, checks and delivery.</p>
        <img class="visual" src="{asset('how-it-works.png')}" alt="How AndyAI Second Brain works">
      </div>
    </section>

    <section id="dialog">
      <div class="wrap">
        <h2>Ask Your Second Brain.</h2>
        <p class="section-copy">This is the next interaction model: write a question, upload a file, ask for memory, request analysis, compare old notes, generate a report, or prepare a client delivery package.</p>
        <div class="dialog-shell">
          <div class="chat">
            <div class="bubble user">Find everything we discussed about pricing, privacy and client delivery.</div>
            <div class="bubble brain">I found pricing docs, trust notes, launch evidence, and public pages. I can summarize, compare versions, or prepare a client-ready report.</div>
            <div class="bubble user">Prepare a simple report for a beginner client.</div>
            <div class="bubble brain">Drafting a clear report with context, key decisions, safety notes, and next steps. Privacy gate required before sharing.</div>
            <div class="inputbar"><span>Ask your Second Brain...</span><strong>↵</strong></div>
          </div>
          <div class="upload-card">
            <h3>Upload + remember + process</h3>
            <p>Bring your files and ideas into one governed workspace.</p>
            <ul>
              <li>Upload notes, PDFs, reports and screenshots</li>
              <li>Sort by project, time, client or event</li>
              <li>Search by meaning, not just filename</li>
              <li>Compare versions and decisions</li>
              <li>Generate printable or web-ready reports</li>
              <li>Prepare future voice interaction</li>
            </ul>
            <div class="chips">
              <span class="chip">📎 Upload</span>
              <span class="chip">🔎 Search</span>
              <span class="chip">🧠 Remember</span>
              <span class="chip">🗣️ Voice soon</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="trust">
      <div class="wrap">
        <h2>Trust is the product boundary.</h2>
        <p class="section-copy">Second Brain does not treat memory as truth, retrieval as authority, or tool access as permission. Public output must pass privacy, trust, logic-layer and human approval gates.</p>
        <img class="visual" src="{asset('trust-and-privacy-architecture.png')}" alt="Trust and privacy architecture">
        <div class="quote" style="margin-top:18px">Machine output is not automatically safe. Safe output passed privacy, trust, logic-layer and human approval gates.</div>
      </div>
    </section>

    <section id="pricing">
      <div class="wrap">
        <h2>Plans built for real AI work.</h2>
        <p class="section-copy">Start as an individual. Grow into consultant delivery. Expand into agency or team operations.</p>
        <img class="visual" src="{asset('plans-and-pricing.png')}" alt="Plans and pricing">
        <div class="grid-3" style="margin-top:18px">
          <div class="card price">
            <span class="tag">Starter</span>
            <h3>Personal AI memory</h3>
            <div class="price-number">$19/mo</div>
            <ul><li>1 workspace</li><li>Personal memory vault</li><li>Context assembly</li><li>Basic client report</li><li>Manual approval</li></ul>
            <a class="btn" href="mailto:kolundzic@gmail.com?subject=AndyAI%20Second%20Brain%20Starter">Start Starter</a>
          </div>
          <div class="card price featured">
            <span class="tag">Most popular</span>
            <h3>Pro delivery</h3>
            <div class="price-number">$79/mo</div>
            <ul><li>5 workspaces</li><li>Advanced memory + skills</li><li>Client report pages</li><li>Privacy firewall</li><li>Audit trail</li></ul>
            <a class="btn primary" href="mailto:kolundzic@gmail.com?subject=AndyAI%20Second%20Brain%20Pro">Start Pro</a>
          </div>
          <div class="card price">
            <span class="tag">Business</span>
            <h3>Team operations</h3>
            <div class="price-number">$249/mo</div>
            <ul><li>Multi-client delivery</li><li>Operator registry</li><li>Approval workflows</li><li>Team collaboration</li><li>Launch assistance</li></ul>
            <a class="btn" href="mailto:kolundzic@gmail.com?subject=AndyAI%20Second%20Brain%20Business">Talk Business</a>
          </div>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="card">
          <h2>Talk with your 2nd Brain by voice.</h2>
          <p class="section-copy">Voice interaction is planned as a natural next layer: ask questions, recall memory, create summaries, prepare reports and control workflows by speaking. First voice preview will come after the web dialog layer.</p>
          <div class="chips">
            <span class="chip">🎙️ Voice preview planned</span>
            <span class="chip">🧠 Memory conversation</span>
            <span class="chip">📄 Voice-to-report</span>
            <span class="chip">✅ Approval before action</span>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <div class="wrap">
      <strong>AndyAI Second Brain</strong><br>
      Public doorway: brain.andyai.ai. Built for governed AI memory, context and delivery.
    </div>
  </footer>
</body>
</html>"""
    out = ROOT / "public/index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)
    return {"ok": True, "file": str(out.relative_to(ROOT)), "generated_at": utc_now()}

def report():
    result = {
        "kind": "andyai.second_brain.homepage_conversion",
        "generated_at": utc_now(),
        "ok": True,
        "homepage": "public/index.html",
        "sections": [
            "hero",
            "visual story",
            "what you can do",
            "how it works",
            "ask your second brain",
            "upload and memory zone",
            "voice preview",
            "trust",
            "pricing",
            "cta"
        ],
        "routes": [
            "/",
            "/client/",
            "/client-portal/",
            "/trust/",
            "/faq/",
            "/health/"
        ]
    }
    out = ROOT / "brain/web/reports/homepage-conversion-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / "brain/web/reports/homepage-conversion-report.md"
    md.write_text("# Homepage Conversion Report\n\n- Public homepage rebuilt.\n- Visuals embedded.\n- Pricing embedded.\n- Ask Your Second Brain mock embedded.\n- Upload and voice preview embedded.\n")
    return result

def bundle():
    build_homepage()
    report()
    target = ROOT / "brain/web/exports/homepage-conversion-pack.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    items = [
        "public/index.html",
        "brain/web/reports/homepage-conversion-report.json",
        "brain/web/reports/homepage-conversion-report.md",
        "docs/web/HOMEPAGE_CONVERSION_SPEC.md",
        "docs/dialog/ASK_YOUR_SECOND_BRAIN_SPEC.md",
        "docs/voice/TALK_WITH_YOUR_SECOND_BRAIN_PREVIEW.md",
        "docs/conversion/SUBSCRIPTION_CONVERSION_COPY.md"
    ]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in items:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": str(target.relative_to(ROOT))}

def main():
    import argparse
    parser = argparse.ArgumentParser(prog="homepage-builder")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("build")
    sub.add_parser("report")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "build":
        print(json.dumps(build_homepage(), indent=2))
    elif args.command == "report":
        print(json.dumps(report(), indent=2))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2))

if __name__ == "__main__":
    main()
