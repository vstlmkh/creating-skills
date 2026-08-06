#!/usr/bin/env python3
"""Validate a skill folder against the Agent Skills open standard.

Standard library only. No network. Importable (tests call the functions directly)
and runnable as a CLI:

    python3 validate_skill.py <skill_dir> [--json]

Exit codes:
    0  no ERROR findings (WARN findings may be present)
    1  at least one ERROR finding
    2  usage error (skill_dir missing)

The rules enforced here are the mechanically-checkable subset of the best
practices; judgment-only practices live in references/checklist.md.
"""
from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import namedtuple

Finding = namedtuple("Finding", "level code message")

# Single source of truth for name rules — new_skill.py imports these.
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RESERVED = {"anthropic", "claude"}
MAX_NAME = 64
MAX_DESC = 1024
MAX_BODY_LINES = 500
MAX_BODY_TOKENS = 5000
TOC_LINE_THRESHOLD = 100


def is_valid_name(name: str) -> bool:
    """True when name matches the open-standard charset/length and is not reserved."""
    if not name or len(name) > MAX_NAME:
        return False
    if not NAME_RE.match(name):
        return False
    lowered = name.lower()
    return not any(word in lowered for word in RESERVED)


def estimate_tokens(text: str) -> int:
    """Approximate token count. Documented heuristic: ceil(chars / 4)."""
    return math.ceil(len(text) / 4)


