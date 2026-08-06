# Design spec — creating-skills

> Stage-3 artifact. Zero-context implementers build from this. Same `<topic>` slug
> as the brief and plan. Grounded on agentskills.io open standard + the 19
> platform.claude.com best-practices (fetched 2026-08-06).

**Goal:** an agent-agnostic, installable skill `creating-skills` that generates new
spec-conformant skills via a scaffold → fill → validate → fix loop.

**No UI surface** — UX track skipped (`no UI`).

## Global constraints (every task inherits these — exact values, copied to the plan)

- **Runtime:** Python **3.8+**, **standard library only**. No third-party imports,
  no network access at runtime. (`package dependencies` + `avoid assuming tools`.)
- **Skill `name` rule:** `^[a-z0-9]+(-[a-z0-9]+)*$`, length 1–64, not equal to and
  not containing reserved words `anthropic` or `claude`, MUST equal the skill's
  parent directory name.
- **`description` rule:** 1–1024 chars, non-empty, no `<...>` XML-like tags.
- **`SKILL.md` budget:** body **< 500 lines** AND **< 5000 tokens** (token estimate =
  `ceil(chars / 4)`, documented as approximate).
- **References:** exactly **one level** below the skill root (`references/x.md`, not
  `references/a/b.md`); no link may escape the skill dir (`../`).
- **TOC rule:** any file in the skill **> 100 lines** must contain a `## Contents`
  heading.
- **Paths:** forward slashes only in all docs/scripts.
- **MCP refs:** fully-qualified `Server:tool_name`.
- **Style:** consistent terminology; the term is **"skill"**, the file is
  **"SKILL.md"**, the check tool is **"validator"**, the generator is
  **"scaffolder"**. No time-sensitive info outside an "Old patterns" block.
- **Layout root:** the skill lives at `skills/creating-skills/`; tests at
  `tests/`; `README.md` at repo root.

## File layout (what each file owns)

```
creating-skills/                      (repo root)
├── README.md                         # install (per-agent) + usage + zero-deps
├── skills/creating-skills/
│   ├── SKILL.md                      # trigger + 6-step workflow + load pointers
│   ├── references/
│   │   ├── best-practices.md         # all 19 sections + ## Contents TOC
│   │   ├── checklist.md              # judgment-only items, mapped to sections
│   │   └── templates.md              # SKILL.md skeletons + eval JSON template
│   ├── scripts/
│   │   ├── new_skill.py              # scaffolder (stdlib only)
│   │   └── validate_skill.py         # validator (stdlib only)
│   └── evals/
│       ├── trigger-invoice-parser.json
│       ├── conformance-generated-skill.json
│       └── negative-nearmiss.json
├── tests/
│   ├── test_validate_skill.py
│   ├── test_new_skill.py
│   └── test_structure.py             # references/evals structural + dogfood
└── docs/superpowers/...              # pipeline artifacts (already present)
```

## Contract: `scripts/validate_skill.py`  — covers: REQ-001, REQ-007, REQ-008

CLI: `python3 validate_skill.py <skill_dir>`
Exit: **0** if no ERROR findings (WARN allowed); **1** if any ERROR; **2** on usage
error (dir missing). Prints one line per finding: `ERROR: <msg>` / `WARN: <msg>`,
then a summary `PASS`/`FAIL`. `--json` optional flag emits findings as a JSON list.

Internal API (importable, stdlib only — so tests call functions directly):

```python
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body). Minimal YAML: key: value lines between
    leading '---' fences. No third-party YAML. Missing fences -> ({}, text)."""

def estimate_tokens(text: str) -> int:
    """ceil(len(text) / 4) — documented approximation."""

def validate_skill(skill_dir: str) -> list[Finding]:
    """Finding = namedtuple('Finding', 'level code message')  # level in {ERROR,WARN}"""
```

ERROR checks (each gets a distinct `code`, probed both ways in tests):
1. `no-skill-md` — `SKILL.md` absent.
2. `no-name` / `no-description` — frontmatter field missing/empty.
3. `name-charset` — fails `^[a-z0-9]+(-[a-z0-9]+)*$`.
4. `name-length` — > 64 chars.
5. `name-reserved` — contains `anthropic` or `claude`.
6. `name-dir-mismatch` — `name` ≠ basename of `skill_dir`.
7. `desc-length` — > 1024 chars.
8. `desc-xml` — matches `<[^>]+>`.
9. `body-lines` — body ≥ 500 lines.
10. `body-tokens` — `estimate_tokens(body)` ≥ 5000.
11. `ref-nesting` — a markdown link target under the skill resolves > 1 dir deep.
12. `ref-escape` — a link target contains `../`.
13. `toc-missing` — a `.md` file in the skill > 100 lines lacking `## Contents`.

WARN checks (reported, exit stays 0):
- `windows-path` — a backslash path `\w+\\\w+` in any `.md`.
- `time-sensitive` — regex `\b(before|after|as of)\b.*\b(20\d\d)\b` in `SKILL.md`.
- `mcp-unqualified` — a `use the <tool> tool` mention without a `Server:` prefix
  (heuristic; documented as advisory).
- `desc-first-person` — description contains `\bI \b` / `\bYou \b` / `\bWe \b`.

Robustness: never raises on malformed input — a parse failure becomes an ERROR
finding (`code=frontmatter-unparseable`), not a traceback. (`solve, don't punt`.)

## Contract: `scripts/new_skill.py`  — covers: REQ-006

