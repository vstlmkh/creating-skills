import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "creating-skills", "scripts")
sys.path.insert(0, SCRIPTS)

import validate_skill as V  # noqa: E402

VALID_FM = """---
name: {name}
description: Generates conformant skills. Use when the user asks to create a skill.
license: MIT
---

# {name}

Some concise body content that stays well under budget.
"""


def make_skill(tmp, name="my-skill", skill_md=None, extra_files=None):
    d = os.path.join(tmp, name)
    os.makedirs(os.path.join(d, "references"), exist_ok=True)
    content = skill_md if skill_md is not None else VALID_FM.format(name=name)
    with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(content)
    for rel, body in (extra_files or {}).items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(body)
    return d


def codes(findings):
    return {f.code for f in findings}


class UnitRules(unittest.TestCase):
    def test_is_valid_name(self):
        self.assertTrue(V.is_valid_name("processing-pdfs"))
        self.assertTrue(V.is_valid_name("skill1"))
        self.assertFalse(V.is_valid_name("Bad-Name"))      # uppercase
        self.assertFalse(V.is_valid_name("-lead"))          # leading hyphen
        self.assertFalse(V.is_valid_name("trail-"))         # trailing hyphen
        self.assertFalse(V.is_valid_name("double--hyphen"))  # double hyphen
        self.assertFalse(V.is_valid_name("claude-helper"))   # reserved
        self.assertFalse(V.is_valid_name("x" * 65))          # too long
        self.assertFalse(V.is_valid_name(""))

    def test_estimate_tokens(self):
        self.assertEqual(V.estimate_tokens("abcd"), 1)
        self.assertEqual(V.estimate_tokens("abcde"), 2)  # ceil(5/4)

    def test_parse_frontmatter_ok(self):
        fm, body = V.parse_frontmatter("---\nname: a\ndescription: b\n---\nBODY")
        self.assertEqual(fm["name"], "a")
        self.assertEqual(fm["description"], "b")
        self.assertIn("BODY", body)

    def test_parse_frontmatter_none(self):
        fm, body = V.parse_frontmatter("no frontmatter here")
        self.assertEqual(fm, {})

    def test_parse_frontmatter_unclosed_raises(self):
        with self.assertRaises(ValueError):
            V.parse_frontmatter("---\nname: a\nno closing fence\nBODY")


