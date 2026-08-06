# Task brief — creating-skills (agent-agnostic skill that creates skills)

> Stage-0 intake artifact. Operator confirms before stage 1.

- **Date:** 2026-08-06
- **Task (one line):** Build an agent-agnostic, installable skill named
  `creating-skills` that generates new, spec-conformant skills on user request by
  applying the 19 Anthropic Agent-Skills best-practice sections, with utility
  scripts and a validate/fix feedback loop.
- **UI verdict:** **no** — file/CLI artifact, no GUI surface. super-ux not armed.
- **Platform vs change:** single module (`creating-skills`); no decomposition.
- **Model:** Opus 4.8 (1M) — top tier available; no per-stage overrides.

## Knowledge sources (phase-1 harvest — written BEFORE the first question)

| Source | What it says about this task | Fresh? | Authority | Stale after run? |
|---|---|---|---|---|
| The repo | empty except `.git`; branch `master`; no `CLAUDE.md`/`docs/`; no remote | current | code | no |
| `make-skill` plugin `0.7.1` | encodes the Agent Skills open standard, progressive-disclosure budgets, plugin ref, cross-agent distribution — **reference doctrine, not a dependency** | current | reference | no |
| `make-skill/references/agent-skills-spec.md` | conformance ref: name 1–64 `[a-z0-9-]`==dir; desc ≤1024; SKILL.md <500 lines & <5000 tokens; refs one level deep; TOC >100 lines; `skills-ref validate` upstream | read 2026-08-06 | reference | no |
| agentskills.io open standard | the **agent-agnostic format** — conforming `SKILL.md` loads on Claude/Cursor/Codex/etc. | via ref | spec | no |
| platform.claude.com best-practices (19 sections) | fetched in full 2026-08-06 — the deliverable's contract | fetched 2026-08-06 | spec | no |
| super-ux (installed) | UX chain — N/A (no UI) | current | convention | no |
| CLAUDE.md / CONTEXT.md / docs/ / retro.md | none found — greenfield | — | — | — |
| obsidian-wiki / graphify | not installed | — | — | — |

- **Retro standing instructions:** none (greenfield) — `docs/superpowers/retro.md` created at stage 10.
- **Precedence:** code > host docs/ADRs > wiki > memory. Operator outranks docs, out loud.

## Scope

- **In scope:**
  - A standalone skill `skills/creating-skills/` conforming to the open standard.
  - `SKILL.md` encoding a guided **scaffold → fill → validate → fix** workflow.
  - `references/best-practices.md` (all 19 sections, with TOC),
    `references/checklist.md` (pre-ship conformance), `references/templates.md`
    (SKILL.md skeletons + eval template).
  - `scripts/new_skill.py` (scaffolder) + `scripts/validate_skill.py` (validator),
    **Python 3 stdlib only, zero third-party deps, offline**.
  - `evals/` with ≥3 eval scenarios.
  - `README.md` at repo root: what it is, per-agent install (copy + skills CLI),
    usage, runtime/deps statement.
  - Dogfooding: `creating-skills` passes its own `validate_skill.py`.
  - Test suite via `python3 -m unittest`.
- **Out of scope / deferred:**
  - Claude Code plugin wrapper (`.claude-plugin/`, marketplace) — carry-over.
  - Cursor `.mdc` shim — carry-over.
  - npm/npx package publish — carry-over.
  - External publish (git remote / npm / marketplace) — carry-over; nothing outward this run.

## Requirements (REQ spine)

| ID | Requirement | How it's verified | Status |
|---|---|---|---|
| REQ-001 | `skills/creating-skills/` conforms to the open standard (name==dir, `[a-z0-9-]`, ≤64, no reserved words; desc ≤1024 non-empty 3rd-person; SKILL.md <500 lines & <5000 tok; refs one level; no `../`) | `validate_skill.py skills/creating-skills` exits 0 (dogfood) + unit test | open |
| REQ-002 | SKILL.md encodes the scaffold→validate workflow with a copyable checklist and stated when-to-load pointers (progressive disclosure) | test: checklist block + ≥3 `references/*` pointers present; budget test | open |
| REQ-003 | `references/best-practices.md` condenses all **19** named sections, addressable, with a table of contents (file >100 lines) | test: 19 section anchors present + `## Contents` TOC present | open |
| REQ-004 | `references/checklist.md` covers the judgment-only best-practices (solve-don't-punt, magic constants, package deps listed, MCP `Server:tool`, don't-assume-installed, visual analysis, evals-first, no time-sensitive info) | test: each checklist item maps to a named section | open |
| REQ-005 | `references/templates.md` — SKILL.md skeletons (instructions-only + with-scripts), reference TOC template, eval JSON template | test: a skill scaffolded from template passes `validate_skill.py` | open |
| REQ-006 | `scripts/new_skill.py` scaffolds a conformant folder; rejects invalid/reserved names with non-zero exit; stdlib only | unit test: scaffold temp skill → validate passes; bad name → exit≠0 | open |
| REQ-007 | `scripts/validate_skill.py` enforces the mechanically-checkable rules with specific messages + non-zero exit on failure (name, desc, budgets, ref nesting, `../` escape, Windows paths, time-sensitive warn, TOC>100 lines, MCP fully-qualified) | unit tests probing **each check both ways** + exit-code asserts | open |
| REQ-008 | Agent-agnostic + installable: plain open-standard folder; no agent-specific API; scripts import stdlib only | test: AST import-scan = stdlib only; README grep for per-agent install | open |
| REQ-009 | `evals/` ≥3 scenarios (trigger + conformant-output), evals-first pattern | test: count ≥3 + JSON schema check | open |
| REQ-010 | `README.md` — what/why, per-agent install (copy + skills CLI: Claude Code, Cursor, Codex, generic), usage example, runtime/deps | presence + section review | open |
| REQ-011 | Full test suite green (`python3 -m unittest discover`); scripts covered | suite run output = OK, non-zero on any failure | open |

