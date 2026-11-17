import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("protect", Path(__file__).resolve().parents[1] / "scripts" / "protect_github.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class TestProtection(unittest.TestCase):
    def test_preview_is_offline(self):
        with patch.object(p, "api", side_effect=AssertionError("API must not run")):
            result = p.run("someone/project", "validate")
        self.assertEqual(result["mode"], "DRY RUN")
        self.assertIn("required_status_checks", [r["type"] for r in result["planned_ruleset"]["rules"]])

    def test_default_plan_has_pr_no_force_delete(self):
        rules = p.make_ruleset(None)["rules"]
        self.assertEqual({r["type"] for r in rules}, {"deletion", "non_fast_forward", "pull_request"})

    def test_bad_repository(self):
        with self.assertRaises(p.ProtectionError):
            p.run("../other")

    def test_apply_requires_exact_confirmation(self):
        with patch.object(p, "api", side_effect=AssertionError("API must not run")):
            with self.assertRaises(p.ProtectionError):
                p.run("someone/project", apply=True)

    def test_existing_ruleset_causes_refusal(self):
        def fake(method, path, payload=None):
            if path == "repos/someone/project":
                return {"full_name": "someone/project", "default_branch": "main"}
            return [{"name": "main-protection", "target": "branch"}]
        with patch.object(p, "api", side_effect=fake):
            with self.assertRaises(p.ProtectionError):
                p.run("someone/project", apply=True, approve="someone/project")

    def test_existing_other_ruleset_causes_refusal(self):
        def fake(method, path, payload=None):
            if path == "repos/someone/project":
                return {"full_name": "someone/project", "default_branch": "main"}
            return [{"name": "another-rule", "target": "branch"}]
        with patch.object(p, "api", side_effect=fake):
            with self.assertRaises(p.ProtectionError):
                p.run("someone/project", apply=True, approve="someone/project")

    def test_verified_create(self):
        def fake(method, path, payload=None):
            if method == "GET" and path == "repos/someone/project":
                return {"full_name": "someone/project", "default_branch": "main"}
            if method == "GET" and path.endswith("/rulesets"):
                return []
            if method == "POST":
                return {"id": 123}
            return {"enforcement": "active", "conditions": {"ref_name": {"include": ["refs/heads/main"]}},
                    "rules": [{"type": t} for t in ("pull_request", "deletion", "non_fast_forward")]}
        with patch.object(p, "api", side_effect=fake):
            result = p.run("someone/project", apply=True, approve="someone/project")
        self.assertTrue(result["verified"])

    def test_apply_refuses_unverified_check(self):
        def fake(method, path, payload=None):
            if path == "repos/someone/project":
                return {"full_name": "someone/project", "default_branch": "main"}
            return []
        with patch.object(p, "api", side_effect=fake):
            with self.assertRaises(p.ProtectionError):
                p.run("someone/project", check="validate", apply=True, approve="someone/project")


if __name__ == "__main__":
    unittest.main()
