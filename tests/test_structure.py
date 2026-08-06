import ast
import os
import re
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_DIR = os.path.join(ROOT, "skills", "creating-skills")
SCRIPTS = os.path.join(SKILL_DIR, "scripts")
REFS = os.path.join(SKILL_DIR, "references")
sys.path.insert(0, SCRIPTS)

import validate_skill as V  # noqa: E402

NINETEEN_KEYS = [
    "naming-conventions", "writing-effective-descriptions", "progressive-disclosure",
    "avoid-deeply-nested-references", "table-of-contents",
    "workflows-and-feedback-loops", "implement-feedback-loops",
    "avoid-time-sensitive-information", "use-consistent-terminology",
    "evaluation-and-iteration", "solve-dont-punt", "provide-utility-scripts",
    "use-visual-analysis", "create-verifiable-intermediate-outputs",
    "package-dependencies", "runtime-environment", "mcp-tool-references",
    "avoid-assuming-tools-are-installed", "token-budgets",
]

# Every top-level module either scripts may import. Anything outside this set is a
# third-party dependency and fails the agent-agnostic / zero-deps requirement.
STDLIB_ALLOWED = {
    "argparse", "os", "sys", "json", "math", "re", "collections", "__future__",
}
LOCAL_ALLOWED = {"validate_skill"}


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class BestPractices(unittest.TestCase):
    def setUp(self):
        self.text = read(os.path.join(REFS, "best-practices.md"))

    def test_has_toc(self):
        self.assertIn("## Contents", self.text)

    def test_all_19_keys_present(self):
        missing = [k for k in NINETEEN_KEYS if k not in self.text]
        self.assertEqual(missing, [], f"missing best-practice keys: {missing}")

    def test_exactly_19(self):
        self.assertEqual(len(NINETEEN_KEYS), 19)


class Checklist(unittest.TestCase):
    def test_key_items_present(self):
        text = read(os.path.join(REFS, "checklist.md"))
        self.assertIn("Run the validator", text)
        self.assertIn("evaluation-and-iteration", text)
        self.assertIn("mcp-tool-references", text)


class TemplatesRoundTrip(unittest.TestCase):
    def test_instructions_skeleton_validates(self):
        text = read(os.path.join(REFS, "templates.md"))
        blocks = re.findall(r"```markdown\n(.*?)```", text, re.DOTALL)
        skeleton = next((b for b in blocks if "name: {{name}}" in b), None)
        self.assertIsNotNone(skeleton, "no instructions-only skeleton found")
        name = "analyzing-logs"
        filled = skeleton.replace("{{name}}", name).replace(
            "{{description}}",
            "Analyzes log files and surfaces errors. Use when inspecting logs.",
        )
        tmp = tempfile.mkdtemp()
        d = os.path.join(tmp, name)
        os.makedirs(os.path.join(d, "references"))
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write(filled)
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [], f"skeleton not conformant: {errs}")


class Evals(unittest.TestCase):
    def test_at_least_three_valid_evals(self):
        import glob
        import json
        files = glob.glob(os.path.join(SKILL_DIR, "evals", "*.json"))
        self.assertGreaterEqual(len(files), 3, "need at least three eval scenarios")
        for f in files:
            data = json.load(open(f, encoding="utf-8"))
            self.assertIn("skills", data)
            self.assertIn("query", data)
            self.assertIsInstance(data.get("expected_behavior"), list)
            self.assertIsInstance(data.get("should_trigger"), bool)


class Dogfood(unittest.TestCase):
    def test_skill_validates_itself(self):
        errs = [f for f in V.validate_skill(SKILL_DIR) if f.level == "ERROR"]
        self.assertEqual(errs, [], f"creating-skills fails its own validator: {errs}")


class ImportScan(unittest.TestCase):
    def _top_imports(self, path):
        tree = ast.parse(read(path))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    names.add(node.module.split(".")[0])
        return names

    def test_scripts_import_stdlib_only(self):
        for fn in ("validate_skill.py", "new_skill.py"):
            imports = self._top_imports(os.path.join(SCRIPTS, fn))
            extra = imports - STDLIB_ALLOWED - LOCAL_ALLOWED
            self.assertEqual(extra, set(), f"{fn} imports non-stdlib: {extra}")


if __name__ == "__main__":
    unittest.main()
