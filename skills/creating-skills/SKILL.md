---
name: creating-skills
description: Generates new, spec-conformant agent skills on request, applying the Agent Skills open standard and the 19 skill best-practices through a scaffold-fill-validate-fix loop. Use when the user wants to create, author, scaffold, or write a new skill ("make a skill", "new skill", "create a skill", "написать скилл", "сделать скилл"), or when an existing skill folder must be checked against the standard. Works on any agent that reads the open-standard SKILL.md format.
license: MIT
metadata:
  version: "0.1.0"
---

# creating-skills

Create new skills that conform to the Agent Skills open standard and follow the 19
best-practices. The method is a feedback loop: scaffold a folder, fill it in from
templates, run the validator, and fix findings until it reports `PASS`.

The scripts use the Python standard library only — no install, no network.

## Workflow

Copy this checklist and tick each item as you complete it:

```
Skill creation:
- [ ] Step 1: Intake — settle name, description, and whether scripts are needed
- [ ] Step 2: Scaffold — run new_skill.py
- [ ] Step 3: Fill — write SKILL.md and references from the templates
- [ ] Step 4: Validate — run validate_skill.py
- [ ] Step 5: Fix — resolve every ERROR, then re-validate until PASS
- [ ] Step 6: Evals — add at least three eval scenarios
```

**Step 1 — Intake.** Ask only what the request leaves open: a name (prefer gerund
form, e.g. `processing-pdfs`), a one-to-two sentence description covering *what* and
*when*, and whether the skill needs utility scripts. Keep it short.

**Step 2 — Scaffold.** Create the folder with a valid stub:

```bash
python3 scripts/new_skill.py <name> [--desc "..."] [--with-scripts] [--dest DIR]
```

The name is validated up front; an invalid or reserved name exits non-zero.

**Step 3 — Fill.** Write the real `SKILL.md` and any reference files using
[references/templates.md](references/templates.md). Keep the body small and push
deep material into `references/`.

**Step 4 — Validate.** Check conformance:

```bash
python3 scripts/validate_skill.py <dir>
```

It prints one line per finding and a `PASS`/`FAIL` summary. ERROR findings mean the
skill is non-conformant; WARN findings are advisory.

**Step 5 — Fix.** Resolve every ERROR and re-run the validator until it passes. This
loop is the point — do not ship on a `FAIL`.

**Step 6 — Evals.** Add at least three eval scenarios (positive trigger, output
conformance, negative near-miss). See the eval template in
[references/templates.md](references/templates.md).

## Gotchas

- The `name` must equal the folder name, be lowercase `[a-z0-9-]`, and must not
  contain the reserved words `anthropic` or `claude`.
- The `description` cap is 1024 characters and applies to that field alone; write it
  in the third person.
- The `SKILL.md` body budget is under 500 lines and under ~5000 tokens (the token
  count is an approximation). Split content into references before it grows past that.
- Keep references one level deep; a reference file over 100 lines needs a
  `## Contents` table of contents.

## References

- [references/best-practices.md](references/best-practices.md) — the 19 practices in
  full; load it when deciding how to structure a skill or what a rule means.
- [references/checklist.md](references/checklist.md) — the pre-ship checklist of
  judgment-only items; run through it before shipping.
- [references/templates.md](references/templates.md) — SKILL.md and eval skeletons;
  load it during Step 3.
