# Pipeline retro — creating-skills project

One file per project. Stage 0 reads the standing instructions **in full** next run.

## Standing instructions (hard cap: 10)

> Pruned every run against three retirement triggers: it became a mechanical check ·
> the paths/commands it names are gone · it hasn't fired in five run stamps.

| # | Instruction | Added | Last fired |
|---|---|---|---|
| 1 | When building a parser/validator, test **adversarial** inputs both ways before shipping: non-UTF8 bytes, YAML block scalars (`>` / `\|`), and characters that look like markup (`<`, `>`, `\`). Trusting the happy-path parser lets malformed input bypass a hard rule. | 2026-08-06 | 2026-08-06 |

## Run log

| Stamp | Task | Diverged? |
|---|---|---|
| 2026-08-06 | creating-skills — agent-agnostic skill that creates skills | yes |

## Entries (only when a run diverged)

### 2026-08-06 — validator did not honor its "never raises / hard-rule" contract until review

- **Symptom:** the validator crashed with `UnicodeDecodeError` on non-UTF8 files, and
  a folded/literal-YAML `description` bypassed the ≤1024 and no-XML hard rules; the
  `desc-xml` ERROR also false-fired on comparison operators (`x < y`).
- **Surfaced at:** stage 5 (independent code review).
- **Owned by:** stage 3 (spec) — it locked the rules but not the parser's handling of
  encoding and YAML block scalars, so stage 5 built to the happy path.
- **Root cause:** the frontmatter parser was written for well-formed scalar input;
  the hard-rule checks trusted whatever it returned.
- **Fix (grade: mechanical check):** block-scalar + encoding handling added; regexes
  tightened to real tags/paths; both-ways tests for every adversarial input. Also
  promoted to standing instruction #1 so the class is caught at design next time.
- **Catches it next time:** `tests/test_validate_skill.py::Regressions` +
  standing instruction #1 read at stage 0.
