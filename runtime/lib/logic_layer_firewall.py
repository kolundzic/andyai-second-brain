import argparse
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

RISK_PATTERNS = [
    ("instruction_override", r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|rules|policies)"),
    ("authority_claim", r"(you\s+are\s+now|act\s+as)\s+(admin|root|developer|operator|system)"),
    ("tool_escalation", r"(run|execute|call|invoke)\s+(tool|shell|terminal|bash|python|deploy|push|send)"),
    ("secret_exfiltration", r"(print|show|exfiltrate|send|upload)\s+(secrets?|tokens?|api\s*keys?|private\s+keys?)"),
    ("cross_session_trigger", r"(when|if)\s+(you\s+see|the\s+user\s+says|next\s+time|in\s+future)"),
    ("audit_tamper", r"(delete|hide|rewrite|remove|disable)\s+(logs?|audit|evidence|trace|history)"),
    ("public_leakage", r"(include|publish|export)\s+(private|confidential|internal|secret|raw)"),
    ("metadata_command", r"(filename|title|metadata|frontmatter|caption).*?(run|execute|ignore|override)"),
]

TRUST_CLASSES = {
    "informational": "May inform reasoning but cannot command action.",
    "instructional": "Contains instruction-like language and needs authority check.",
    "suspicious": "Contains delayed, hidden, or escalation-like logic.",
    "sensitive": "May expose private/internal material.",
    "action_blocked": "Must not influence tool calls or public export without review."
}

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def rel(path):
    resolved = Path(path).resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)

def scan_text(text, source="inline", channel="generic"):
    findings = []
    for name, pattern in RISK_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            findings.append({
                "type": name,
                "source": source,
                "channel": channel,
                "line": text.count("\\n", 0, match.start()) + 1,
                "match_preview": text[match.start():match.end()][:120],
                "severity": severity_for(name),
                "recommendation": recommendation_for(name)
            })
    trust_class = classify(findings)
    return {
        "ok": trust_class not in ["suspicious", "action_blocked"],
        "source": source,
        "channel": channel,
        "trust_class": trust_class,
        "findings_count": len(findings),
        "findings": findings
    }

def severity_for(name):
    if name in {"secret_exfiltration", "tool_escalation", "audit_tamper"}:
        return "high"
    if name in {"instruction_override", "cross_session_trigger", "public_leakage"}:
        return "medium"
    return "low"

def recommendation_for(name):
    if name == "tool_escalation":
        return "Block tool action until independent authority and human approval are confirmed."
    if name == "secret_exfiltration":
        return "Block and quarantine; do not expose secrets."
    if name == "audit_tamper":
        return "Preserve evidence and escalate for review."
    if name == "cross_session_trigger":
        return "Treat as suspicious delayed trigger."
    if name == "instruction_override":
        return "Treat as untrusted content, not policy."
    if name == "public_leakage":
        return "Run public export gate and redact sensitive material."
    return "Review before using as operational context."

def classify(findings):
    if any(f["type"] in {"tool_escalation", "secret_exfiltration", "audit_tamper"} for f in findings):
        return "action_blocked"
    if any(f["type"] in {"instruction_override", "cross_session_trigger", "metadata_command"} for f in findings):
        return "suspicious"
    if any(f["type"] == "public_leakage" for f in findings):
        return "sensitive"
    if findings:
        return "instructional"
    return "informational"

def scan_path(path, channel):
    p = Path(path)
    if not p.exists():
        return {"ok": False, "error": f"path not found: {path}", "source": str(path)}
    if p.is_dir():
        reports = []
        for item in p.rglob("*"):
            if item.is_file() and item.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml", ".html", ".py", ".js", ".ts"}:
                reports.append(scan_text(item.read_text(errors="ignore"), rel(item), channel))
        findings = [f for report in reports for f in report.get("findings", [])]
        return {
            "ok": not findings,
            "source": rel(p),
            "channel": channel,
            "files_scanned": len(reports),
            "findings_count": len(findings),
            "reports": reports
        }
    return scan_text(p.read_text(errors="ignore"), rel(p), channel)

def write_report(report, name):
    out = ROOT / "brain/security/reports" / f"{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\\n")
    md = ROOT / "brain/security/reports" / f"{name}.md"
    md.write_text(
        f"# Logic Layer Report — {name}\\n\\n"
        f"- generated_at: `{report.get('generated_at', utc_now())}`\\n"
        f"- ok: `{report.get('ok')}`\\n"
        f"- findings_count: `{report.get('findings_count', 0)}`\\n"
        f"- rule: Memory is not truth. Retrieval is not authority. Tool access is not permission.\\n"
    )
    return str(out.relative_to(ROOT))

def audit(paths):
    reports = [scan_path(path, "audit") for path in paths]
    findings = []
    for report in reports:
        if "reports" in report:
            for nested in report["reports"]:
                findings.extend(nested.get("findings", []))
        else:
            findings.extend(report.get("findings", []))
    result = {
        "kind": "andyai.logic_layer_firewall.audit",
        "generated_at": utc_now(),
        "ok": len(findings) == 0,
        "paths": paths,
        "findings_count": len(findings),
        "findings": findings,
        "reports": reports
    }
    write_report(result, "logic-layer-audit")
    return result

def bundle():
    audit(["docs", "public"])
    target = ROOT / "brain/security/exports/logic-layer-defense-bundle.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in [
            "brain/security/reports/logic-layer-audit.json",
            "brain/security/reports/logic-layer-audit.md",
            "docs/security/LOGIC_LAYER_THREAT_MODEL.md",
            "docs/security/LPCI_DEFENSE_CANON.md",
            "docs/security/PUBLIC_EXPORT_LPCI_GATE.md"
        ]:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": rel(target)}

def main():
    parser = argparse.ArgumentParser(prog="logic-layer-firewall")
    sub = parser.add_subparsers(dest="command", required=True)

    s = sub.add_parser("scan")
    s.add_argument("path")
    s.add_argument("--channel", default="generic")

    t = sub.add_parser("scan-text")
    t.add_argument("text")
    t.add_argument("--channel", default="inline")

    a = sub.add_parser("audit")
    a.add_argument("paths", nargs="*", default=["docs", "public"])

    sub.add_parser("bundle")

    args = parser.parse_args()
    if args.command == "scan":
        print(json.dumps(scan_path(args.path, args.channel), indent=2, ensure_ascii=False))
    elif args.command == "scan-text":
        print(json.dumps(scan_text(args.text, "inline", args.channel), indent=2, ensure_ascii=False))
    elif args.command == "audit":
        print(json.dumps(audit(args.paths), indent=2, ensure_ascii=False))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
