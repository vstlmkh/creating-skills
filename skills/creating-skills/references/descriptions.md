# Optimizing the description

The `description` is the only thing an agent sees before loading a skill, so it
carries the entire triggering burden. An under-specified description won't fire
when it should; an over-broad one fires when it shouldn't. Load this reference
when writing or tuning a description (Step 6 of the workflow). Method condensed
from [agentskills.io/skill-creation/optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

## Contents

- What a good description looks like
- Designing trigger-eval queries
- Measuring the trigger rate
- Train / validation split (avoid overfitting)
- The optimization loop
- Before / after example

## What a good description looks like

- **Imperative phrasing addressed to the agent.** "Use when the user wants to …"
  rather than "This skill does …". The agent is deciding whether to act.
- **User intent, not implementation.** Match what the user asked for, not the
  skill's internal mechanics.
- **Be pushy.** List the contexts where it applies, including ones where the user
  doesn't name the domain — "even if they don't explicitly mention 'CSV' or
  'analysis'."
- **Concise.** A few sentences to a short paragraph. Hard cap 1024 chars — and
  descriptions grow during tuning, so re-check the length.
- One nuance: agents reach for skills mainly on tasks needing knowledge beyond
  what they can do alone. A trivial one-step request may not trigger even a
  perfectly matching description — that is expected.

## Designing trigger-eval queries

Write realistic prompts, each labelled `should_trigger` true or false. Aim for
~20: 8–10 positive, 8–10 negative.

**Should-trigger** — vary phrasing (formal, casual, typos), explicitness (name
the domain vs merely describe the need), detail (terse vs file paths + context),
and complexity (single-step vs multi-step). The most useful positives are ones
where the skill helps but the connection isn't obvious from the query.

**Should-not-trigger** — the valuable ones are **near-misses** that share
keywords but need something different. For a CSV-analysis skill, "update the
formulas in my Excel budget" (needs Excel editing) and "read a CSV and upload
each row to postgres" (needs ETL) are strong negatives; "write a fibonacci
function" tests nothing.

Add realism: file paths (`~/Downloads/report_final_v2.xlsx`), personal context
("my manager asked me to…"), specific column/company names, casual language.

## Measuring the trigger rate

Model behavior is nondeterministic, so run each query several times (3 is a fine
start) and compute a **trigger rate** = fraction of runs where the skill loaded.
A should-trigger query passes if its rate is above a threshold (0.5 default); a
should-not-trigger query passes if below it. Observe triggering via your
client's execution logs / tool-call history. This repo's `evals/*.json` trigger
scenarios (fields `query`, `should_trigger`) are the seed set for exactly this.

## Train / validation split (avoid overfitting)

Optimizing against all queries overfits to their phrasings. Split ~60% train /
~40% validation, each with a proportional mix of positives and negatives; keep
the split fixed across iterations. Use only train failures to guide edits; use
validation only to check whether edits generalize.

## The optimization loop

1. **Evaluate** on both sets.
2. **Identify train failures** — which positives didn't fire, which negatives
   did.
3. **Revise** the description:
   - Missing positives → too narrow; broaden scope / add context on when useful.
   - False positives → too broad; add what the skill does *not* do, clarify the
     boundary with adjacent skills.
   - Don't paste specific keywords from failed queries (overfitting) — address
     the general category they represent.
   - Stuck after a few tries → try a structurally different framing, not tweaks.
   - Re-check the 1024-char limit.
4. **Repeat** until train passes or gains stall (usually ≤5 iterations).
5. **Select the best iteration by validation pass rate** — not necessarily the
   last one produced.

If nothing improves, the queries may be the problem (too easy/hard/mislabelled),
not the description.

## Before / after example

```yaml
# Before
description: Process CSV files.

# After
description: >
  Analyze CSV and tabular data files — compute summary statistics, add derived
  columns, generate charts, and clean messy data. Use when the user has a CSV,
  TSV, or Excel file and wants to explore, transform, or visualize the data,
  even if they don't explicitly mention "CSV" or "analysis."
```

More specific about *what* (stats, derived columns, charts, cleaning), broader
about *when* (CSV/TSV/Excel, even without the keyword).
