#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

SAFE_FILES = ["PROJECT.md", "STATUS.md", "OPEN.md", "DECISIONS.md"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    raw = text[4:end]
    body = text[end + 5:]
    meta = {}
    for line in raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body


def section(body: str, heading: str) -> str:
    pat = re.compile(rf"^#{{1,2}}\s+{re.escape(heading)}\s*$", re.M | re.I)
    match = pat.search(body)
    if not match:
        return ""
    start = match.end()
    nxt = re.search(r"^#{1,2}\s+.+$", body[start:], re.M)
    end = start + nxt.start() if nxt else len(body)
    return body[start:end].strip()


def bullets(text: str):
    out = []
    for line in text.splitlines():
        value = line.strip()
        if value.startswith("- "):
            out.append(value[2:].strip())
        elif re.match(r"^\d+\.\s+", value):
            out.append(re.sub(r"^\d+\.\s+", "", value))
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(vault: Path) -> dict:
    base = vault / "Projects" / "AOC"
    docs = {}
    sources = []

    for name in SAFE_FILES:
        path = base / name
        if not path.is_file():
            raise SystemExit(f"Missing required note: {path}")
        meta, body = split_frontmatter(read_text(path))
        if meta.get("status") not in {"active", "current"}:
            raise SystemExit(f"Note is not current: {name}")
        docs[name] = (meta, body)
        sources.append({
            "source": str(path.relative_to(vault)),
            "sha256": sha256(path),
        })

    project_meta, project_body = docs["PROJECT.md"]
    _, status_body = docs["STATUS.md"]
    _, open_body = docs["OPEN.md"]
    _, decisions_body = docs["DECISIONS.md"]

    return {
        "current_project": project_meta.get("project", ""),
        "current_repo": project_meta.get("repo", ""),
        "where_we_stopped": section(status_body, "Gde smo stali"),
        "last_canon": section(status_body, "Poslednji kanon"),
        "open_threads": bullets(section(open_body, "Otvoreno")),
        "related_projects": bullets(section(project_body, "Povezani projekti")),
        "next_3_actions": bullets(section(open_body, "Sledeća 3 koraka"))[:3],
        "decisions_waiting_for_andy": bullets(section(decisions_body, "Odluke koje čekaju Andyja")),
        "authority_state": "HUMAN_REQUIRED",
        "execution_allowed": False,
        "provenance": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a simple KORMILO summary from an AOC Obsidian vault")
    parser.add_argument("vault", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = build(args.vault)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
