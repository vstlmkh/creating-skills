# Acceptance — creating-skills

Date: 2026-08-06 · Model: Opus 4.8 (1M) · Single repository (no submodules).

## Ladder walk (ran before the coverage table)

Each REQ walked bottom-up: decision → spec section → contract + failure behavior →
task → change → executed test → surface/docs. Findings ordered by seam.

- **Seam spec→change (contract "never raises"):** stage-5 review found the validator
  crashed on non-UTF8 and folded-YAML descriptions bypassed the ≤1024 rule — the
  contract at design-spec L102/L60 was not fully realized in code. **Closed** in fix
  round 1 (commit `fix: resolve stage-5 review findings`), each with a both-ways test.
- **Seam task→test (REQ-009):** the eval deliverable existed but its promised
  automated check did not. **Closed** — `tests/test_structure.py::Evals` added.
- **Seam change→surface (scaffold output):** generated skills shipped a dangling
  `references/guide.md` link. **Closed** — scaffolder now writes the stub.
- No absence found that required a **new** REQ row.

Axis-rotation counts — **new findings this pass: 0; findings caused by this run's own
fixes: 0.** (All substantive findings surfaced at the stage-5 review; the ladder walk
confirmed their closure and found nothing new. Axis not exhausted; none needed.)

Checks-seen-failing: every validator ERROR/WARN check has a paired test that plants a
defect and asserts the specific code fires (`ErrorChecksBothWays`, `WarnChecks`,
`Regressions`) — i.e. each check was observed catching a planted defect.

## REQ coverage

| REQ | Status | Evidence |
|---|---|---|
| REQ-001 conformance/dogfood | verified | `validate_skill.py skills/creating-skills` → `PASS`; `test_structure.py::Dogfood.test_skill_validates_itself` |
| REQ-002 SKILL.md workflow | verified | `skills/creating-skills/SKILL.md` (6-step copyable checklist, 3 ref pointers w/ load-triggers, Gotchas); passes budget checks in dogfood |
| REQ-003 best-practices 19+TOC | verified | `test_structure.py::BestPractices` (all 19 keys + `## Contents`) |
| REQ-004 checklist | verified | `references/checklist.md`; `test_structure.py::Checklist` |
| REQ-005 templates round-trip | verified | `test_structure.py::TemplatesRoundTrip` (skeleton → validate no ERROR) |
| REQ-006 new_skill.py | verified | `test_new_skill.py` (scaffold conformant; bad/reserved name exit 1; existing dir exit 1) |
| REQ-007 validate_skill.py | verified | `test_validate_skill.py` — 13 ERROR + 4 WARN codes both ways, exit 0/1/2 |
| REQ-008 agnostic/stdlib | verified | `test_structure.py::ImportScan` (stdlib only); install-copy simulation validates `PASS`; scripts use no agent API |
| REQ-009 evals ≥3 | verified | 3 JSON evals; `test_structure.py::Evals` (count ≥3 + schema) |
| REQ-010 README | verified | `README.md` — what/why, zero-deps, install for Claude Code/Cursor/Codex/generic, usage |
| REQ-011 suite green | verified | `python3 -m unittest discover -s tests` → `Ran 52 tests … OK` (cold run) |

**11/11 verified. 0 partial, 0 deferred, 0 dropped, 0 unknown.**

## Carry-over ledger status

8 rows. Deferrals (plugin wrapper, Cursor shim, npm publish, external push) all
operator-agreed at stage 0. Recommendations (obsidian-wiki, code graph, docs/wiki)
not installed — offered, none a gate. **0 unresolved rows.**

## Repository close-out (single repo)

- No submodules (`git submodule status` empty).
- Working tree clean; `master` holds the merged work.
- No remote configured (brief: no outward publish this run) — nothing to push.
