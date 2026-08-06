# Templates

Copy-and-fill skeletons for new skills. Placeholders `{{name}}` and
`{{description}}` are replaced with real values. A skill built from the
instructions-only skeleton passes `validate_skill.py` with no ERROR.

## Contents

- Instructions-only SKILL.md (high freedom)
- SKILL.md with scripts (low freedom)
- Gotchas section
- Reference file with table of contents
- Description before / after
- Eval JSON — trigger scenario
- Eval JSON — output scenario with assertions

## Instructions-only SKILL.md (high freedom)

Use when several approaches are valid and the agent should apply judgment.

```markdown
---
name: {{name}}
description: {{description}}
license: MIT
---

# {{name}}

One-paragraph overview of what this skill does and when it applies.

## Instructions

1. Analyze the input.
2. Apply the approach that fits the context (explain *why*, so the agent adapts).
3. Verify the result and iterate until it is correct.

## Gotchas

- Non-obvious, environment-specific facts the agent would get wrong otherwise.

## References

- `references/guide.md` — load this when you need the detailed procedure.
```

## SKILL.md with scripts (low freedom)

Use when the operation is fragile and must run a specific, bundled script.

```markdown
---
name: {{name}}
description: {{description}}
license: MIT
---

# {{name}}

One-paragraph overview.

## Workflow

Copy this checklist and tick items as you go:

- [ ] Step 1: run the analyzer
- [ ] Step 2: validate
- [ ] Step 3: apply

Run exactly this (do not add flags):

    python3 scripts/run.py input.json

## Gotchas

- Environment-specific traps; document script exit codes here.

## References

- `references/guide.md` — detailed procedure, load when needed.
```

## Gotchas section

The highest-value content in many skills — concrete corrections, not general
advice. Keep it in `SKILL.md`, not a reference.

```markdown
## Gotchas

- The `users` table uses soft deletes. Queries must include
  `WHERE deleted_at IS NULL` or results include deactivated accounts.
- The user ID is `user_id` in the DB, `uid` in auth, `accountId` in billing —
  all the same value.
- `/health` returns 200 while the DB is down; use `/ready` for full health.
```

## Reference file with table of contents

Any reference file longer than 100 lines opens like this:

```markdown
# Title

## Contents
- Section one
- Section two

## Section one
...
```

## Description before / after

Prefer imperative "Use when…" addressed to the agent; user intent in third person.

```yaml
# Before — vague, won't trigger reliably
description: Process CSV files.

# After — specific about what, broad about when
description: >
  Analyze CSV and tabular data — summary statistics, derived columns, charts,
  cleaning. Use when the user has a CSV, TSV, or Excel file and wants to explore,
  transform, or visualize it, even if they don't say "CSV" or "analysis."
```

## Eval JSON — trigger scenario

One file per scenario under `evals/`. Tests whether the skill activates. Aim for
at least three scenarios overall: positive triggers, an output-conformance
check, and a negative near-miss (a query that shares keywords but needs
something else).

```json
{
  "skills": ["{{name}}"],
  "query": "A realistic request that should activate the skill",
  "files": [],
  "should_trigger": true,
  "expected_behavior": [
    "First observable behavior",
    "Second observable behavior",
    "Third observable behavior"
  ]
}
```

## Eval JSON — output scenario with assertions

Tests output *quality* once the skill is active. Grade each assertion PASS/FAIL
with concrete evidence, comparing a with-skill run against a without-skill
baseline. See `evaluating.md`.

```json
{
  "skills": ["{{name}}"],
  "query": "A realistic task the skill should perform, with file paths and detail",
  "files": ["evals/files/example.csv"],
  "should_trigger": true,
  "expected_behavior": ["Human-readable description of what success looks like"],
  "assertions": [
    "Objectively checkable statement about the output",
    "Another specific, verifiable claim (countable / programmatic where possible)"
  ]
}
```
