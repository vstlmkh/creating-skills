import json
import os
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(ROOT, "bin", "cli.js")


class Installer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def run_cli(self, *args, env=None):
        return subprocess.run(["node", CLI, *args], capture_output=True, text=True, env=env)

    def test_help_lists_kimi(self):
        r = self.run_cli("--help")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("kimi", r.stdout)
        self.assertIn("claude", r.stdout)

    def test_kimi_install_respects_kimi_code_home_and_force(self):
        env = os.environ.copy()
        env["KIMI_CODE_HOME"] = os.path.join(self.tmp, "isolated-kimi")
        r = self.run_cli("install", "--agent", "kimi", env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        dest = os.path.join(env["KIMI_CODE_HOME"], "skills", "creating-skills")
        self.assertTrue(os.path.isfile(os.path.join(dest, "SKILL.md")))
        self.assertTrue(os.path.isfile(os.path.join(dest, "references", "platforms.md")))

        rerun = self.run_cli("install", "--agent", "kimi", env=env)
        self.assertEqual(rerun.returncode, 1)
        forced = self.run_cli("install", "--agent", "kimi", "--force", env=env)
        self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)

    def test_claude_install_uses_claude_skills_directory(self):
        env = os.environ.copy()
        env["HOME"] = os.path.join(self.tmp, "home")
        r = self.run_cli("install", "--agent", "claude", env=env)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        dest = os.path.join(env["HOME"], ".claude", "skills", "creating-skills", "SKILL.md")
        self.assertTrue(os.path.isfile(dest))

    def test_version_matches_package(self):
        with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as fh:
            version = json.load(fh)["version"]
        r = self.run_cli("--version")
        self.assertEqual(r.returncode, 0)
        self.assertEqual(r.stdout.strip(), version)


if __name__ == "__main__":
    unittest.main()
