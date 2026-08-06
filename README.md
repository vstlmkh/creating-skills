# creating-skills

An **agent-agnostic**, installable skill that generates new, spec-conformant skills
on request — applying the [Agent Skills open standard](https://agentskills.io/specification)
and the [agentskills.io skill-creation best practices](https://agentskills.io/skill-creation/best-practices),
through a ground → scaffold → fill → validate → evaluate → refine loop.

Because it conforms to the [Agent Skills open standard](https://agentskills.io),
the same folder loads on any compliant agent — Claude Code, Cursor, Codex, and
others — with no changes.

## Zero dependencies

The utility scripts use the **Python 3.8+ standard library only**. No `pip install`,
no network access at runtime. If `python3` runs, the skill runs.

## What it does

Given a request like *"make me a skill for parsing invoices"*, it:

1. **Grounds** the skill in real expertise (a hands-on task or project artifacts),
   and settles name, description, and scope.
2. **Scaffolds** a conformant folder with `scripts/new_skill.py`.
3. **Fills** `SKILL.md` from the templates — calibrated instructions, a Gotchas
   section, deep material pushed into `references/`.
4. **Validates** with `scripts/validate_skill.py`, fixing findings until `PASS`.
5. **Evaluates** with at least three evals, including a with-skill / without-skill
   baseline.
6. **Refines** the description (trigger evals) and the skill (real execution traces).

## Install

The skill is the folder `skills/creating-skills/`. Install it by copying that folder
into your agent's skills directory:

### Claude Code
```bash
cp -r skills/creating-skills ~/.claude/skills/creating-skills
```
(or place it under a plugin's `skills/` directory).

### Cursor
```bash
cp -r skills/creating-skills ~/.cursor/skills/creating-skills
```

### Codex / generic agents that support the open standard
```bash
cp -r skills/creating-skills <agent-skills-dir>/creating-skills
```
Or use the open-standard tooling if your setup provides it:
```bash
npx skills add <this-repo-or-path>
```

Any agent that reads the open-standard `SKILL.md` format works — the folder is the
unit of installation.

## Usage

Once installed, just ask your agent to create a skill:

> "Create a skill called `managing-backups` for our nightly backup routine."

The skill activates, scaffolds the folder, fills it in, and validates it. You can
also run the tools directly:

```bash
python3 skills/creating-skills/scripts/new_skill.py managing-backups --with-scripts
python3 skills/creating-skills/scripts/validate_skill.py managing-backups
```

## Reference

- `skills/creating-skills/references/best-practices.md` — the full practice set.
- `skills/creating-skills/references/descriptions.md` — trigger-eval method for
  tuning a description.
- `skills/creating-skills/references/evaluating.md` — baseline + assertions for
  output quality.
- `skills/creating-skills/references/scripts.md` — designing bundled scripts for
  agentic use.
- `skills/creating-skills/references/checklist.md` — pre-ship checklist.
- `skills/creating-skills/references/templates.md` — SKILL.md and eval templates.

## Development

```bash
python3 -m unittest discover -s tests
```

## License

MIT.
