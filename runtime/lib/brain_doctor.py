import argparse
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def rel(path):
    return str(path.relative_to(ROOT))

def find_files(folder, suffixes):
    base = ROOT / folder
    if not base.exists():
        return []
    out = []
    for path in base.rglob("*"):
        if path.is_file() and path.suffix.lower() in suffixes:
            out.append(path)
    return sorted(out)

def json_validate(path):
    target = Path(path)
    if not target.is_absolute():
        target = ROOT / target
    try:
        data = json.loads(target.read_text())
        return {"path": rel(target), "ok": True, "type": type(data).__name__}
    except Exception as exc:
        return {"path": str(path), "ok": False, "error": str(exc)}

def scan_schemas():
    files = find_files("schemas", {".json"})
    valid = []
    invalid = []
    for item in files:
        result = json_validate(item)
        if result["ok"]:
            valid.append(result)
        else:
            invalid.append(result)
    return {"count": len(files), "valid": len(valid), "invalid": len(invalid), "invalid_items": invalid}

def scan_reports():
    files = []
    for folder in ["brain/reports", "docs", "release-notes"]:
        files.extend(find_files(folder, {".md"}))
    return {"count": len(files), "sample": [rel(x) for x in files[:20]]}

def scan_evidence():
    files = find_files("evidence", {".md", ".json", ".txt"})
    return {"count": len(files), "sample": [rel(x) for x in files[:20]]}

def tag_snapshot(limit=30):
    try:
        result = subprocess.run(["git", "tag", "--sort=-creatordate"], cwd=ROOT, text=True, capture_output=True, check=True)
        tags = [x for x in result.stdout.splitlines() if x.strip()]
        return {"count": len(tags), "latest": tags[:limit]}
    except Exception as exc:
        return {"count": 0, "latest": [], "error": str(exc)}

def check():
    schemas = scan_schemas()
    reports = scan_reports()
    evidence = scan_evidence()
    tags = tag_snapshot(20)
    ok = schemas["invalid"] == 0 and reports["count"] > 0 and evidence["count"] > 0
    return {
        "ok": ok,
        "checked_at": utc_now(),
        "schemas": schemas,
        "reports": reports,
        "evidence": evidence,
        "tags": tags
    }

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return target

def write_markdown_report(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Brain Doctor Report",
        "",
        f"Generated: {data.get('checked_at')}",
        f"Status: {'PASS' if data.get('ok') else 'FAIL'}",
        "",
        "## Counts",
        "",
        f"- Schemas: {data['schemas']['count']}",
        f"- Invalid schemas: {data['schemas']['invalid']}",
        f"- Reports/docs: {data['reports']['count']}",
        f"- Evidence files: {data['evidence']['count']}",
        f"- Tags: {data['tags']['count']}",
        ""
    ]
    if data["schemas"]["invalid_items"]:
        lines.append("## Invalid JSON")
        lines.append("")
        for item in data["schemas"]["invalid_items"]:
            lines.append(f"- {item['path']}: {item.get('error')}")
        lines.append("")
    target.write_text("\n".join(lines))
    return target

def export_bundle(path):
    data = check()
    report = write_markdown_report("brain/doctor/reports/brain-doctor-report.md", data)
    payload = write_json("brain/doctor/reports/brain-doctor-report.json", data)
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(report, report.relative_to(ROOT))
        archive.write(payload, payload.relative_to(ROOT))
    return {"ok": True, "export": rel(target), "report": rel(report), "payload": rel(payload)}

def main():
    parser = argparse.ArgumentParser(prog="brain-doctor")
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate-json")
    p_validate.add_argument("path")

    sub.add_parser("scan-schemas")
    sub.add_parser("scan-reports")
    sub.add_parser("scan-evidence")
    sub.add_parser("tag-snapshot")
    sub.add_parser("check")

    p_report = sub.add_parser("generate-report")
    p_report.add_argument("--json", default="brain/doctor/reports/brain-doctor-report.json")
    p_report.add_argument("--md", default="brain/doctor/reports/brain-doctor-report.md")

    p_export = sub.add_parser("export-evidence")
    p_export.add_argument("--out", default="brain/doctor/exports/brain-doctor-evidence.zip")

    args = parser.parse_args()

    if args.command == "validate-json":
        result = json_validate(args.path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["ok"] else 1)
    if args.command == "scan-schemas":
        print(json.dumps(scan_schemas(), indent=2, ensure_ascii=False))
        return
    if args.command == "scan-reports":
        print(json.dumps(scan_reports(), indent=2, ensure_ascii=False))
        return
    if args.command == "scan-evidence":
        print(json.dumps(scan_evidence(), indent=2, ensure_ascii=False))
        return
    if args.command == "tag-snapshot":
        print(json.dumps(tag_snapshot(), indent=2, ensure_ascii=False))
        return
    if args.command == "check":
        result = check()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["ok"] else 1)
    if args.command == "generate-report":
        result = check()
        write_json(args.json, result)
        write_markdown_report(args.md, result)
        print(json.dumps({"ok": result["ok"], "json": args.json, "md": args.md}, indent=2))
        sys.exit(0 if result["ok"] else 1)
    if args.command == "export-evidence":
        result = export_bundle(args.out)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

if __name__ == "__main__":
    main()
