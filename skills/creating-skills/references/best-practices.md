# Best practices for writing skills

The practices this skill enforces or checks, drawn from the
[Agent Skills open standard](https://agentskills.io/specification) and the
skill-creation guides at agentskills.io:
[best-practices](https://agentskills.io/skill-creation/best-practices),
[optimizing-descriptions](https://agentskills.io/skill-creation/optimizing-descriptions),
[evaluating-skills](https://agentskills.io/skill-creation/evaluating-skills),
and [using-scripts](https://agentskills.io/skill-creation/using-scripts).

Each heading ends with its `kebab-key`. The validator enforces the
mechanically-checkable ones; the rest are judgment calls collected in
`checklist.md`. Deep, load-on-demand method lives in the sibling references
(`descriptions.md`, `evaluating.md`, `scripts.md`).

## Contents

**Part 1 — Before you write: ground the skill**
1. Start from real expertise — `ground-in-real-expertise`
2. Design coherent units — `design-coherent-units`
3. Evaluation and iteration — `evaluation-and-iteration`

**Part 2 — Spend context wisely**
4. Add what the agent lacks — `spend-context-wisely`
5. Progressive disclosure — `progressive-disclosure`
6. Avoid deeply nested references — `avoid-deeply-nested-references`
7. Table of contents for long files — `table-of-contents`
8. Token budgets — `token-budgets`
9. Runtime environment — `runtime-environment`

**Part 3 — Naming and triggering**
10. Naming conventions — `naming-conventions`
11. Writing effective descriptions — `writing-effective-descriptions`
12. Optimize descriptions with trigger evals — `optimize-descriptions`

**Part 4 — Calibrating control**
13. Match specificity to fragility — `calibrate-control`
14. Provide defaults, not menus — `provide-defaults-not-menus`
15. Favor procedures over declarations — `procedures-over-declarations`

**Part 5 — Patterns for effective instructions**
16. Workflows and checklists — `workflows-and-feedback-loops`
17. Implement feedback loops — `implement-feedback-loops`
18. Gotchas sections — `gotchas-sections`
19. Templates for output format — `output-templates`
20. Create verifiable intermediate outputs — `create-verifiable-intermediate-outputs`
21. Use consistent terminology — `use-consistent-terminology`
22. Avoid time-sensitive information — `avoid-time-sensitive-information`
23. Use visual analysis — `use-visual-analysis`

**Part 6 — Scripts**
24. Provide utility scripts — `provide-utility-scripts`
25. Design scripts for agentic use — `scripts-for-agentic-use`
26. Solve, don't punt — `solve-dont-punt`
27. Package dependencies — `package-dependencies`
28. Avoid assuming tools are installed — `avoid-assuming-tools-are-installed`
29. MCP tool references — `mcp-tool-references`

**Part 7 — Refine after shipping**
30. Refine with real execution — `refine-with-execution`

---

## Part 1 — Before you write: ground the skill

### 1. Start from real expertise `ground-in-real-expertise`

The most common failure is asking a model to generate a skill from its general
training knowledge alone. The result is vague filler — "handle errors
appropriately", "follow best practices" — not the specific APIs, edge cases, and
conventions that make a skill worth loading. Effective skills are grounded in
real expertise. Two ways to get it:

- **Extract from a hands-on task.** Do the real task with the agent first,
  correcting and steering it. Then extract the reusable pattern. Capture: the
  steps that worked, the corrections you made ("use X not Y", "check edge case
  Z"), the input/output formats, and the project-specific context the agent
  lacked.
- **Synthesize from project artifacts.** Feed real material — runbooks, style
  guides, API specs, schemas, code-review comments, patches/fixes, past
  incidents — and synthesize from *those*, not from a generic article. The
  point is project-specific source material.

During intake, ask the author for this grounding. A skill with no expertise
behind it is not worth generating.

### 2. Design coherent units `design-coherent-units`

Scoping a skill is like scoping a function: it should encapsulate one coherent
unit of work that composes with others. Too narrow → several skills load for a
single task, risking overhead and conflicting instructions. Too broad → hard to
trigger precisely. "Query a database and format the results" is coherent;
adding "…and administer the database" is doing too much. One skill = one job.

### 3. Evaluation and iteration `evaluation-and-iteration`

Build evals **before** writing extensive docs. Find gaps by running the task
*without* the skill first, then write the minimum content that closes them.
Iterate against observed agent behavior, not assumptions, and test with every
model you plan to run on. The structured method — baseline runs, assertions,
grading — is in `evaluating.md`.

## Part 2 — Spend context wisely

### 4. Add what the agent lacks `spend-context-wisely`

Once a skill activates, its whole `SKILL.md` competes for attention with the
conversation and every other active skill. Focus on what the agent *wouldn't*
know without you: project conventions, domain procedures, non-obvious edge
cases, the specific tool/API to use. Don't explain what a PDF is or how HTTP
works. For each line ask: **"Would the agent get this wrong without this
instruction?"** If no, cut it. If the agent already does the whole task well
unaided, the skill may not be worth having. Aim for moderate detail — concise
stepwise guidance with one working example beats exhaustive documentation,
which makes the agent chase instructions that don't apply.

### 5. Progressive disclosure `progressive-disclosure`

`SKILL.md` is an overview that points to detail on demand. Keep the body small;
push deep material into `references/`, `scripts/`, `assets/`. Always state
**when** to load each file ("read `references/api-errors.md` if the API returns
a non-200"), so a pointer is loaded exactly when relevant — never a bare "see
references/".

### 6. Avoid deeply nested references `avoid-deeply-nested-references`

Keep references **one level deep** from `SKILL.md`; every reference links
directly from it, never reference-to-reference chains. Nested references get
partially previewed and read incompletely.

### 7. Table of contents for long files `table-of-contents`

Any reference file longer than 100 lines opens with a `## Contents` list, so the
agent sees the full scope even when it previews with a partial read.

### 8. Token budgets `token-budgets`

Keep the `SKILL.md` body under 500 lines and under ~5000 tokens. Split past that
into reference files. References and assets cost no context until actually read.

### 9. Runtime environment `runtime-environment`

Skills run in a code-execution environment with a filesystem, bash, and script
execution. Metadata is preloaded; files are read on demand; scripts execute
without loading their source into context. Use descriptive file names, forward
slashes, and organize by domain so the agent loads exactly what it needs.

## Part 3 — Naming and triggering

### 10. Naming conventions `naming-conventions`

Prefer gerund form (`processing-pdfs`, `analyzing-spreadsheets`); noun phrases
(`pdf-processing`) are acceptable. The `name` must be lowercase `[a-z0-9-]`,
1–64 chars, no leading/trailing hyphen, no `--`, and must equal the folder name.
Avoid vague names (`helper`, `utils`, `tools`).

### 11. Writing effective descriptions `writing-effective-descriptions`

The `description` is the only thing the agent sees before loading the skill, so
it carries the entire triggering burden. Write it 1–1024 chars, stating both
**what** the skill does and **when** to use it, with concrete trigger terms —
including contexts where the user never names the domain. Prefer **imperative
phrasing addressed to the agent** — "Use when the user wants to …" — over "This
skill does …": the agent is deciding whether to act, so tell it when to act.
Describe the *user's intent* in the third person; never "I can help you …" /
"You can use this …". Err on the side of being pushy about when it applies.

### 12. Optimize descriptions with trigger evals `optimize-descriptions`

Triggering is testable. Build ~20 labelled queries (half should-trigger, half
should-not, with near-misses), measure the trigger rate over several runs, and
refine the description until it fires when it should and stays quiet when it
shouldn't — without overfitting. Full method (train/validation split,
optimization loop, before/after examples) in `descriptions.md`.

## Part 4 — Calibrating control

### 13. Match specificity to fragility `calibrate-control`

Not every part of a skill needs the same prescriptiveness — match it to the
fragility of the task. **Give freedom** where multiple approaches are valid and
the task tolerates variation; for flexible steps, explaining *why* beats a rigid
directive, because an agent that understands the purpose makes better
context-dependent choices. **Be prescriptive** where operations are fragile,
consistency matters, or an exact sequence is required ("Run exactly this
command. Do not add flags."). Most skills mix both — calibrate each part
independently.

### 14. Provide defaults, not menus `provide-defaults-not-menus`

When several tools or approaches could work, pick one default and mention
alternatives briefly as an escape hatch. "Use pdfplumber; for scanned PDFs use
pdf2image + pytesseract" beats "you can use pypdf, pdfplumber, PyMuPDF, or
pdf2image…". Menus of equal options make the agent chase unproductive paths.

### 15. Favor procedures over declarations `procedures-over-declarations`

Teach *how to approach a class of problems*, not *what to produce for one
instance*. "Read the schema, join on the `_id` convention, apply the user's
filters as WHERE clauses, aggregate and format" generalizes; "join orders to
customers on customer_id where region='EMEA'" only serves one task. Specific
details (output templates, "never output PII", tool-specific commands) are still
valuable — the *approach* is what must generalize.

## Part 5 — Patterns for effective instructions

### 16. Workflows and checklists `workflows-and-feedback-loops`

Break complex operations into clear, numbered steps. For multi-step work provide
a copyable checklist the agent ticks off, especially where steps have
dependencies or validation gates. Explicit steps stop the agent skipping
validation.

### 17. Implement feedback loops `implement-feedback-loops`

Prefer: do the work → run a validator → fix what it reports → repeat until
clean. The "validator" can be a script or a reference the agent checks against.
This lifts output quality more than any amount of prose.

### 18. Gotchas sections `gotchas-sections`

Often the highest-value content in a skill: environment-specific facts that
defy reasonable assumptions — concrete corrections, not general advice. "The
`users` table uses soft deletes; queries must include `WHERE deleted_at IS
NULL`." "`/health` returns 200 even when the DB is down; use `/ready`." Keep
gotchas **in `SKILL.md`**, where the agent reads them before hitting the
situation — it can't know to open a reference about a trap it doesn't know
exists. Every time you have to correct the agent, add the correction here.

### 19. Templates for output format `output-templates`

When the output must follow a specific format, give a template — agents
pattern-match against concrete structures far better than against prose
descriptions. Short templates live inline in `SKILL.md`; long or
case-specific ones go in `assets/` and are referenced so they load only when
needed.

### 20. Create verifiable intermediate outputs `create-verifiable-intermediate-outputs`

For batch, destructive, or high-stakes work use **plan → validate → execute**:
the agent emits a structured plan file, a script validates it against a source
of truth, and only then does it run. Errors surface before anything changes, and
a good error ("Field 'x' not found — available: …") lets the agent self-correct.

### 21. Use consistent terminology `use-consistent-terminology`

One term per concept, everywhere (always "API endpoint", never a mix of
"endpoint / URL / route / path"). Consistency helps the agent parse and follow.

### 22. Avoid time-sensitive information `avoid-time-sensitive-information`

Don't write instructions that expire ("before August 2025, use the old API").
Put superseded guidance under a clearly labelled "Old patterns" section so the
main content stays correct over time.

### 23. Use visual analysis `use-visual-analysis`

When inputs can be rendered as images (a PDF page, a form layout), convert them
and let the agent analyze the image. Vision catches layout and structure that
text extraction loses.

## Part 6 — Scripts

### 24. Provide utility scripts `provide-utility-scripts`

Ship ready scripts for deterministic operations: more reliable than generated
code, they save tokens (the code never enters context), save time, and stay
consistent. State clearly whether the agent should **run** a script or **read**
it as reference — running is preferred for most utilities.

### 25. Design scripts for agentic use `scripts-for-agentic-use`

An agent reads a script's stdout/stderr to decide what to do next, so design for
that: **never block on interactive prompts** (agents run in non-interactive
shells and will hang), document the interface with `--help`, send structured
data (JSON/CSV) to stdout and diagnostics to stderr, use meaningful documented
exit codes, be idempotent, offer `--dry-run` for destructive ops, and keep
output size predictable (summarize or paginate). Full guidance and
self-contained-script recipes (PEP 723, `uvx`/`npx`, version pinning) in
`scripts.md`.

### 26. Solve, don't punt `solve-dont-punt`

In scripts, handle error conditions explicitly rather than returning them for
the agent to sort out. Justify configuration values — no magic constants (a
`TIMEOUT = 47` with no reason is a defect).

### 27. Package dependencies `package-dependencies`

List required packages in `SKILL.md`. Runtimes differ — some install from
npm/PyPI, others have no network. Prefer standard-library / zero-dep scripts so
the skill runs everywhere; verify availability before relying on a package.

### 28. Avoid assuming tools are installed `avoid-assuming-tools-are-installed`

Never assume a package or CLI is present. State the install step, or depend only
on what the runtime guarantees. "Use the pdf library" is a trap; "install
`pypdf`, then …" is safe. Runtime-level requirements belong in the
`compatibility` frontmatter field.

### 29. MCP tool references `mcp-tool-references`

When referencing MCP tools, always use the fully-qualified `Server:tool_name`
form (e.g. `GitHub:create_issue`). Without the server prefix the agent may fail
to find the tool when several MCP servers are connected.

## Part 7 — Refine after shipping

### 30. Refine with real execution `refine-with-execution`

The first draft usually needs work. Run the skill against real tasks and feed
the results — all of them, not just failures — back in. Read the **execution
traces**, not just final outputs: wasted steps usually mean instructions are too
vague (the agent tries several approaches), don't apply (it follows them anyway),
or offer too many options with no default. Even one execute-then-revise pass
noticeably improves quality; complex domains need several.