> **Frozen.** Adding a REQ mid-run is fine (append with source). Removing/narrowing
> needs operator agreement, logged in carry-over.

## Decisions locked

| # | Decision | Chosen | Rationale |
|---|---|---|---|
| 1 | Relationship to make-skill | Fresh standalone skill; make-skill is reference input only | user wants agent-agnostic artifact, not ssheleg-canon plugin |
| 2 | Agent-agnostic mechanism | Conform to agentskills.io open standard; plain folder | the open standard IS the cross-agent format |
| 3 | Behavior | Guided scaffold → fill from templates → validate → fix loop | applies workflows + feedback-loops + verifiable-intermediate-outputs to skill-making |
| 4 | Runtime | Python 3 stdlib only, zero deps, offline | package-deps + don't-assume-installed; python3 near-universal |
| 5 | Layout | `skills/creating-skills/`, README + wrappers room at root | matches make-skill/super-ux shape |
| 6 | Distribution this run | Plain folder + skills CLI, documented per-agent | agnostic core; wrappers deferred |
| 7 | Dogfooding | `creating-skills` passes its own validator | credibility of a skill-maker |
| 8 | 19 sections split | all in best-practices.md; validator enforces checkable subset; rest in checklist | not all 19 are machine-checkable |

## Autonomy sweep

| Stage | Question | Answer |
|---|---|---|
| run-wide | Model | Opus 4.8 (1M); no overrides |
| run-wide | Autonomous vs escalate | Autonomous through gates; escalate only outward actions |
| 0 Harvest | Doc sources beyond repo; stage-9 writes | none beyond repo; no external writes |
| 1 Docs | External libs/APIs | none — stdlib only; spec docs already fetched (agentskills.io, best-practices) |
| 2 Decompose | Platform or module | single module; no decomposition |
| 2–3 Spec | UI verdict | no — UX track skipped |
| 3 Design surface/file | Figma | N/A (no UI) |
| 4–5 Dev | Branch / commit / tracker | branch `build/creating-skills`; conventional commits; TaskList tracker; `master` is integration target |
| 5 Integration | How it lands | local merge to `master`, no PR (no remote); no parallel fan-out |
| 6 Tests | Command / green / coverage | `python3 -m unittest discover -s tests`; green = OK exit 0; scripts covered; no known-red baseline |
| 7 Lint | Lint command | `python3 -m py_compile` on scripts + `validate_skill.py` self-run |
| 7 Deploy | Target / authorization | "deploy" = local install verification (dogfood validate). **No outward publish.** No authorization needed |
| 8 Post-deploy | Where health lives | run validator against the shipped folder + full suite once cold |
| 9 Docs+wiki | Docs updated; wiki; graph | README + skill files; wiki not installed (offer init); no graph |
| 10 Acceptance | Sign-off; deferred tracker; retro | operator signs off; deferrals → carry-over ledger; create `docs/superpowers/retro.md` |

## Done-criteria

- `validate_skill.py skills/creating-skills` exits 0 (dogfood).
- `python3 -m unittest discover` reports OK; every validator check probed both ways.
- README documents install for ≥3 agents + generic, and the zero-deps statement.
- All 11 REQs `verified` with evidence at stage 10; carry-over deferrals agreed.

## Open assumptions / risks

- Token-count in `validate_skill.py` is an estimate (chars/4 heuristic) — flagged as
  approximate; validated against the <5000 budget with margin.
- "Third-person description" and "solve-don't-punt" are partly heuristic — validator
  warns, checklist owns the judgment call.
