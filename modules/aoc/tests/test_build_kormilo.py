import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_kormilo.py"
VAULT = ROOT / "vault-proof-01d"


class TestKormiloLiveVault(unittest.TestCase):
    def run_build(self, vault=VAULT):
        result = subprocess.run([sys.executable, str(SCRIPT), str(vault)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_builds_expected_project(self):
        data = self.run_build()
        self.assertEqual(data["current_project"], "AOC — AndyAI Obsidian Cockpit")
        self.assertEqual(data["current_repo"], "kolundzic/andyai-second-brain")

    def test_keeps_human_authority(self):
        data = self.run_build()
        self.assertEqual(data["authority_state"], "HUMAN_REQUIRED")
        self.assertIs(data["execution_allowed"], False)

    def test_has_three_next_actions(self):
        data = self.run_build()
        self.assertEqual(len(data["next_3_actions"]), 3)

    def test_has_sources(self):
        data = self.run_build()
        self.assertEqual(len(data["provenance"]), 4)
        self.assertTrue(all(len(item["sha256"]) == 64 for item in data["provenance"]))

    def test_stale_note_is_not_used(self):
        data = self.run_build()
        blob = json.dumps(data, ensure_ascii=False)
        self.assertNotIn("rm -rf", blob)
        self.assertNotIn("bez odobrenja", blob)

    def test_missing_required_note_fails(self):
        with tempfile.TemporaryDirectory() as td:
            import shutil
            copy = Path(td) / "vault"
            shutil.copytree(VAULT, copy)
            (copy / "Projects" / "AOC" / "STATUS.md").unlink()
            result = subprocess.run([sys.executable, str(SCRIPT), str(copy)], text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