CLI: `python3 new_skill.py <name> [--desc TEXT] [--with-scripts] [--dest DIR]`
- `<name>` validated with the same regex + reserved-word rule as the validator
  (shared function `is_valid_name(name)` — defined here, imported by the validator
  to keep one source of truth). Invalid → `stderr` message + exit **1**.
- Creates `<dest>/<name>/` (default `dest=.`). **Refuses** if it exists (exit 1).
- Writes `SKILL.md` from the instructions-only template (or the with-scripts
  template if `--with-scripts`), substituting `{{name}}` and `{{description}}`
  (default desc placeholder if `--desc` omitted).
- Creates `references/` and `assets/`; `scripts/` only with `--with-scripts`.
- Prints: `Created <path>. Next: python3 .../validate_skill.py <path>`. Exit 0.

Shared module: `is_valid_name` and the reserved-word set live in
`validate_skill.py`; `new_skill.py` imports them (`from validate_skill import
is_valid_name`). Single source of truth — no duplicated regex.

## Contract: `references/best-practices.md`  — covers: REQ-003

- Opens with `## Contents` TOC listing all sections (file is > 100 lines).
- Contains an addressable subsection for **each of the 19** named practices, in the
  operator's order. Each: 2–6 lines, the rule + the concrete do/don't, no filler.
- Section anchors (kebab) MUST include, verbatim, these 19 keys (tested):
  `naming-conventions`, `writing-effective-descriptions`,
  `progressive-disclosure`, `avoid-deeply-nested-references`,
  `table-of-contents`, `workflows-and-feedback-loops`, `implement-feedback-loops`,
  `avoid-time-sensitive-information`, `use-consistent-terminology`,
  `evaluation-and-iteration`, `solve-dont-punt`, `provide-utility-scripts`,
  `use-visual-analysis`, `create-verifiable-intermediate-outputs`,
  `package-dependencies`, `runtime-environment`, `mcp-tool-references`,
  `avoid-assuming-tools-are-installed`, `token-budgets`.

## Contract: `references/checklist.md`  — covers: REQ-004

Pre-ship checkbox list. Each item references the section it enforces. Covers the
judgment-only practices the validator cannot decide: solve-don't-punt, no magic
constants, package deps listed, MCP fully-qualified, don't-assume-installed,
visual-analysis (where inputs render), evals-first (≥3), no time-sensitive info,
degree-of-freedom match, test on target models. Plus a "run the validator" item.

## Contract: `references/templates.md`  — covers: REQ-005

`## Contents` TOC (file > 100 lines). Sections:
1. **SKILL.md — instructions-only** skeleton (high freedom).
2. **SKILL.md — with-scripts** skeleton (low freedom, references a script).
3. **Reference file TOC** template.
4. **Eval JSON** template: `{"skills":[...],"query":"...","files":[...],
   "expected_behavior":["...","...","..."]}`.
Round-trip guarantee: a skill scaffolded from template 1 passes `validate_skill.py`.

## Contract: `SKILL.md` (of creating-skills itself)  — covers: REQ-001, REQ-002

- Frontmatter: `name: creating-skills`; `description` third-person, ≤1024, states
  what (generates conformant skills) + when (triggers: "make a skill", "new skill",
  "create a skill", "написать скилл"…); `license: MIT`; `metadata.version: "0.1.0"`.
- Body < 500 lines / < 5000 tokens: the 6-step workflow with a **copyable
  checklist**; ≥3 `references/*` pointers each with a stated load-trigger; a short
  inline Gotchas section; the two script invocations.

## Contract: `README.md`  — covers: REQ-010

Sections: what it is; **zero-deps / agent-agnostic statement**; install for
**Claude Code**, **Cursor**, **Codex/generic** (copy the `skills/creating-skills/`
folder into the agent's skills dir; or via the open-standard `skills` CLI); usage
example (invoke → scaffold → validate → fix); link to the best-practices reference.

## evals/  — covers: REQ-009

≥3 JSON files matching the eval template: one positive trigger, one
generated-skill-conformance, one negative near-miss (`should_trigger:false`).

## Error handling & degradation

Scripts import stdlib only and never touch the network. Malformed inputs become
findings, not tracebacks. `new_skill.py` refuses destructive overwrites. Token
count is explicitly approximate and documented as such.

## Testing approach  — covers: REQ-011

`python3 -m unittest discover -s tests`. Suites:
- `test_validate_skill.py` — every ERROR check both ways (clean fixture → no
  finding; planted-defect fixture → the specific `code`); WARN checks fire on
  planted input; exit codes 0/1/2 asserted via `subprocess`.
- `test_new_skill.py` — scaffold to a temp dir → `validate_skill.validate_skill`
  returns no ERROR; invalid name → exit 1; existing dir → exit 1.
- `test_structure.py` — best-practices.md has all 19 anchors + TOC; templates.md
  round-trip validates; checklist items present; **dogfood**:
  `validate_skill(skills/creating-skills)` returns no ERROR; **import-scan**: AST of
  both scripts imports only stdlib modules.

## Self-review (done inline)

- REQ coverage: every REQ 001–011 appears in a `covers:` above ✓; no section
  without a REQ ✓.
- No placeholders / TBD ✓. Names consistent (`validate_skill`, `is_valid_name`,
  `estimate_tokens`, `Finding`) across contracts ✓.
- Scope = one implementable module ✓. Ambiguities resolved (token estimate defined;
  shared name-validation source named) ✓.
```
