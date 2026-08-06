import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "creating-skills", "scripts")
sys.path.insert(0, SCRIPTS)

import new_skill as N  # noqa: E402
import validate_skill as V  # noqa: E402


class Scaffold(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_scaffold_is_conformant(self):
        rc = N.scaffold("managing-backups", N.DEFAULT_DESC, False, self.tmp)
        self.assertEqual(rc, 0)
        d = os.path.join(self.tmp, "managing-backups")
        self.assertTrue(os.path.isfile(os.path.join(d, "SKILL.md")))
        self.assertTrue(os.path.isdir(os.path.join(d, "references")))
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [], f"scaffold not conformant: {errs}")

    def test_with_scripts_creates_scripts_dir(self):
        N.scaffold("processing-pdfs", N.DEFAULT_DESC, True, self.tmp)
        d = os.path.join(self.tmp, "processing-pdfs")
        self.assertTrue(os.path.isdir(os.path.join(d, "scripts")))
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [])

    def test_refuses_existing_dir(self):
        os.makedirs(os.path.join(self.tmp, "dupe"))
        rc = N.scaffold("dupe", N.DEFAULT_DESC, False, self.tmp)
        self.assertEqual(rc, 1)


class Cli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.script = os.path.join(SCRIPTS, "new_skill.py")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, self.script, *args],
                              capture_output=True, text=True)

    def test_invalid_name_exit_1(self):
        r = self.run_cli("Bad_Name", "--dest", self.tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("invalid name", r.stderr)

    def test_reserved_name_exit_1(self):
        r = self.run_cli("claude-helper", "--dest", self.tmp)
        self.assertEqual(r.returncode, 1)

    def test_valid_name_exit_0_and_validates(self):
        r = self.run_cli("analyzing-logs", "--dest", self.tmp)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        d = os.path.join(self.tmp, "analyzing-logs")
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [])


if __name__ == "__main__":
    unittest.main()
