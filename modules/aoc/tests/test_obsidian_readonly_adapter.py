#!/usr/bin/env python3
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "obsidian_readonly_adapter.py"
spec = importlib.util.spec_from_file_location("aoc_adapter", MODULE)
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
CONTRACT = a.load_contract()


class ReadOnlyAdapterTests(unittest.TestCase):
    def test_read_is_allowed(self):
        argv = a.build_argv("read", {"path": "Projects/AOC.md"}, vault="AndyAI", contract=CONTRACT)
        self.assertEqual(argv, ["obsidian", "vault=AndyAI", "read", "path=Projects/AOC.md"])

    def test_search_is_allowed(self):
        argv = a.build_argv("search", {"query": "KORMILO", "limit": 20, "format": "json"}, contract=CONTRACT)
        self.assertEqual(argv[1], "search")
        self.assertIn("query=KORMILO", argv)

    def test_delete_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("delete", {"path": "Canon.md"}, contract=CONTRACT)

    def test_create_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("create", {"path": "x.md"}, contract=CONTRACT)

    def test_command_escape_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("command", {"id": "some.plugin.command"}, contract=CONTRACT)

    def test_eval_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("eval", {"code": "app.vault.delete(...)"}, contract=CONTRACT)

    def test_parent_traversal_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("read", {"path": "../outside.md"}, contract=CONTRACT)

    def test_absolute_path_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("read", {"path": "/etc/passwd"}, contract=CONTRACT)

    def test_unknown_parameter_is_blocked(self):
        with self.assertRaises(a.ContractError):
            a.build_argv("read", {"path": "x.md", "overwrite": True}, contract=CONTRACT)

    def test_binary_is_fixed_to_obsidian(self):
        altered = json.loads(json.dumps(CONTRACT))
        altered["binary"] = "/bin/echo"
        with self.assertRaises(a.ContractError):
            a.build_argv("read", {"path": "x.md"}, contract=altered)

    def test_false_boolean_is_not_emitted(self):
        argv = a.build_argv("tasks", {"todo": False, "total": True}, contract=CONTRACT)
        self.assertIn("total", argv)
        self.assertNotIn("todo", argv)


if __name__ == "__main__":
    unittest.main(verbosity=2)
