#!/usr/bin/env python3
"""AOC 01C — strict read-only adapter for the official Obsidian CLI.

The adapter never accepts a raw command line. It receives a command plus a mapping
of parameters, validates both against a contract, and calls subprocess with
shell=False. This file deliberately has no write-capable command in its allow-list.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "contracts" / "aoc-obsidian-readonly-contract-v0.1.json"
CONTROL_RE = re.compile(r"[\x00-\x1f\x7f]")
SAFE_VAULT_RE = re.compile(r"^[^\x00-\x1f\x7f]{1,120}$")


class ContractError(ValueError):
    pass


def load_contract(path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _validate_path(value: str, policy: dict[str, Any]) -> None:
    if policy.get("reject_control_characters") and CONTROL_RE.search(value):
        raise ContractError("path contains control characters")
    if policy.get("reject_absolute") and (value.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", value)):
        raise ContractError("absolute paths are not allowed")
    parts = re.split(r"[\\/]", value)
    if policy.get("reject_parent_traversal") and ".." in parts:
        raise ContractError("parent traversal is not allowed")


def _validate_value(key: str, value: Any, contract: dict[str, Any]) -> str | None:
    if isinstance(value, bool):
        return key if value else None
    if value is None:
        return None
    if not isinstance(value, (str, int)):
        raise ContractError(f"unsupported value type for {key}")
    text = str(value)
    if CONTROL_RE.search(text):
        raise ContractError(f"control characters are not allowed in {key}")
    if key in {"path", "folder"}:
        _validate_path(text, contract.get("path_policy", {}))
    if key == "limit":
        try:
            n = int(text)
        except ValueError as exc:
            raise ContractError("limit must be an integer") from exc
        if not 1 <= n <= 500:
            raise ContractError("limit must be between 1 and 500")
    if key == "format" and text not in {"text", "json", "tsv", "csv", "md", "yaml", "tree"}:
        raise ContractError("unsupported output format")
    if key == "info" and text not in {"name", "path", "files", "folders", "size"}:
        raise ContractError("unsupported vault info selector")
    return f"{key}={text}"


def build_argv(command: str, params: dict[str, Any], *, vault: str | None = None,
               contract: dict[str, Any] | None = None) -> list[str]:
    contract = contract or load_contract()
    allowed = contract["allowed_commands"]
    forbidden = set(contract.get("forbidden_commands", []))

    if command in forbidden or command not in allowed:
        raise ContractError(f"command is not read-only or not approved: {command}")

    if not isinstance(params, dict):
        raise ContractError("params must be an object")

    allowed_params = set(allowed[command])
    unknown = sorted(set(params) - allowed_params)
    if unknown:
        raise ContractError("unapproved parameters: " + ", ".join(unknown))

    binary = contract.get("binary", "obsidian")
    if binary != "obsidian":
        raise ContractError("adapter binary is fixed to obsidian")
    argv = [binary]
    if vault is not None:
        if not SAFE_VAULT_RE.match(vault):
            raise ContractError("invalid vault selector")
        argv.append(f"vault={vault}")
    argv.append(command)

    for key, value in params.items():
        encoded = _validate_value(key, value, contract)
        if encoded:
            argv.append(encoded)

    return argv


def run_readonly(command: str, params: dict[str, Any], *, vault: str | None = None,
                 contract: dict[str, Any] | None = None) -> subprocess.CompletedProcess[str]:
    contract = contract or load_contract()
    argv = build_argv(command, params, vault=vault, contract=contract)
    timeout = int(contract.get("execution", {}).get("timeout_seconds", 10))
    env = {"PATH": os.environ.get("PATH", "")}
    return subprocess.run(
        argv,
        shell=False,
        check=False,
        text=True,
        capture_output=True,
        timeout=timeout,
        env=env,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="AOC strict read-only Obsidian CLI adapter")
    parser.add_argument("command")
    parser.add_argument("--params", default="{}", help="JSON object of approved command parameters")
    parser.add_argument("--vault", default=None)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        params = json.loads(args.params)
        argv = build_argv(args.command, params, vault=args.vault)
    except (json.JSONDecodeError, ContractError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(json.dumps(argv, ensure_ascii=False))
        return 0

    try:
        result = run_readonly(args.command, params, vault=args.vault)
    except FileNotFoundError:
        print("ERROR: obsidian CLI binary not found", file=sys.stderr)
        return 127
    except subprocess.TimeoutExpired:
        print("ERROR: obsidian CLI timed out", file=sys.stderr)
        return 124

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
