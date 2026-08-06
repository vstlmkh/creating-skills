# creating-skills — implementation plan

> **For agentic workers:** execute task-by-task under the task-pipeline stage-5
> build doctrine — TDD per task (failing test → watch fail → minimal impl → watch
> pass → commit), a review with three verdicts after each. Steps use `- [ ]`.

**Goal:** an agent-agnostic, installable skill `creating-skills` that generates
spec-conformant skills via scaffold → fill → validate → fix.

**Architecture:** one skill at `skills/creating-skills/` (SKILL.md + references/ +
scripts/ + evals/), tests at `tests/`, README at repo root. Two stdlib-only Python
scripts: a validator (source of truth for name rules) and a scaffolder that imports
from it.

**Tech stack:** Python 3.8+ stdlib only; Markdown; `unittest`.

**Spec:** docs/superpowers/specs/2026-08-06-skill-creator-design.md

## Global constraints

- Python 3.8+, **standard library only**, no network at runtime.
- `name`: `^[a-z0-9]+(-[a-z0-9]+)*$`, 1–64 chars, no `anthropic`/`claude`, == parent dir.
- `description`: 1–1024 chars, non-empty, no `<...>` tags.
- `SKILL.md` body < 500 lines AND < 5000 tokens (tokens = ceil(chars/4), approx).
- references one level deep; no `../` escape; any skill `.md` > 100 lines needs `## Contents`.
- forward slashes only; MCP refs `Server:tool_name`; consistent terms (skill / SKILL.md / validator / scaffolder).
- Layout: `skills/creating-skills/`, `tests/`, root `README.md`.

## Execution order

| Group | Tasks | Runs after |
|---|---|---|
| A | 1, 3, 4, 7, 8 | — |
| B | 2, 5 | A |
| C | 6 | B |
| D | 9 | C |

File ownership is disjoint within every group.

---

### Task 1: validator — `scripts/validate_skill.py`
**Depends:** — · **Implements:** REQ-007 (validator), REQ-001 (conformance mechanism), REQ-008 (stdlib-only)
**Files:** Create `skills/creating-skills/scripts/validate_skill.py`, `tests/test_validate_skill.py`
**Interfaces — Produces:** `is_valid_name(name)->bool`, `RESERVED={'anthropic','claude'}`,
`parse_frontmatter(text)->(dict,str)`, `estimate_tokens(text)->int`,
`Finding(level,code,message)`, `validate_skill(skill_dir)->list[Finding]`; CLI exit 0/1/2, `--json`.
**DoD:** all 13 ERROR codes + 4 WARN codes implemented per spec; never raises on
malformed input (→ `frontmatter-unparseable` ERROR); tests assert each ERROR both
ways and exit codes via subprocess; `python3 -m unittest tests.test_validate_skill` green.

- [ ] Step 1: write failing tests for `is_valid_name` (valid, bad charset, reserved, >64) and `validate_skill` on a clean fixture (no ERROR) + a planted-defect fixture per code.
- [ ] Step 2: run → FAIL (module missing).
- [ ] Step 3: implement validator (stdlib: `re`, `os`, `sys`, `json`, `math`, `collections`).
- [ ] Step 4: run → PASS.
- [ ] Step 5: `git commit -m "feat: skill validator with 13 error + 4 warn checks"`.

### Task 3: `references/best-practices.md`
**Depends:** — · **Implements:** REQ-003
**Files:** Create `skills/creating-skills/references/best-practices.md`
**DoD:** `## Contents` TOC; one addressable subsection per each of the 19 keys
(exact kebab anchors from spec); each 2–6 lines; file > 100 lines.
- [ ] Step 1: write the 19 sections from the fetched best-practices + TOC.
- [ ] Step 2: verify all 19 anchor keys present (grep). Step 3: commit.

### Task 4: `references/checklist.md`
**Depends:** — · **Implements:** REQ-004
**Files:** Create `skills/creating-skills/references/checklist.md`
**DoD:** checkbox list; judgment-only items (solve-don't-punt, magic constants,
package-deps, MCP fully-qualified, don't-assume-installed, visual-analysis,
evals-first, no-time-sensitive, degree-of-freedom, test-on-models, run-validator),
each naming its section.
- [ ] Step 1: write checklist. Step 2: commit.

