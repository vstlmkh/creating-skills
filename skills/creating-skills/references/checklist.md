# Pre-ship checklist

Run this before shipping a generated skill. The **validator** (`validate_skill.py`)
covers the mechanical rules automatically; the items below are the judgment-only
practices it cannot decide. Each links to its section in `best-practices.md`.

## Grounding and scope

- [ ] **Grounded in real expertise** — built from a real task or project
  artifacts, not the model's general knowledge — `ground-in-real-expertise`.
- [ ] **Coherent scope** — one unit of work; not so narrow that skills must
  co-load, not so broad it won't trigger precisely — `design-coherent-units`.
- [ ] **Earns its context** — every instruction is something the agent would get
  wrong without it; no filler explaining what a PDF/HTTP is — `spend-context-wisely`.

## Always

- [ ] **Run the validator** and get `PASS` with no ERROR — `python3 scripts/validate_skill.py <dir>`.
- [ ] **Description** states what AND when, imperative "Use when…", user intent
  in third person, real trigger terms — `writing-effective-descriptions`.
- [ ] **Calibrated control** — freedom (with *why*) for open steps, exact
  prescription for fragile ones; defaults not menus; approach over answer —
  `calibrate-control`, `provide-defaults-not-menus`, `procedures-over-declarations`.
- [ ] **Gotchas section** present in SKILL.md for non-obvious, environment-specific
  traps — `gotchas-sections`.
- [ ] **Consistent terminology** — one term per concept throughout — `use-consistent-terminology`.
- [ ] **No time-sensitive info** in the main body; superseded guidance under "Old patterns" — `avoid-time-sensitive-information`.

## Evals and testing

- [ ] **At least three evals** exist and were written before extensive docs — `evaluation-and-iteration`.
- [ ] **Baseline measured** — output evaluated with the skill AND without it, so
  the skill's value is demonstrated, not assumed — `evaluation-and-iteration`.
- [ ] **Description triggering** checked with should-/should-not-trigger queries — `optimize-descriptions`.
- [ ] Tested with each model you plan to run on (Haiku / Sonnet / Opus).
- [ ] **Refined from real execution traces**, not just final outputs — `refine-with-execution`.

## For skills with scripts

- [ ] **Designed for agentic use** — no interactive prompts, `--help`, structured
  stdout / diagnostics to stderr, documented exit codes — `scripts-for-agentic-use`.
- [ ] **Solve, don't punt** — scripts handle errors explicitly; no bare crashes pushed to the agent — `solve-dont-punt`.
- [ ] **No magic constants** — every configuration value is justified in a comment — `solve-dont-punt`.
- [ ] **Package dependencies listed** in SKILL.md and verified available; prefer zero-dep or inline (PEP 723) — `package-dependencies`.
- [ ] **Do not assume tools installed** — install steps are explicit — `avoid-assuming-tools-are-installed`.
- [ ] **MCP tool references** are fully-qualified `Server:tool_name` — `mcp-tool-references`.
- [ ] **Visual analysis** used where inputs can be rendered as images — `use-visual-analysis`.
- [ ] **Verifiable intermediate outputs** for batch/destructive work (plan → validate → execute) — `create-verifiable-intermediate-outputs`.
- [ ] **Run vs read** intent is explicit for each script — `provide-utility-scripts`.

## Structure

- [ ] References are one level deep and linked directly from SKILL.md, each with a stated load trigger — `avoid-deeply-nested-references`, `progressive-disclosure`.
- [ ] Files over 100 lines open with `## Contents` — `table-of-contents`.
- [ ] SKILL.md body under 500 lines / ~5000 tokens; deep material split out — `token-budgets`, `progressive-disclosure`.
