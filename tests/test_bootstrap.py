"""Stdlib tests for the safe bootstrap generator."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "bootstrap.py"
spec = importlib.util.spec_from_file_location("bootstrap", MODULE)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


class BootstrapTests(unittest.TestCase):
    def test_supported_combinations(self):
        for stacks in ("web", "mobile-expo,database-supabase", "api", "database-supabase"):
            with self.subTest(stacks=stacks):
                self.assertTrue(bootstrap.validate("NewApp", stacks))

    def test_rejects_bad_inputs(self):
        for project, stacks in (("../bad", "web"), ("App", "unknown"), ("App", "web,web"), ("", "api")):
            with self.subTest(project=project, stacks=stacks):
                with self.assertRaises(ValueError):
                    bootstrap.validate(project, stacks)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bootstrap.execute("NewApp", ["web"], apply=False, root=root)
            self.assertEqual(list(root.iterdir()), [])

    def test_apply_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bootstrap.execute("NewApp", ["web", "database-supabase"], apply=True, root=root)
            content = (root / ".github/workflows/stack-ci.yml").read_text()
            self.assertIn("npm run build", content)
            self.assertIn("does NOT apply migrations", content)
            with self.assertRaises(FileExistsError):
                bootstrap.execute("NewApp", ["web"], apply=True, root=root)

    def test_mobile_avoids_build_and_production(self):
        w = bootstrap.workflow(["mobile-expo"])
        self.assertNotIn("npm run build", w)
        self.assertNotIn("deploy", w.lower())
        self.assertIn("npm ci", w)

    def test_db_only_has_no_node_requirement(self):
        w = bootstrap.workflow(["database-supabase"])
        self.assertNotIn("npm ci", w)
        self.assertIn("Review Supabase migrations", w)


if __name__ == "__main__":
    unittest.main()
