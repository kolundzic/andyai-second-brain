import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import host_check


NOTES = {
    "Projects/AOC/PROJECT.md": """---
status: active
project: AOC
repo: kolundzic/andyai-second-brain
---
## Povezani projekti
- ALOG
- GOM
""",
    "Projects/AOC/STATUS.md": """---
status: current
---
## Gde smo stali
01D je prošao.

## Poslednji kanon
AOC-KORMILO-LIVE-VAULT-01D
""",
    "Projects/AOC/OPEN.md": """---
status: active
---
## Otvoreno
- Povezati pravi host

## Sledeća 3 koraka
1. Proveri CLI
2. Pročitaj vault
3. Uporedi KORMILO
""",
    "Projects/AOC/DECISIONS.md": """---
status: active
---
## Odluke koje čekaju Andyja
- Izabrati prvi host
""",
}


class Result:
    def __init__(self, stdout="", stderr="", returncode=0):
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


def good_reader(command, params, vault=None):
    if command == "vault":
        return Result("/Users/andy/AOC\n")
    if command == "read":
        path = params["path"]
        if path in NOTES:
            return Result(NOTES[path])
        return Result(stderr="missing", returncode=1)
    return Result(stderr="not allowed", returncode=1)


class HostCheckTests(unittest.TestCase):
    def test_builds_kormilo_from_obsidian_reads(self):
        data = host_check.build_from_obsidian("AOC Proof", reader=good_reader)
        self.assertEqual(data["current_project"], "AOC")
        self.assertEqual(data["current_repo"], "kolundzic/andyai-second-brain")
        self.assertEqual(len(data["next_3_actions"]), 3)
        self.assertEqual(len(data["provenance"]), 4)
        self.assertEqual(data["host_check"]["read_via"], "obsidian_cli_readonly_adapter")

    def test_human_authority_is_preserved(self):
        data = host_check.build_from_obsidian("AOC Proof", reader=good_reader)
        self.assertEqual(data["authority_state"], "HUMAN_REQUIRED")
        self.assertFalse(data["execution_allowed"])

    def test_missing_required_note_stops(self):
        def missing_reader(command, params, vault=None):
            if command == "vault":
                return Result("/Users/andy/AOC\n")
            if command == "read" and params["path"].endswith("OPEN.md"):
                return Result(stderr="missing", returncode=1)
            return good_reader(command, params, vault=vault)

        with self.assertRaises(host_check.HostCheckError):
            host_check.build_from_obsidian("AOC Proof", reader=missing_reader)


if __name__ == "__main__":
    unittest.main()
