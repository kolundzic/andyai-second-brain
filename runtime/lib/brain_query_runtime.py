#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
BRAIN = ROOT / "brain"

TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml"}
IGNORE_PARTS = {".git", "__pycache__", ".DS_Store"}

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s[:80] or "query"

def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-zA-Z0-9_\-]+", text.lower()) if len(t) > 1]

def iter_files() -> Iterable[Path]:
    for base in [ROOT / "ANDYAI_CONTEXT.md", ROOT / "SECOND_BRAIN_CANON.md", ROOT / "README.md"]:
        if base.exists():
            yield base
    for folder in ["brain", "docs", "skills", "schemas", "examples"]:
        root = ROOT / folder
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if any(part in IGNORE_PARTS for part in path.parts):
                continue
            if path.suffix.lower() in TEXT_EXTS:
                yield path

def read_text(path: Path, limit: int = 120000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except Exception:
        return ""

def kind_for(path: Path) -> str:
    parts = set(path.parts)
    if "evidence" in parts or "evidence-packs" in parts:
        return "evidence"
    if "decisions" in parts:
        return "decision"
    if "projects" in parts:
        return "project"
    if "skills" in parts:
        return "skill"
    if "reports" in parts:
        return "report"
    if "schemas" in parts:
        return "schema"
    if "archives" in parts:
        return "archive"
    return "resource"

def stale_warning(path: Path, text: str) -> str:
    lower = str(path).lower()
    if "/archives/" in lower or "archive" in lower:
        return "archive-source-review-before-action"
    if "deprecated" in text.lower():
        return "deprecated-source-review-before-action"
    return ""

def snippet_for(text: str, terms: list[str], size: int = 420) -> str:
    lower = text.lower()
    idxs = [lower.find(t) for t in terms if lower.find(t) >= 0]
    if idxs:
        start = max(min(idxs) - 120, 0)
    else:
        start = 0
    snippet = text[start:start+size].replace("\n", " ").strip()
    return re.sub(r"\s+", " ", snippet)

def score_text(query_terms: list[str], path: Path, text: str) -> float:
    if not query_terms:
        return 0.0
    lower = text.lower()
    path_lower = str(path).lower()
    score = 0.0
    for term in query_terms:
        score += lower.count(term)
        if term in path_lower:
            score += 4.0
    k = kind_for(path)
    if k in {"evidence", "decision", "project"}:
        score += 3.0
    elif k in {"report", "skill"}:
        score += 1.5
    if "pack4" in path_lower:
        score += 1.0
    return score

def search(query: str, max_results: int = 10, project: str = "") -> list[dict]:
    terms = tokenize(query + " " + project)
    results = []
    for path in iter_files():
        text = read_text(path)
        if not text:
            continue
        score = score_text(terms, path, text)
        if score <= 0:
            continue
        rel = str(path.relative_to(ROOT))
        kind = kind_for(path)
        results.append({
            "path": rel,
            "score": round(score, 3),
            "kind": kind,
            "snippet": snippet_for(text, terms),
            "reason": f"Matched query terms in {kind} source.",
            "staleness_warning": stale_warning(path, text)
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]

def ensure_dirs() -> None:
    for d in [
        BRAIN / "query",
        BRAIN / "retrieval",
        BRAIN / "context" / "bundles",
        BRAIN / "context" / "handoffs",
        BRAIN / "answers",
        BRAIN / "reports",
        BRAIN / "evidence-packs",
        BRAIN / "search"
    ]:
        d.mkdir(parents=True, exist_ok=True)

def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def build_bundle(query: str, project: str = "", max_results: int = 10) -> dict:
    results = search(query, max_results=max_results, project=project)
    evidence = [r for r in results if r["kind"] == "evidence"]
    warnings = [f"{r['path']}: {r['staleness_warning']}" for r in results if r.get("staleness_warning")]
    return {
        "query": query,
        "project": project,
        "created_at": now(),
        "sources": results,
        "evidence": evidence,
        "warnings": warnings,
        "next_action": "Review context bundle, then decide whether to answer, inspect sources, or request human approval."
    }

def markdown_bundle(bundle: dict) -> str:
    lines = [
        f"# Context Bundle — {bundle['query']}",
        "",
        f"Created: `{bundle['created_at']}`",
        f"Project: `{bundle.get('project') or 'not-specified'}`",
        "",
        "## Sources",
        ""
    ]
    for i, src in enumerate(bundle["sources"], 1):
        lines += [
            f"### {i}. `{src['path']}`",
            "",
            f"- Score: `{src['score']}`",
            f"- Kind: `{src['kind']}`",
            f"- Reason: {src['reason']}",
        ]
        if src.get("staleness_warning"):
            lines.append(f"- Warning: `{src['staleness_warning']}`")
        lines += ["", f"> {src['snippet']}", ""]
    if bundle["warnings"]:
        lines += ["## Warnings", ""]
        lines += [f"- {w}" for w in bundle["warnings"]]
        lines.append("")
    lines += ["## Next Action", "", bundle["next_action"], ""]
    return "\n".join(lines)

def cmd_index(args: argparse.Namespace) -> None:
    ensure_dirs()
    records = []
    for path in iter_files():
        text = read_text(path)
        records.append({
            "path": str(path.relative_to(ROOT)),
            "kind": kind_for(path),
            "tokens": len(tokenize(text)),
            "chars": len(text)
        })
    out = BRAIN / "search" / "brain-index.json"
    write_json(out, {"created_at": now(), "records": records})
    print(f"🟢 Brain query index written: {out.relative_to(ROOT)} ({len(records)} records)")

def cmd_search(args: argparse.Namespace) -> None:
    ensure_dirs()
    results = search(args.query, max_results=args.max_results, project=args.project or "")
    payload = {
        "query": args.query,
        "project": args.project,
        "created_at": now(),
        "results": results
    }
    out = BRAIN / "retrieval" / f"{now()}-{slug(args.query)}.json"
    write_json(out, payload)
    for r in results:
        print(f"{r['score']:>6}  {r['kind']:<9}  {r['path']}")
    print(f"🟢 Retrieval results written: {out.relative_to(ROOT)}")

def cmd_bundle(args: argparse.Namespace) -> None:
    ensure_dirs()
    bundle = build_bundle(args.query, project=args.project or "", max_results=args.max_results)
    base = f"{now()}-{slug(args.query)}"
    json_out = BRAIN / "context" / "bundles" / f"{base}.json"
    md_out = BRAIN / "context" / "bundles" / f"{base}.md"
    write_json(json_out, bundle)
    md_out.write_text(markdown_bundle(bundle), encoding="utf-8")
    print(f"🟢 Context bundle written: {md_out.relative_to(ROOT)}")
    print(f"🟢 Context bundle JSON written: {json_out.relative_to(ROOT)}")

def cmd_handoff(args: argparse.Namespace) -> None:
    ensure_dirs()
    bundle = build_bundle(args.query, project=args.project or "", max_results=args.max_results)
    base = f"{now()}-{slug(args.query)}"
    out = BRAIN / "context" / "handoffs" / f"{base}-agent-handoff.md"
    md = [
        f"# Agent Handoff — {args.query}",
        "",
        "## Instruction",
        "",
        "Use this handoff as the minimal context set before acting. Do not assume unstated facts. Inspect sources if needed.",
        "",
        markdown_bundle(bundle)
    ]
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"🟢 Agent handoff written: {out.relative_to(ROOT)}")

def cmd_answer_draft(args: argparse.Namespace) -> None:
    ensure_dirs()
    bundle = build_bundle(args.query, project=args.project or "", max_results=args.max_results)
    base = f"{now()}-{slug(args.query)}"
    out = BRAIN / "answers" / f"{base}-answer-draft.md"
    lines = [
        f"# Answer Draft — {args.query}",
        "",
        "## Grounded Findings",
        "",
    ]
    for src in bundle["sources"][:5]:
        lines.append(f"- `{src['path']}` — {src['reason']}")
    lines += [
        "",
        "## Assumptions",
        "",
        "- Add assumptions explicitly before final answer.",
        "",
        "## Evidence To Inspect",
        "",
    ]
    for src in bundle["sources"]:
        if src["kind"] in {"evidence", "decision", "project", "report"}:
            lines.append(f"- `{src['path']}`")
    lines += [
        "",
        "## Draft Response",
        "",
        "Write the user-facing response here after inspecting the context bundle.",
        ""
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"🟢 Answer draft written: {out.relative_to(ROOT)}")

def cmd_report(args: argparse.Namespace) -> None:
    ensure_dirs()
    report = BRAIN / "reports" / "PACK4_CONTEXT_ASSEMBLY_REPORT.md"
    bundles = list((BRAIN / "context" / "bundles").glob("*.md"))
    retrievals = list((BRAIN / "retrieval").glob("*.json"))
    handoffs = list((BRAIN / "context" / "handoffs").glob("*.md"))
    report.write_text(f"""# PACK4 Context Assembly Report

Created: `{now()}`

## Counts

- Context bundles: {len(bundles)}
- Retrieval result files: {len(retrievals)}
- Agent handoffs: {len(handoffs)}

## Status

PACK4 query/retrieval/context assembly runtime is present.

## Next Action

Use `runtime/bin/brain-query bundle "your query"` to create a compact context bundle before major AI action.
""", encoding="utf-8")
    print(f"🟢 Context assembly report written: {report.relative_to(ROOT)}")

def main() -> None:
    parser = argparse.ArgumentParser(prog="brain-query")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("index")
    p.set_defaults(func=cmd_index)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--project", default="")
    p.add_argument("--max-results", type=int, default=10)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("bundle")
    p.add_argument("query")
    p.add_argument("--project", default="")
    p.add_argument("--max-results", type=int, default=10)
    p.set_defaults(func=cmd_bundle)

    p = sub.add_parser("handoff")
    p.add_argument("query")
    p.add_argument("--project", default="")
    p.add_argument("--max-results", type=int, default=10)
    p.set_defaults(func=cmd_handoff)

    p = sub.add_parser("answer-draft")
    p.add_argument("query")
    p.add_argument("--project", default="")
    p.add_argument("--max-results", type=int, default=10)
    p.set_defaults(func=cmd_answer_draft)

    p = sub.add_parser("report")
    p.set_defaults(func=cmd_report)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
