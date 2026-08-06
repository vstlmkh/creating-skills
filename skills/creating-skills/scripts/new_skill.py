#!/usr/bin/env python3
"""Scaffold a new, spec-conformant skill folder.

Standard library only. Usage:

    python3 new_skill.py <name> [--desc TEXT] [--with-scripts] [--dest DIR]

Name rules are shared with the validator (single source of truth):
`is_valid_name` and `RESERVED` are imported from validate_skill.py.
Exit 0 on success; 1 on invalid name or refusal to overwrite.
"""
from __future__ import annotations

import argparse
import os
import sys

# Same directory as this script — the validator is the source of truth for names.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_skill import is_valid_name  # noqa: E402

DEFAULT_DESC = (
    "Use when ... — describe what this skill does and the concrete situations "
    "that should trigger it. Replace this placeholder."
)

SKILL_TEMPLATE = """---
name: {name}
description: {description}
license: MIT
metadata:
  version: "0.1.0"
---

# {name}

One-paragraph overview of what this skill does and the situations it applies to.

## Instructions

1. First step.
2. Second step.
3. Validate the result and iterate until it is correct.

## Gotchas

- Replace with non-obvious, environment-specific facts the agent would get wrong
  otherwise. Delete this section if the skill genuinely has none.

## References

- `references/guide.md` — load this when you need the detailed procedure.
"""

SCRIPTS_SECTION = """
## Scripts

Run the bundled utility instead of regenerating code:

```bash
python3 scripts/example.py <input>
```
"""

GUIDE_STUB = """# Guide

Detailed procedure for this skill. Replace this stub with the real steps, and load
it from SKILL.md only when the agent needs the full detail.
"""

EXAMPLE_SCRIPT = """#!/usr/bin/env python3
\"\"\"Example utility. Replace with the real script.\"\"\"
import sys


def main(argv):
    print("replace me", argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
"""


def build_skill_md(name: str, description: str, with_scripts: bool) -> str:
    body = SKILL_TEMPLATE.format(name=name, description=description)
    if with_scripts:
        body += SCRIPTS_SECTION
    return body


def scaffold(name, description, with_scripts, dest):
    target = os.path.join(dest, name)
    if os.path.exists(target):
        print(f"ERROR: {target} already exists; refusing to overwrite", file=sys.stderr)
        return 1
    os.makedirs(os.path.join(target, "references"))
    os.makedirs(os.path.join(target, "assets"))
    with open(os.path.join(target, "references", "guide.md"), "w", encoding="utf-8") as fh:
        fh.write(GUIDE_STUB)  # so the SKILL.md reference link resolves from the start
    if with_scripts:
        os.makedirs(os.path.join(target, "scripts"))
        with open(os.path.join(target, "scripts", "example.py"), "w", encoding="utf-8") as fh:
            fh.write(EXAMPLE_SCRIPT)
    with open(os.path.join(target, "SKILL.md"), "w", encoding="utf-8") as fh:
        fh.write(build_skill_md(name, description, with_scripts))
    validator = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_skill.py")
    print(f"Created {target}. Next: python3 {validator} {target}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Scaffold a conformant skill folder.")
    parser.add_argument("name", help="skill name (lowercase, [a-z0-9-], == folder name)")
    parser.add_argument("--desc", default=DEFAULT_DESC, help="skill description")
    parser.add_argument("--with-scripts", action="store_true", help="also create scripts/ and a Scripts section")
    parser.add_argument("--dest", default=".", help="parent directory (default: current)")
    args = parser.parse_args(argv)

    if not is_valid_name(args.name):
        print(
            f"ERROR: invalid name '{args.name}'. Must be lowercase [a-z0-9-], 1-64 chars, "
            "no leading/trailing/double hyphen, and not contain 'anthropic' or 'claude'.",
            file=sys.stderr,
        )
        return 1
    return scaffold(args.name, args.desc, args.with_scripts, args.dest)


if __name__ == "__main__":
    sys.exit(main())
