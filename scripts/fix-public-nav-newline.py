from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "public/index.html",
    "public/help/index.html",
    "public/help/print.html",
    "public/knowledge/index.html",
    "runtime/lib/homepage_builder.py",
    "runtime/lib/brain_dialog.py",
    "runtime/lib/knowledge_front_page.py",
]

REPLACEMENTS = {
    "\\n": "\n",
    "\\\\n": "\n",
}

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def clean_text(text: str) -> str:
    # Target only escaped newline tokens that appear in rendered/generated HTML strings.
    text = text.replace('>\\n        <a ', '>\n        <a ')
    text = text.replace('>\\n  <a ', '>\n  <a ')
    text = text.replace('>\\n<a ', '>\n<a ')
    text = text.replace('>\\\\n        <a ', '>\n        <a ')
    text = text.replace('>\\\\n  <a ', '>\n  <a ')
    text = text.replace('>\\\\n<a ', '>\n<a ')
    return text

def main():
    changed = []
    checked = []

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

    # Hard assertion: literal escaped newline must not appear near public nav links.
    public_index = ROOT / "public/index.html"
    if public_index.exists():
        text = public_index.read_text(errors="ignore")
        bad_markers = ["\\n        <a href=\"/help/\"", "\\\\n        <a href=\"/help/\"", "\\n  <a href=\"/help/\""]
        found = [m for m in bad_markers if m in text]
        if found:
            raise SystemExit(f"escaped newline still found in public/index.html: {found}")

    report = {
        "kind": "andyai.second_brain.public_nav_newline_cleanup",
        "generated_at": utc_now(),
        "ok": True,
        "checked": checked,
        "changed": changed,
        "rule": "Public navigation must not display escaped newline tokens such as \\n."
    }

    out = ROOT / "brain/web/reports/public-nav-newline-cleanup.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