### Task 7: `evals/`
**Depends:** — · **Implements:** REQ-009
**Files:** Create 3 JSON files under `skills/creating-skills/evals/`
**DoD:** ≥3 valid JSON files matching the eval template (positive trigger,
generated-skill conformance, negative near-miss with `should_trigger:false`).
- [ ] Step 1: write 3 evals. Step 2: `python3 -c "import json"` parse-check each. Step 3: commit.

### Task 8: `README.md`
**Depends:** — · **Implements:** REQ-010
**Files:** Create `README.md` (repo root)
**DoD:** sections: what it is; zero-deps/agent-agnostic statement; install for
Claude Code, Cursor, Codex/generic (copy folder or skills CLI); usage example;
link to best-practices reference.
- [ ] Step 1: write README. Step 2: commit.

### Task 2: scaffolder — `scripts/new_skill.py`
**Depends:** [1] · **Implements:** REQ-006
**Files:** Create `skills/creating-skills/scripts/new_skill.py`, `tests/test_new_skill.py`
**Interfaces — Consumes:** `is_valid_name`, `RESERVED` from `validate_skill`.
**DoD:** CLI `new_skill.py <name> [--desc] [--with-scripts] [--dest]`; scaffolds
folder + SKILL.md from template; refuses existing dir (exit 1); invalid name exit 1;
scaffolded skill passes `validate_skill()` with no ERROR; tests green.
- [ ] Step 1: failing tests (scaffold temp → validate no ERROR; bad name exit 1; existing dir exit 1).
- [ ] Step 2: run → FAIL. Step 3: implement (import from validate_skill; embed minimal template inline or read templates.md). Step 4: run → PASS. Step 5: commit.

### Task 5: `references/templates.md`
**Depends:** [1] · **Implements:** REQ-005
**Files:** Create `skills/creating-skills/references/templates.md`
**DoD:** `## Contents` TOC; 4 sections (SKILL.md instructions-only, SKILL.md
with-scripts, reference TOC template, eval JSON template); a skill built from the
instructions-only skeleton passes `validate_skill()`.
- [ ] Step 1: write templates. Step 2: round-trip check with validator. Step 3: commit.

### Task 6: `SKILL.md`
**Depends:** [2,3,4,5] · **Implements:** REQ-001 (self-conformance), REQ-002
**Files:** Create `skills/creating-skills/SKILL.md`
**DoD:** valid frontmatter (name `creating-skills`, ≤1024 3rd-person desc with
triggers, `license: MIT`, `metadata.version "0.1.0"`); body < 500 lines / < 5000
tokens; the 6-step copyable workflow; ≥3 `references/*` pointers with load-triggers;
inline Gotchas; both script invocations. `validate_skill(skills/creating-skills)` no ERROR.
- [ ] Step 1: write SKILL.md. Step 2: run validator on it → PASS. Step 3: commit.

### Task 9: structural tests + dogfood + suite green
**Depends:** [6] · **Implements:** REQ-011, REQ-008 (import-scan), REQ-001 (dogfood)
**Files:** Create `tests/test_structure.py`
**DoD:** tests — best-practices.md has all 19 anchors + TOC; templates.md round-trip
validates; checklist items present; dogfood `validate_skill(skills/creating-skills)`
no ERROR; import-scan via `ast` proves both scripts import stdlib only. Full suite
`python3 -m unittest discover -s tests` green.
- [ ] Step 1: write structural tests. Step 2: run full suite → PASS. Step 3: commit.

## Self-review
- **REQ set equality:** union of Implements = {001,002,003,004,005,006,007,008,009,010,011} = brief REQ set ✓.
- Every spec contract maps to a task ✓. No placeholders ✓. Names consistent
  (`validate_skill`, `is_valid_name`, `estimate_tokens`, `Finding`, `RESERVED`) ✓.
- Parallel safety: Group A tasks own disjoint files; B (new_skill.py+test vs
  templates.md) disjoint; C, D singletons ✓.
