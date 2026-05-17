import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[2]

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))

def run(cmd, allow_fail=False):
    try:
        result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=not allow_fail)
        return {"ok": result.returncode == 0, "code": result.returncode, "stdout": result.stdout.strip(), "stderr": result.stderr.strip()}
    except subprocess.CalledProcessError as exc:
        return {"ok": False, "code": exc.returncode, "stdout": exc.stdout, "stderr": exc.stderr}

def exists(path):
    return (ROOT / path).exists()

def refresh_exports():
    results = {}
    if exists("runtime/bin/artifact-viewer"):
        results["artifact_viewer"] = run(["runtime/bin/artifact-viewer", "generate-all"], allow_fail=True)
    if exists("runtime/bin/vercel-export"):
        results["vercel_export"] = run(["runtime/bin/vercel-export", "export-public"], allow_fail=True)
        results["vercel_readiness"] = run(["runtime/bin/vercel-export", "readiness"], allow_fail=True)
    if exists("runtime/bin/client-report"):
        results["client_report"] = run(["runtime/bin/client-report", "export-public"], allow_fail=True)
    return results

def privacy_gate():
    if exists("runtime/bin/privacy-firewall"):
        return run(["runtime/bin/privacy-firewall", "public-gate"], allow_fail=True)
    return {"ok": False, "stderr": "privacy-firewall missing"}

def check():
    refresh = refresh_exports()
    privacy = privacy_gate()
    checks = {
        "public_index": exists("public/index.html"),
        "public_manifest": exists("public/manifest.json"),
        "vercel_json": exists("vercel.json"),
        "client_page": exists("public/client/index.html") or exists("public/client-portal/index.html"),
        "privacy_firewall": exists("runtime/bin/privacy-firewall"),
        "privacy_gate_ok": privacy.get("ok", False)
    }
    ok = all(v for k, v in checks.items() if k != "privacy_gate_ok")
    report = {
        "kind": "andyai.vercel_operator.readiness",
        "generated_at": utc_now(),
        "ok": ok,
        "privacy_gate_ok": privacy.get("ok", False),
        "note": "privacy_gate_ok may be false when findings exist; human review is required before production deploy.",
        "checks": checks,
        "refresh": refresh,
        "privacy_gate": privacy
    }
    out = ROOT / "brain/vercel-operator/reports/vercel-operator-readiness.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    md = ROOT / "brain/vercel-operator/reports/vercel-operator-readiness.md"
    md.write_text("# Vercel Operator Readiness\n\n" + "\n".join([f"- {k}: {v}" for k, v in checks.items()]) + "\n\nHuman approval required before production deploy.\n")
    return report

def deploy_command():
    cmd = "vercel --prod"
    out = ROOT / "brain/vercel-operator/reports/vercel-deploy-command.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(cmd + "\n")
    return {"ok": True, "command": cmd, "file": rel(out), "warning": "Run only after human approval."}

def preview_command():
    cmd = "cd public && python3 -m http.server 4173"
    out = ROOT / "brain/vercel-operator/reports/local-preview-command.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(cmd + "\n")
    return {"ok": True, "command": cmd, "url": "http://localhost:4173"}

def bundle(path="brain/vercel-operator/exports/vercel-operator-readiness.zip"):
    check()
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for item in ["brain/vercel-operator/reports/vercel-operator-readiness.json", "brain/vercel-operator/reports/vercel-operator-readiness.md", "vercel.json", "public/index.html"]:
            p = ROOT / item
            if p.exists():
                archive.write(p, p.relative_to(ROOT))
    return {"ok": True, "export": rel(target)}

def main():
    parser = argparse.ArgumentParser(prog="vercel-operator")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh")
    sub.add_parser("check")
    sub.add_parser("privacy-gate")
    sub.add_parser("preview-command")
    sub.add_parser("deploy-command")
    sub.add_parser("bundle")
    args = parser.parse_args()
    if args.command == "refresh":
        print(json.dumps(refresh_exports(), indent=2, ensure_ascii=False))
    elif args.command == "check":
        print(json.dumps(check(), indent=2, ensure_ascii=False))
    elif args.command == "privacy-gate":
        print(json.dumps(privacy_gate(), indent=2, ensure_ascii=False))
    elif args.command == "preview-command":
        print(json.dumps(preview_command(), indent=2, ensure_ascii=False))
    elif args.command == "deploy-command":
        print(json.dumps(deploy_command(), indent=2, ensure_ascii=False))
    elif args.command == "bundle":
        print(json.dumps(bundle(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
