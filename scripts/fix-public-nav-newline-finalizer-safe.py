from pathlib import Path
import json
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "public/index.html",
    "public/help/index.html",
    "public/help/print.html",
    "public/knowledge/index.html",
    "public/dialog/index.html",
    "public/capture/index.html",
    "runtime/lib/homepage_builder.py",
    "runtime/lib/brain_dialog.py",
    "runtime/lib/knowledge_front_page.py",
]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def clean_text(text: str) -> str:
    # Remove literal backslash-n tokens that were accidentally rendered in nav/link areas.
    replacements = [
        ('>\\n        <a ', '>\n        <a '),
        ('>\\n      <a ', '>\n      <a '),
        ('>\\n  <a ', '>\n  <a '),
        ('>\\n<a ', '>\n<a '),
        ('>\\\\n        <a ', '>\n        <a '),
        ('>\\\\n      <a ', '>\n      <a '),
        ('>\\\\n  <a ', '>\n  <a '),
        ('>\\\\n<a ', '>\n<a '),
        ('Health \\n Help', 'Health Help'),
        ('Health \\\\n Help', 'Health Help'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)

    # More general cleanup inside nav-like fragments only.
    text = re.sub(r'(Health</a>)\\n(\s*<a\s+href="/help/")', r'\1\n\2', text)
    text = re.sub(r'(Health</a>)\\\\n(\s*<a\s+href="/help/")', r'\1\n\2', text)
    text = re.sub(r'(Help</a>)\\n(\s*<a\s+href="/knowledge/")', r'\1\n\2', text)
    text = re.sub(r'(Help</a>)\\\\n(\s*<a\s+href="/knowledge/")', r'\1\n\2', text)

    return text

def main():
    checked = []
    changed = []
    remaining_nav_hits = []

    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        old = path.read_text(errors="ignore")
        new = clean_text(old)
        checked.append(rel)
        if new != old:
            path.write_text(new)
            changed.append(rel)

    # Verify no visible escaped newline survives around public nav words.
    for rel in ["public/index.html", "public/help/index.html", "public/help/print.html", "public/knowledge/index.html"]:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(errors="ignore")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if "\\n" in line and any(word in line for word in ["Health", "Help", "Knowledge", "Ask Your Brain", "Pricing"]):
                remaining_nav_hits.append({"path": rel, "line": line_no, "text": line[:240]})

    report = {
        "kind": "andyai.second_brain.public_nav_newline_finalizer_safe",
        "generated_at": utc_now(),
        "ok": not remaining_nav_hits,
        "checked": checked,
        "changed": changed,
        "remaining_nav_hits": remaining_nav_hits,
        "rule": "No literal escaped newline tokens may appear in public navigation."
    }

    out = ROOT / "brain/web/reports/public-nav-newline-finalizer-safe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")

    md = ROOT / "brain/web/reports/public-nav-newline-finalizer-safe.md"
    md.write_text(
        "# Public Nav Newline Finalizer-Safe Report\n\n"
        f"- generated_at: `{report['generated_at']}`\n"
        f"- ok: `{report['ok']}`\n"
        f"- checked: `{len(checked)}` files\n"
        f"- changed: `{len(changed)}` files\n"
        f"- remaining_nav_hits: `{len(remaining_nav_hits)}`\n"
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    if remaining_nav_hits:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
