#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "aoc-kormilo-contract-v0.1.json"


def walk_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_keys(item)


def validate(payload, contract):
    errors = []
    for field in contract["required_fields"]:
        if field not in payload:
            errors.append(f"missing required field: {field}")

    c = contract["constraints"]
    if payload.get("authority_state") != c["authority_state"]:
        errors.append("authority_state must remain HUMAN_REQUIRED")
    if payload.get("execution_allowed") is not c["execution_allowed"]:
        errors.append("execution_allowed must be false")

    actions = payload.get("next_3_actions", [])
    if not isinstance(actions, list) or len(actions) > c["next_actions_max"]:
        errors.append("next_3_actions must be a list with at most 3 items")

    provenance = payload.get("provenance", [])
    if not isinstance(provenance, list) or len(provenance) < c["provenance_min"]:
        errors.append("at least one provenance entry is required")

    forbidden = {k.lower() for k in contract["forbidden_keys"]}
    seen = {k.lower() for k in walk_keys(payload)}
    hits = sorted(forbidden & seen)
    if hits:
        errors.append("forbidden execution keys present: " + ", ".join(hits))

    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: validate_kormilo.py <fixture.json>")
        return 2

    with CONTRACT.open("r", encoding="utf-8") as f:
        contract = json.load(f)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        payload = json.load(f)

    errors = validate(payload, contract)
    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PASS")
    print("- required cockpit fields present")
    print("- human authority preserved")
    print("- direct execution disabled")
    print("- provenance present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
