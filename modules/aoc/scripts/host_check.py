#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from obsidian_readonly_adapter import ContractError, run_readonly
from build_kormilo import SAFE_FILES, bullets, section, split_frontmatter

NOTE_PREFIX = "Projects/AOC"


class HostCheckError(RuntimeError):
    pass


def _run_fixed(args: list[str], timeout: int = 10) -> subprocess.CompletedProcess[str]:
    """Run only hard-coded, read-only Obsidian discovery commands."""
    return subprocess.run(
        ["obsidian", *args],
        shell=False,
        check=False,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def cli_info() -> dict[str, str]:
    version = _run_fixed(["version"])
    if version.returncode != 0:
        raise HostCheckError(version.stderr.strip() or "Obsidian CLI version check failed")

    vaults = _run_fixed(["vaults", "verbose"])
    if vaults.returncode != 0:
        raise HostCheckError(vaults.stderr.strip() or "Could not list Obsidian vaults")

    return {
        "version": version.stdout.strip(),
        "vaults": vaults.stdout.strip(),
    }


def build_from_obsidian(vault: str, *, reader=run_readonly) -> dict:
    docs: dict[str, tuple[dict, str]] = {}
    sources = []

    vault_path = reader("vault", {"info": "path"}, vault=vault)
    if vault_path.returncode != 0:
        raise HostCheckError(vault_path.stderr.strip() or f"Could not open vault: {vault}")

    for name in SAFE_FILES:
        rel = f"{NOTE_PREFIX}/{name}"
        result = reader("read", {"path": rel}, vault=vault)
        if result.returncode != 0:
            raise HostCheckError(result.stderr.strip() or f"Missing required note: {rel}")

        text = result.stdout
        meta, body = split_frontmatter(text)
        if meta.get("status") not in {"active", "current"}:
            raise HostCheckError(f"Note is not current: {rel}")
        docs[name] = (meta, body)
        sources.append({
            "source": rel,
            "content_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        })

    project_meta, project_body = docs["PROJECT.md"]
    _, status_body = docs["STATUS.md"]
    _, open_body = docs["OPEN.md"]
    _, decisions_body = docs["DECISIONS.md"]

    next_actions = bullets(section(open_body, "Sledeća 3 koraka"))[:3]
    if len(next_actions) != 3:
        raise HostCheckError("Expected exactly 3 next actions")

    return {
        "current_project": project_meta.get("project", ""),
        "current_repo": project_meta.get("repo", ""),
        "where_we_stopped": section(status_body, "Gde smo stali"),
        "last_canon": section(status_body, "Poslednji kanon"),
        "open_threads": bullets(section(open_body, "Otvoreno")),
        "related_projects": bullets(section(project_body, "Povezani projekti")),
        "next_3_actions": next_actions,
        "decisions_waiting_for_andy": bullets(section(decisions_body, "Odluke koje čekaju Andyja")),
        "authority_state": "HUMAN_REQUIRED",
        "execution_allowed": False,
        "host_check": {
            "vault": vault,
            "vault_path": vault_path.stdout.strip(),
            "read_via": "obsidian_cli_readonly_adapter",
        },
        "provenance": sources,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="AOC 01E — check a real Obsidian host without writing to the vault")
    parser.add_argument("--vault", help="Obsidian vault name or id")
    parser.add_argument("--list", action="store_true", help="Only show Obsidian version and known vaults")
    args = parser.parse_args()

    try:
        info = cli_info()
    except (FileNotFoundError, subprocess.TimeoutExpired, HostCheckError) as exc:
        print(f"HOST CHECK FAILED: {exc}", file=sys.stderr)
        return 2

    if args.list or not args.vault:
        print(f"Obsidian: {info['version']}")
        print("Known vaults:")
        print(info["vaults"] or "(none)")
        if not args.vault:
            print("\nRun again with: python3 scripts/host_check.py --vault \"VAULT NAME\"")
        return 0 if args.list else 3

    try:
        data = build_from_obsidian(args.vault)
    except (ContractError, HostCheckError, subprocess.TimeoutExpired) as exc:
        print(f"HOST CHECK FAILED: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