class ErrorChecksBothWays(unittest.TestCase):
    """Each ERROR code: clean fixture omits it, planted fixture triggers it."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_clean_skill_has_no_errors(self):
        d = make_skill(self.tmp)
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [], f"unexpected errors: {errs}")

    def test_no_skill_md(self):
        d = os.path.join(self.tmp, "empty")
        os.makedirs(d)
        self.assertIn("no-skill-md", codes(V.validate_skill(d)))

    def test_frontmatter_unparseable(self):
        d = make_skill(self.tmp, skill_md="---\nname: x\nnever closed\nbody")
        self.assertIn("frontmatter-unparseable", codes(V.validate_skill(d)))

    def test_no_name_and_no_description(self):
        d = make_skill(self.tmp, skill_md="---\nlicense: MIT\n---\nbody")
        c = codes(V.validate_skill(d))
        self.assertIn("no-name", c)
        self.assertIn("no-description", c)

    def test_name_charset(self):
        d = make_skill(self.tmp, name="Bad_Name")
        self.assertIn("name-charset", codes(V.validate_skill(d)))

    def test_name_length(self):
        long = "a" * 65
        d = make_skill(self.tmp, name=long)
        self.assertIn("name-length", codes(V.validate_skill(d)))

    def test_name_reserved(self):
        d = make_skill(self.tmp, name="claude-tools")
        self.assertIn("name-reserved", codes(V.validate_skill(d)))

    def test_name_dir_mismatch(self):
        # folder is 'my-skill' but frontmatter name is 'other'
        md = VALID_FM.format(name="other")
        d = make_skill(self.tmp, name="my-skill", skill_md=md)
        self.assertIn("name-dir-mismatch", codes(V.validate_skill(d)))

    def test_desc_length(self):
        md = "---\nname: my-skill\ndescription: " + ("x" * 1100) + "\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("desc-length", codes(V.validate_skill(d)))

    def test_desc_xml(self):
        md = "---\nname: my-skill\ndescription: Use <b>this</b> for stuff\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("desc-xml", codes(V.validate_skill(d)))

    def test_body_lines(self):
        body = "\n".join("line" for _ in range(520))
        md = VALID_FM.format(name="my-skill") + body
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("body-lines", codes(V.validate_skill(d)))

    def test_body_tokens(self):
        big = "x" * 21000  # ~5250 tokens, one line -> not caught by body-lines
        md = VALID_FM.format(name="my-skill") + big
        d = make_skill(self.tmp, skill_md=md)
        c = codes(V.validate_skill(d))
        self.assertIn("body-tokens", c)
        self.assertNotIn("body-lines", c)

    def test_ref_nesting(self):
        md = VALID_FM.format(name="my-skill") + "\nSee [x](references/a/b.md)\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("ref-nesting", codes(V.validate_skill(d)))

    def test_ref_escape(self):
        md = VALID_FM.format(name="my-skill") + "\nSee [x](../outside.md)\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("ref-escape", codes(V.validate_skill(d)))

    def test_toc_missing(self):
        big = "# Ref\n" + "\n".join(f"line {i}" for i in range(150))
        d = make_skill(self.tmp, extra_files={"references/big.md": big})
        self.assertIn("toc-missing", codes(V.validate_skill(d)))

    def test_toc_present_ok(self):
        big = "# Ref\n## Contents\n- a\n" + "\n".join(f"line {i}" for i in range(150))
        d = make_skill(self.tmp, extra_files={"references/big.md": big})
        self.assertNotIn("toc-missing", codes(V.validate_skill(d)))


class WarnChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_windows_path_warn(self):
        md = VALID_FM.format(name="my-skill") + "\nRun scripts\\helper.py now\n"
        d = make_skill(self.tmp, skill_md=md)
        f = V.validate_skill(d)
        self.assertIn("windows-path", codes(f))
        self.assertEqual([x for x in f if x.code == "windows-path"][0].level, "WARN")

    def test_time_sensitive_warn(self):
        md = VALID_FM.format(name="my-skill") + "\nBefore August 2025 use the old API.\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("time-sensitive", codes(V.validate_skill(d)))

    def test_mcp_unqualified_warn(self):
        md = VALID_FM.format(name="my-skill") + "\nUse the bigquery_schema tool here.\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("mcp-unqualified", codes(V.validate_skill(d)))

    def test_mcp_qualified_ok(self):
        md = VALID_FM.format(name="my-skill") + "\nUse the BigQuery:bigquery_schema tool.\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertNotIn("mcp-unqualified", codes(V.validate_skill(d)))

    def test_desc_first_person_warn(self):
        md = "---\nname: my-skill\ndescription: I can help you process files\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("desc-first-person", codes(V.validate_skill(d)))


class Regressions(unittest.TestCase):
    """Defects found in stage-5 review; each asserted both ways."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_non_utf8_degrades_gracefully(self):
        d = os.path.join(self.tmp, "my-skill")
        os.makedirs(d)
        with open(os.path.join(d, "SKILL.md"), "wb") as fh:
            fh.write(b"---\nname: my-skill\ndescription: \xff\xfe bad bytes\n---\nbody")
        findings = V.validate_skill(d)  # must not raise
        self.assertIn("frontmatter-unparseable", codes(findings))

    def test_folded_description_is_measured(self):
        long = "x " * 600  # > 1024 chars once folded
        md = f"---\nname: my-skill\ndescription: >\n  {long}\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("desc-length", codes(V.validate_skill(d)))

    def test_folded_description_xml_caught(self):
        md = "---\nname: my-skill\ndescription: >\n  Use <b>bold</b> here\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertIn("desc-xml", codes(V.validate_skill(d)))

    def test_desc_xml_allows_comparison_operators(self):
        md = "---\nname: my-skill\ndescription: Use when x < y and y > 0 holds\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertNotIn("desc-xml", codes(V.validate_skill(d)))

    def test_desc_first_person_ignores_ie(self):
        md = "---\nname: my-skill\ndescription: Extracts fields, i.e. named boxes, from forms\n---\nbody"
        d = make_skill(self.tmp, skill_md=md)
        self.assertNotIn("desc-first-person", codes(V.validate_skill(d)))

    def test_windows_path_ignores_markdown_escape(self):
        md = VALID_FM.format(name="my-skill") + "\nThe field file\\_name is escaped.\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertNotIn("windows-path", codes(V.validate_skill(d)))

    def test_ref_nesting_ignores_assets(self):
        md = VALID_FM.format(name="my-skill") + "\n![logo](assets/img/logo.png)\n"
        d = make_skill(self.tmp, skill_md=md)
        self.assertNotIn("ref-nesting", codes(V.validate_skill(d)))

    def test_metadata_block_still_parsed(self):
        md = ("---\nname: my-skill\ndescription: Valid desc here.\n"
              "metadata:\n  version: \"0.1.0\"\n---\nbody")
        d = make_skill(self.tmp, skill_md=md)
        errs = [f for f in V.validate_skill(d) if f.level == "ERROR"]
        self.assertEqual(errs, [])


class CliExitCodes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.script = os.path.join(SCRIPTS, "validate_skill.py")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, self.script, *args],
                              capture_output=True, text=True)

    def test_exit_0_clean(self):
        d = make_skill(self.tmp)
        r = self.run_cli(d)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("PASS", r.stdout)

    def test_exit_1_error(self):
        d = make_skill(self.tmp, name="Bad_Name")
        r = self.run_cli(d)
        self.assertEqual(r.returncode, 1)
        self.assertIn("FAIL", r.stdout)

    def test_exit_2_usage(self):
        r = self.run_cli(os.path.join(self.tmp, "nope"))
        self.assertEqual(r.returncode, 2)

    def test_json_flag(self):
        d = make_skill(self.tmp)
        r = self.run_cli(d, "--json")
        self.assertEqual(r.returncode, 0)
        import json
        json.loads(r.stdout)  # must be valid JSON


if __name__ == "__main__":
    unittest.main()
