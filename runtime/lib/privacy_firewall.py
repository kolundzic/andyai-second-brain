import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SECRET_PATTERNS = [
    ("private_key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("password_assignment", r"(?i)\b(password|passwd|pwd)\s*[:=]\s*['\"]?[^'\"\s]{6,}"),
    ("api_key_assignment", r"(?i)\b(api[_-]?key|apikey)\s*[:=]\s*['\"]?[^'\"\s]{6,}"),
    ("token_assignment", r"(?i)\b(token|access_token|refresh_token)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    ("secret_assignment", r"(?i)\b(secret|client_secret|service_role)\s*[:=]\s*['\"]?[^'\"\s]{6,}"),
]
PII_PATTERNS = [
    ("email", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ("phone_like", r"\b(?:\+?\d[\d\-\s().]{7,}\d)\b"),
    ("credit_card_like", r"\b(?:\d[ -]*?){13,16}\b"),
]
CLIENT_MARKERS = [
    ("client_confidential_marker", r"(?i)\b(confidential|private client|client secret|NDA|do not share|internal only)\b"),
    ("raw_conversation_marker", r"(?i)\b(raw conversation|chat transcript|unredacted prompt|private prompt)\b"),
]

# Narrow false-positive allowlist.
# This is Git SSH remote metadata, not a personal email.
ALLOWLIST_EXACT_MATCHES = {
    "git@github.com"
}


DEFAULT_SCAN_DIRS = ["public", "brain/client", "brain/vercel", "docs", "examples"]
EXCLUDE_PARTS = {".git", "node_modules", "__pycache__", ".next", "dist", "build"}
BINARY_SUFFIXES = {".zip", ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ico", ".webp"}

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def rel(path):
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)

def read_text(path):
    return Path(path).read_text(errors="replace")

def is_allowlisted_match(group, name, value):
    if value in ALLOWLIST_EXACT_MATCHES:
        return True
    return False

def should_skip(path):
    p = Path(path)
    if any(part in EXCLUDE_PARTS for part in p.parts):
        return True
    if p.suffix.lower() in BINARY_SUFFIXES:
        return True
    return False

def iter_files(paths):
    out = []
    for item in paths:
        base = ROOT / item if not Path(item).is_absolute() else Path(item)
        if not base.exists():
            continue
        if base.is_file() and not should_skip(base):
            out.append(base)
        elif base.is_dir():
            for path in base.rglob("*"):
                if path.is_file() and not should_skip(path):
                    out.append(path)
    return sorted(set(out))

def scan_file(path):
    path = Path(path)
    text = read_text(path)
    findings = []
    for group, patterns in [("secret", SECRET_PATTERNS), ("pii", PII_PATTERNS), ("client_data", CLIENT_MARKERS)]:
        for name, pattern in patterns:
            for m in re.finditer(pattern, text):
                value = text[m.start():m.end()]
                if is_allowlisted_match(group, name, value):
                    continue
                findings.append({
                    "group": group,
                    "type": name,
                    "path": rel(path),
                    "line": text.count("\n", 0, m.start()) + 1,
                    "match_preview": value[:80]
                })
    return findings

def scan_paths(paths):
    files = iter_files(paths)
    findings = []
    for path in files:
        findings.extend(scan_file(path))
    return {
        "ok": len(findings) == 0,
        "scanned_at": utc_now(),
        "paths": paths,
        "files_scanned": len(files),
        "findings_count": len(findings),
        "findings": findings
    }

def classify_file(path):
    target = ROOT / path if not Path(path).is_absolute() else Path(path)
    findings = scan_file(target)
    groups = {f["group"] for f in findings}
    if "secret" in groups:
        classification = "secret"
    elif "pii" in groups or "client_data" in groups:
        classification = "confidential"
    elif "public" in rel(target).split("/"):
        classification = "public_candidate"
    else:
        classification = "internal"
    return {
        "path": rel(target),
        "classification": classification,
        "findings_count": len(findings),
        "findings": findings
    }

def redact_file(src, dst=None):
    source = ROOT / src if not Path(src).is_absolute() else Path(src)
    text = read_text(source)
    redacted = text
    for name, pattern in SECRET_PATTERNS + PII_PATTERNS + CLIENT_MARKERS:
        redacted = re.sub(pattern, f"[REDACTED:{name}]", redacted)
    if dst:
        target = ROOT / dst if not Path(dst).is_absolute() else Path(dst)
    else:
        target = ROOT / "brain/privacy/redacted" / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(redacted)
    return {"ok": True, "source": rel(source), "redacted": rel(target)}

def quarantine_file(src):
    source = ROOT / src if not Path(src).is_absolute() else Path(src)
    target = ROOT / "brain/privacy/quarantine" / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {"ok": True, "source": rel(source), "quarantine": rel(target)}

def git_tracked_files():
    try:
        result = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True)
        return [x for x in result.stdout.splitlines() if x.strip()]
    except Exception:
        return []

def scan_git_tracked():
    return scan_paths(git_tracked_files())

def public_gate():
    result = scan_paths(["public"])
    # Public output must not include secrets, PII or client confidentiality markers.
    return result

def audit():
    public = public_gate()
    docs_examples = scan_paths(DEFAULT_SCAN_DIRS)
    audit_obj = {
        "kind": "andyai.privacy_audit",
        "generated_at": utc_now(),
        "public_gate": public,
        "general_scan": docs_examples,
        "rules": [
            "No client data in GitHub.",
            "No secrets in GitHub.",
            "No raw evidence in public.",
            "No public report without human approval.",
            "No Supabase table without RLS.",
            "No deployment without privacy gate."
        ]
    }
    out = ROOT / "brain/privacy/audit/privacy-audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_obj, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / "brain/privacy/reports/privacy-audit.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(
        "# Privacy Audit Report\n\n"
        f"Generated: {audit_obj['generated_at']}\n\n"
        f"- Public gate findings: {public['findings_count']}\n"
        f"- General scan findings: {docs_examples['findings_count']}\n\n"
        "## Trust Rules\n\n" +
        "\n".join([f"- {rule}" for rule in audit_obj["rules"]]) + "\n"
    )
    return {"ok": public["ok"], "json": rel(out), "markdown": rel(md), "public_findings": public["findings_count"], "general_findings": docs_examples["findings_count"]}

def generate_hook(path="scripts/pre-commit-privacy-guard.sh"):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("""#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
runtime/bin/privacy-firewall public-gate >/tmp/andyai-precommit-privacy-gate.log
echo "privacy pre-commit guard passed"
""")
    target.chmod(0o755)
    return {"ok": True, "hook": rel(target)}

def safe_export(path="brain/privacy/exports/public-safe-privacy-export.zip"):
    aud = audit()
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in ["brain/privacy/audit/privacy-audit.json", "brain/privacy/reports/privacy-audit.md", "docs/privacy/TRUST_BOUNDARY_CANON.md", "docs/pack29/PRIVACY_FIREWALL_RUNBOOK.md"]:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "audit_ok": aud["ok"], "export": rel(target)}

def main():
    parser = argparse.ArgumentParser(prog="privacy-firewall")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan")
    p_scan.add_argument("paths", nargs="*", default=DEFAULT_SCAN_DIRS)

    p_classify = sub.add_parser("classify")
    p_classify.add_argument("path")

    p_redact = sub.add_parser("redact")
    p_redact.add_argument("source")
    p_redact.add_argument("--out", default=None)

    p_quarantine = sub.add_parser("quarantine")
    p_quarantine.add_argument("source")

    sub.add_parser("scan-git")
    sub.add_parser("public-gate")
    sub.add_parser("audit")
    sub.add_parser("generate-hook")
    p_export = sub.add_parser("safe-export")
    p_export.add_argument("--out", default="brain/privacy/exports/public-safe-privacy-export.zip")

    args = parser.parse_args()

    if args.command == "scan":
        print(json.dumps(scan_paths(args.paths), indent=2, ensure_ascii=False))
    elif args.command == "classify":
        print(json.dumps(classify_file(args.path), indent=2, ensure_ascii=False))
    elif args.command == "redact":
        print(json.dumps(redact_file(args.source, args.out), indent=2, ensure_ascii=False))
    elif args.command == "quarantine":
        print(json.dumps(quarantine_file(args.source), indent=2, ensure_ascii=False))
    elif args.command == "scan-git":
        print(json.dumps(scan_git_tracked(), indent=2, ensure_ascii=False))
    elif args.command == "public-gate":
        result = public_gate()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["ok"] else 1)
    elif args.command == "audit":
        print(json.dumps(audit(), indent=2, ensure_ascii=False))
    elif args.command == "generate-hook":
        print(json.dumps(generate_hook(), indent=2, ensure_ascii=False))
    elif args.command == "safe-export":
        print(json.dumps(safe_export(args.out), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
