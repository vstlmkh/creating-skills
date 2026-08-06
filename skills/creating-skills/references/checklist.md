# Pre-ship checklist

Run this before shipping a generated skill. The **validator** (`validate_skill.py`)
covers the mechanical rules automatically; the items below are the judgment-only
practices it cannot decide. Each links to its section in `best-practices.md`.

## Always

- [ ] **Run the validator** and get `PASS` with no ERROR — `python3 scripts/validate_skill.py <dir>`.
- [ ] **Description** states what AND when, third person, with real trigger terms — `writing-effective-descriptions`.
- [ ] **Degree of freedom** matches the task: high (prose) for open tasks, low (exact script) for fragile ones.
- [ ] **Consistent terminology** — one term per concept throughout — `use-consistent-terminology`.
- [ ] **No time-sensitive info** in the main body; superseded guidance under "Old patterns" — `avoid-time-sensitive-information`.

## Evals and testing

- [ ] **At least three evals** exist and were written before extensive docs — `evaluation-and-iteration`.
- [ ] Tested with each model you plan to run on (Haiku / Sonnet / Opus).

## For skills with scripts

- [ ] **Solve, don't punt** — scripts handle errors explicitly; no bare crashes pushed to the agent — `solve-dont-punt`.
- [ ] **No magic constants** — every configuration value is justified in a comment — `solve-dont-punt`.
- [ ] **Package dependencies listed** in SKILL.md and verified available; prefer zero-dep — `package-dependencies`.
- [ ] **Do not assume tools installed** — install steps are explicit — `avoid-assuming-tools-are-installed`.
- [ ] **MCP tool references** are fully-qualified `Server:tool_name` — `mcp-tool-references`.
- [ ] **Visual analysis** used where inputs can be rendered as images — `use-visual-analysis`.
- [ ] **Verifiable intermediate outputs** for batch/destructive work (plan → validate → execute) — `create-verifiable-intermediate-outputs`.
- [ ] **Run vs read** intent is explicit for each script — `provide-utility-scripts`.

## Structure

- [ ] References are one level deep and linked directly from SKILL.md — `avoid-deeply-nested-references`.
- [ ] Files over 100 lines open with `## Contents` — `table-of-contents`.
- [ ] SKILL.md body under 500 lines / ~5000 tokens; deep material split out — `token-budgets`, `progressive-disclosure`.
