# Templates

Copy-and-fill skeletons for new skills. Placeholders `{{name}}` and
`{{description}}` are replaced with real values. A skill built from the
instructions-only skeleton passes `validate_skill.py` with no ERROR.

## Contents

- Instructions-only SKILL.md (high freedom)
- SKILL.md with scripts (low freedom)
- Reference file with table of contents
- Eval JSON

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
2. Apply the approach that fits the context.
3. Verify the result and iterate until it is correct.

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

Run exactly:

    python3 scripts/run.py input.json

## References

- `references/guide.md` — detailed procedure, load when needed.
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

## Eval JSON

One file per scenario under `evals/`. Aim for at least three: positive triggers,
a generated-output conformance check, and a negative near-miss.

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
