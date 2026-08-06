# Evaluating skill output quality

Triggering (see `descriptions.md`) decides *whether* the skill loads; this
decides *whether it helps* once loaded. Load this reference for Step 5 when you
want more than a smoke test. Method condensed from
[agentskills.io/skill-creation/evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills).

## Contents

- Designing test cases
- The with-skill / without-skill baseline
- Writing assertions
- Grading with evidence
- Aggregating and analyzing
- Human review
- The iteration loop

## Designing test cases

A test case has a **prompt** (a realistic user message), an **expected output**
(human-readable description of success), and optional **input files**. Store
them in `evals/evals.json` in the skill dir:

```json
{
  "skill_name": "csv-analyzer",
  "evals": [
    {
      "id": 1,
      "prompt": "I have a CSV of monthly sales in data/sales_2025.csv. Find the top 3 months by revenue and make a bar chart.",
      "expected_output": "A bar chart image of the top 3 months by revenue, with labeled axes and values.",
      "files": ["evals/files/sales_2025.csv"]
    }
  ]
}
```

Start with **2–3 cases** — don't over-invest before the first results. Vary
phrasing and detail, cover at least one edge/boundary case, and use realistic
context (paths, column names). Don't define pass/fail checks yet; add them after
you see what the first run produces.

## The with-skill / without-skill baseline

Run each case **twice**: once with the skill, once without it (the baseline).
Without a baseline you can't tell whether the skill added value or the model
would have succeeded anyway. When improving an existing skill, snapshot the old
version and use that as the baseline instead of "no skill".

Give each run a **clean context** (a subagent or fresh session) so it follows
only what `SKILL.md` says, not leftover development state. Organize outputs per
iteration:

```
csv-analyzer-workspace/iteration-1/
  <eval-name>/with_skill/{outputs,timing.json,grading.json}
  <eval-name>/without_skill/{outputs,timing.json,grading.json}
  benchmark.json
```

Capture **timing** (`total_tokens`, `duration_ms`) per run — a skill that
triples tokens for a 2-point gain is a different trade-off than one that's
better and cheaper.

## Writing assertions

Assertions are verifiable statements about the output — add them *after* seeing
the first outputs, because you often don't know what "good" looks like until the
skill has run. Good: "The output file is valid JSON", "The chart has labeled
axes", "The report includes ≥3 recommendations". Weak: "The output is good"
(unverifiable), "uses exactly the phrase 'Total Revenue: $X'" (too brittle).
Reserve assertions for objectively checkable things; leave style/polish to human
review.

## Grading with evidence

Grade each assertion PASS/FAIL **with concrete evidence** quoting the output —
never benefit of the doubt. A section titled "Summary" containing one vague
sentence FAILS "includes a summary". Use a script for mechanical checks (valid
JSON, row counts, file exists) — more reliable and reusable than model judgment.
While grading, also fix assertions that are too easy, too hard, or unverifiable.

## Aggregating and analyzing

Compute per-configuration pass rate / time / tokens into `benchmark.json`, and a
`delta` between with- and without-skill. Then dig past the averages:

- **Drop assertions that pass in both** — they don't reflect skill value.
- **Investigate assertions that fail in both** — broken assertion or too-hard
  case.
- **Study assertions that pass with the skill but fail without** — this is where
  the skill earns its keep; understand *why*.
- **Inconsistent across runs (high stddev)** → the eval is flaky or the
  instructions are ambiguous; add examples / tighten wording.
- **Time/token outliers** → read that run's transcript for the bottleneck.

## Human review

Assertions only check what you thought to write. A human catches
technically-correct-but-misses-the-point outputs and hard-to-express issues.
Record specific, actionable feedback per case ("missing axis labels; months in
alphabetical not chronological order"), empty when the output looked fine.

## The iteration loop

Three signals drive improvement: failed **assertions** (specific gaps), human
**feedback** (broader quality), and execution **transcripts** (*why* it went
wrong). Hand all three plus the current `SKILL.md` to a model and ask for
changes, instructing it to: **generalize** (fix the underlying issue, not the
one example), **keep it lean** (remove instructions transcripts show are
wasted; if pass rates plateau while rules grow, it's over-constrained), **explain
the why** ("do X because Y causes Z" beats "ALWAYS do X"), and **bundle repeated
work** (if every run reinvents the same helper, put it in `scripts/`). Apply,
rerun in a new `iteration-N+1/`, regrade, review. Stop when satisfied, feedback
is consistently empty, or gains stall.
