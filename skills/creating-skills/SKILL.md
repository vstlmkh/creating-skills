---
name: creating-skills
description: Use when the user wants to create, author, scaffold, write, or improve an agent skill ("make a skill", "new skill", "create a skill", "improve this skill", "написать скилл", "сделать скилл", "улучшить скилл"), or when an existing skill folder must be checked against the standard. Generates spec-conformant skills by grounding in real expertise, then a scaffold → fill → validate → eval → refine loop, applying the Agent Skills open standard and the agentskills.io skill-creation best practices. Works on any agent that reads the open-standard SKILL.md format.
license: MIT
metadata:
  version: "0.2.0"
---

# creating-skills

Create skills that conform to the [Agent Skills open standard](https://agentskills.io/specification)
and follow the agentskills.io skill-creation best practices. The method is a
feedback loop: ground the skill in real expertise, scaffold a folder, fill it in
with calibrated instructions, run the validator, evaluate against a baseline,
and refine from real execution until it holds up.

The scripts use the Python standard library only — no install, no network.

## Workflow

Copy this checklist and tick each item as you complete it:

```
Skill creation:
- [ ] Step 1: Ground — settle name + description, and gather the real expertise
- [ ] Step 2: Scaffold — run new_skill.py
- [ ] Step 3: Fill — write calibrated instructions + a Gotchas section
- [ ] Step 4: Validate — run validate_skill.py, fix every ERROR, re-run until PASS
- [ ] Step 5: Evaluate — evals with a with-skill / without-skill baseline
- [ ] Step 6: Refine — tune the description, refine from real execution traces
```

**Step 1 — Ground.** Two things must be settled before writing anything.

- *Identity.* A `name` (prefer gerund form, e.g. `processing-pdfs`) and a
  description covering **what** and **when**.
- *Expertise.* The most common failure is generating a skill from the model's
  general knowledge alone — the result is vague filler. Ground it in real
  material: either **extract from a hands-on task** the author just did with the
  agent (the steps that worked, corrections made, input/output formats,
  project-specific context) or **synthesize from artifacts** (runbooks, API
  specs, schemas, past fixes/incidents). If the author has neither, that is the
  first thing to get. Ask only what the request leaves open; keep it short.

Also decide **scope** (one coherent unit of work — not so narrow that several
skills must co-load, not so broad it won't trigger precisely) and whether the
skill needs **utility scripts**. If the agent already does the whole task well
unaided, say so — the skill may not be worth building.

**Step 2 — Scaffold.** Create the folder with a valid stub:

```bash
python3 scripts/new_skill.py <name> [--desc "..."] [--with-scripts] [--dest DIR]
```

The name is validated up front; an invalid or reserved name exits non-zero.

**Step 3 — Fill.** Write the real `SKILL.md` and references using
[references/templates.md](references/templates.md). Keep the body small and push
deep material into `references/`, each with a stated "load this when…" trigger.
Three things distinguish a good fill from a mediocre one:

- **Spend context on what the agent lacks.** For each line ask "would the agent
  get this wrong without it?" — if no, cut it. Skip explaining what a PDF or HTTP
  is. Aim for moderate detail with one working example, not exhaustive coverage.
- **Calibrate control to fragility.** Give freedom (and explain *why*) where
  many approaches work; be prescriptive ("run exactly this, don't add flags")
  where the operation is fragile. Provide a default, not a menu of equal
  options. Teach *how to approach* the problem class, not the answer to one
  instance.
- **Write a Gotchas section in `SKILL.md`.** Environment-specific facts that
  defy assumptions (soft-deletes, ID field renames, a lying `/health` endpoint)
  are often the highest-value content. Keep them in the body — the agent can't
  open a reference about a trap it doesn't know exists.

When the skill bundles scripts, design them for agentic use — load
[references/scripts.md](references/scripts.md).

**Step 4 — Validate.** Check conformance:

```bash
python3 scripts/validate_skill.py <dir>
```

It prints one line per finding plus a `PASS`/`FAIL` summary. Resolve every ERROR
and re-run until it passes. WARN findings are advisory. Do not ship on a `FAIL`.

**Step 5 — Evaluate.** Add at least three eval scenarios (a positive trigger, an
output-conformance check, and a negative near-miss) using the templates in
[references/templates.md](references/templates.md). Evals are most useful built
*before* extensive docs: run the task without the skill first to find the gaps.
For output quality, run each case **with the skill and without it** — the
baseline is what tells you the skill added value. When you want the full method
(assertions, evidence-based grading, iteration), load
[references/evaluating.md](references/evaluating.md).

**Step 6 — Refine.** The description carries the entire triggering burden; tune
it with should-trigger / should-not-trigger queries — load
[references/descriptions.md](references/descriptions.md). Then refine the skill
from **real execution traces**, not just final outputs: wasted steps usually
mean instructions are too vague, don't apply, or offer too many options. Every
time you have to correct the agent, add the correction to Gotchas.

## Gotchas

- The `name` must equal the folder name, be lowercase `[a-z0-9-]` (no
  leading/trailing hyphen, no `--`), and must not contain the reserved words
  `anthropic` or `claude`.
- The `description` cap is 1024 characters and applies to that field alone.
  Prefer imperative "Use when…" phrasing addressed to the agent; describe the
  *user's* intent in the third person; never "I can help you…".
- The `SKILL.md` body budget is under 500 lines and under ~5000 tokens (the
  token count is an approximation). Split into references before it grows past.
- Keep references one level deep; a reference file over 100 lines needs a
  `## Contents` table of contents.

## References

- [references/best-practices.md](references/best-practices.md) — the full set of
  practices; load it when deciding how to structure a skill or what a rule means.
- [references/descriptions.md](references/descriptions.md) — the trigger-eval
  method for tuning a description; load it in Step 6.
- [references/evaluating.md](references/evaluating.md) — baseline, assertions,
  and grading for output quality; load it in Step 5 for more than a smoke test.
- [references/scripts.md](references/scripts.md) — designing bundled scripts for
  agentic use; load it in Step 3 when the skill ships scripts.
- [references/checklist.md](references/checklist.md) — the pre-ship checklist of
  judgment-only items; run through it before shipping.
- [references/templates.md](references/templates.md) — SKILL.md and eval
  skeletons; load it during Step 3.