def parse_frontmatter(text: str):
    """Return (frontmatter_dict, body).

    Minimal top-level `key: value` YAML between leading `---` fences. Nested
    (indented) keys are ignored — only scalars like name/description are needed.
    No leading fence -> ({}, text). A leading fence with no closing fence raises
    ValueError so the caller can report it as a finding rather than crash.
    """
    stripped = text.lstrip()
    if not stripped.startswith("---"):
        return {}, text
    # Work from the first line that is exactly '---'.
    lines = text.splitlines()
    start = next((i for i, ln in enumerate(lines) if ln.strip() == "---"), None)
    if start is None:
        return {}, text
    end = next((i for i in range(start + 1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("frontmatter opened with '---' but never closed")
    fm = {}
    block = lines[start + 1:end]
    i = 0
    while i < len(block):
        ln = block[i]
        if not ln.strip() or ln[:1] in (" ", "\t"):
            i += 1  # skip blanks and nested/indented keys (e.g. metadata: children)
            continue
        if ":" not in ln:
            i += 1
            continue
        key, _, value = ln.partition(":")
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] in "\"'" and value[-1] == value[0]:
            fm[key] = value[1:-1]
            i += 1
            continue
        # Block scalars ('>' folded, '|' literal, with optional chomping indicators)
        # gather the indented continuation so length/tag rules see the real text.
        if value and value[0] in ">|" and value.strip(">|+-") == "":
            folded = value[0] == ">"
            j, parts = i + 1, []
            while j < len(block) and (not block[j].strip() or block[j][:1] in (" ", "\t")):
                parts.append(block[j].strip())
                j += 1
            fm[key] = (" " if folded else "\n").join(parts).strip()
            i = j
            continue
        fm[key] = value
        i += 1
    body = "\n".join(lines[end + 1:])
    return fm, body


def _iter_markdown(skill_dir: str):
    for root, _dirs, files in os.walk(skill_dir):
        for fn in files:
            if fn.endswith(".md"):
                yield os.path.join(root, fn)


_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# dir\file.ext — a real backslash path, not a markdown escape like file\_name.
_WINDOWS_PATH_RE = re.compile(r"[\w.-]+\\[\w.-]+\.[A-Za-z0-9]+")
_TIME_RE = re.compile(r"\b(?:before|after|as of)\b[^\n]*\b20\d\d\b", re.IGNORECASE)
_MCP_RE = re.compile(r"\buse the (\S+) tool\b", re.IGNORECASE)
# Spec pattern: capitalised first/second person as a word, not "i.e." or "we're".
_FIRST_PERSON_RE = re.compile(r"\b(?:I|You|We)\s")
# An actual HTML/XML tag (open or close), not a bare '<' from "x < y".
_XML_RE = re.compile(r"</?[A-Za-z][^>]*>")


def validate_skill(skill_dir: str) -> list:
    """Return a list of Finding. ERROR findings mean non-conformant."""
    findings = []
    add = findings.append
    skill_dir = os.path.normpath(skill_dir)
    dir_name = os.path.basename(skill_dir)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        add(Finding("ERROR", "no-skill-md", f"SKILL.md not found in {skill_dir}"))
        return findings

    try:
        with open(skill_md, encoding="utf-8") as fh:
            text = fh.read()
    except (UnicodeDecodeError, OSError) as exc:
        add(Finding("ERROR", "frontmatter-unparseable", f"SKILL.md is not readable UTF-8: {exc}"))
        return findings

    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        add(Finding("ERROR", "frontmatter-unparseable", str(exc)))
        return findings

    name = fm.get("name", "").strip()
    desc = fm.get("description", "").strip()

    # name
    if not name:
        add(Finding("ERROR", "no-name", "frontmatter is missing a non-empty 'name'"))
    else:
        if len(name) > MAX_NAME:
            add(Finding("ERROR", "name-length", f"name is {len(name)} chars (max {MAX_NAME})"))
        if not NAME_RE.match(name):
            add(Finding("ERROR", "name-charset", f"name '{name}' must match ^[a-z0-9]+(-[a-z0-9]+)*$"))
        if any(word in name.lower() for word in RESERVED):
            add(Finding("ERROR", "name-reserved", f"name '{name}' contains a reserved word ({', '.join(sorted(RESERVED))})"))
        if name != dir_name:
            add(Finding("ERROR", "name-dir-mismatch", f"name '{name}' must equal the folder name '{dir_name}'"))

    # description
    if not desc:
        add(Finding("ERROR", "no-description", "frontmatter is missing a non-empty 'description'"))
    else:
        if len(desc) > MAX_DESC:
            add(Finding("ERROR", "desc-length", f"description is {len(desc)} chars (max {MAX_DESC})"))
        if _XML_RE.search(desc):
            add(Finding("ERROR", "desc-xml", "description must not contain XML-like <tags>"))
        if _FIRST_PERSON_RE.search(desc):
            add(Finding("WARN", "desc-first-person", "description should be third-person (found I/you/we)"))

    # body budgets
    body_lines = len(body.splitlines())
    if body_lines >= MAX_BODY_LINES:
        add(Finding("ERROR", "body-lines", f"SKILL.md body is {body_lines} lines (must be < {MAX_BODY_LINES})"))
    if estimate_tokens(body) >= MAX_BODY_TOKENS:
        add(Finding("ERROR", "body-tokens", f"SKILL.md body ~{estimate_tokens(body)} tokens (must be < {MAX_BODY_TOKENS}, approx)"))

    # SKILL.md text-level warnings
    for m in _MCP_RE.finditer(body):
        if ":" not in m.group(1):
            add(Finding("WARN", "mcp-unqualified", f"MCP tool ref '{m.group(1)}' should be fully-qualified Server:tool"))
    if _TIME_RE.search(body):
        add(Finding("WARN", "time-sensitive", "SKILL.md contains time-sensitive phrasing (before/after/as of <year>)"))

    # per-file checks across the whole skill
    for path in _iter_markdown(skill_dir):
        rel = os.path.relpath(path, skill_dir)
        try:
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
        except (UnicodeDecodeError, OSError):
            add(Finding("WARN", "file-unreadable", f"{rel} is not readable UTF-8; skipped"))
            continue
        lines = content.splitlines()
        if len(lines) > TOC_LINE_THRESHOLD and "## Contents" not in content:
            add(Finding("ERROR", "toc-missing", f"{rel} is {len(lines)} lines (> {TOC_LINE_THRESHOLD}) and has no '## Contents'"))
        if _WINDOWS_PATH_RE.search(content):
            add(Finding("WARN", "windows-path", f"{rel} contains a backslash path; use forward slashes"))
        for m in _LINK_RE.finditer(content):
            target = m.group(1).split()[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            parts = target.split("/")
            if ".." in parts:
                add(Finding("ERROR", "ref-escape", f"{rel} links outside the skill dir: {target}"))
            elif parts and parts[0] == "references":
                depth = len([p for p in parts[:-1] if p not in ("", ".")])
                if depth > 1:
                    add(Finding("ERROR", "ref-nesting", f"{rel} link '{target}' is more than one level deep"))

    return findings


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    if len(argv) != 1:
        print("usage: validate_skill.py <skill_dir> [--json]", file=sys.stderr)
        return 2
    skill_dir = argv[0]
    if not os.path.isdir(skill_dir):
        print(f"ERROR: not a directory: {skill_dir}", file=sys.stderr)
        return 2

    findings = validate_skill(skill_dir)
    errors = [f for f in findings if f.level == "ERROR"]
    if as_json:
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        for f in findings:
            print(f"{f.level}: [{f.code}] {f.message}")
        print("FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
