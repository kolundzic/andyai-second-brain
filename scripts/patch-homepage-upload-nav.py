from pathlib import Path
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "public/index.html",
    "runtime/lib/homepage_builder.py",
    "runtime/lib/protected_app_shell.py",
    "runtime/lib/upload_intake.py"
]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def add_upload_link(text: str) -> str:
    if 'href="/upload/"' in text:
        return text

    patterns = [
        ('<a href="/app/">App</a>', '<a href="/app/">App</a>\n        <a href="/upload/">Upload</a>'),
        ('<a href="/login/">Login</a>', '<a href="/upload/">Upload</a>\n        <a href="/login/">Login</a>'),
        ('<a href="/dialog/">Ask Your Brain</a>', '<a href="/dialog/">Ask Your Brain</a>\n        <a href="/upload/">Upload</a>'),
        ('<a class="btn" href="/dialog/">Ask Your Brain</a>', '<a class="btn" href="/dialog/">Ask Your Brain</a> <a class="btn" href="/upload/">Upload</a>'),
        ('<a class="btn dark" href="/dialog/">Ask Your Brain</a>', '<a class="btn dark" href="/dialog/">Ask Your Brain</a> <a class="btn" href="/upload/">Upload</a>')
    ]
    for old, new in patterns:
        if old in text:
            return text.replace(old, new, 1)

    # Fallback: add before closing nav/div if obvious.
    if "</nav>" in text:
        return text.replace("</nav>", '<a href="/upload/">Upload</a></nav>', 1)
    return text

def main():
    changed = []
    checked = []

    for rel in TARGETS:
        path = ROOT / rel
        if not path.exists():
            continue
        old = path.read_text(errors="ignore")
        new = add_upload_link(old)
        checked.append(rel)
        if new != old:
            path.write_text(new)
            changed.append(rel)

    public_index = ROOT / "public/index.html"
    if public_index.exists():
        text = public_index.read_text(errors="ignore")
        if 'href="/upload/"' not in text:
            raise SystemExit("Upload link missing from public/index.html after patch")

    report = {
        "kind": "andyai.second_brain.homepage_upload_nav_link_patch",
        "generated_at": utc_now(),
        "ok": True,
        "checked": checked,
        "changed": changed,
        "route": "/upload/",
        "rule": "Homepage navigation must expose Upload after PACK44."
    }
    out = ROOT / "brain/web/reports/homepage-upload-nav-link-patch.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
