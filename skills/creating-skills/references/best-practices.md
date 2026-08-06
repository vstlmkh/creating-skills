# Best practices for writing skills

The 19 practices this skill enforces or checks, condensed from the Agent Skills
open standard and Anthropic's skill best-practices. Each heading ends with its
`kebab-key`. The validator enforces the mechanically-checkable ones; the rest are
in `checklist.md`.

## Contents

1. Naming conventions — `naming-conventions`
2. Writing effective descriptions — `writing-effective-descriptions`
3. Progressive disclosure — `progressive-disclosure`
4. Avoid deeply nested references — `avoid-deeply-nested-references`
5. Table of contents for long files — `table-of-contents`
6. Workflows and feedback loops — `workflows-and-feedback-loops`
7. Implement feedback loops — `implement-feedback-loops`
8. Avoid time-sensitive information — `avoid-time-sensitive-information`
9. Use consistent terminology — `use-consistent-terminology`
10. Evaluation and iteration — `evaluation-and-iteration`
11. Solve, don't punt — `solve-dont-punt`
12. Provide utility scripts — `provide-utility-scripts`
13. Use visual analysis — `use-visual-analysis`
14. Create verifiable intermediate outputs — `create-verifiable-intermediate-outputs`
15. Package dependencies — `package-dependencies`
16. Runtime environment — `runtime-environment`
17. MCP tool references — `mcp-tool-references`
18. Avoid assuming tools are installed — `avoid-assuming-tools-are-installed`
19. Token budgets — `token-budgets`

---

## 1. Naming conventions `naming-conventions`

Prefer gerund form (verb + -ing): `processing-pdfs`, `analyzing-spreadsheets`.
Noun phrases (`pdf-processing`) are acceptable. The `name` must be lowercase
`[a-z0-9-]`, 1–64 chars, no reserved words (`anthropic`, `claude`), and must equal
the skill's folder name. Avoid vague names (`helper`, `utils`, `tools`).

## 2. Writing effective descriptions `writing-effective-descriptions`

The `description` is the only thing the agent sees before loading the skill. Write
it in the **third person**, 1–1024 chars, stating both **what** the skill does and
**when** to use it. Include concrete trigger terms, including contexts where the
user never says the domain word. Avoid "I can help you…" / "You can use this…".

## 3. Progressive disclosure `progressive-disclosure`

`SKILL.md` is an overview that points to detail on demand. Keep the body small;
move deep material into `references/`, `scripts/`, and `assets/`. State **when** to
load each file ("read `references/x.md` before doing Y"), so a pointer is loaded
when relevant, never always or never.

## 4. Avoid deeply nested references `avoid-deeply-nested-references`

Keep references **one level deep** from `SKILL.md`. All reference files link
directly from `SKILL.md`, never reference-to-reference chains. Nested references
get partially previewed (e.g. `head -100`) and read incompletely.

## 5. Table of contents for long files `table-of-contents`

Any reference file longer than 100 lines opens with a `## Contents` list, so the
agent sees the full scope even when it previews with a partial read.

## 6. Workflows and feedback loops `workflows-and-feedback-loops`

Break complex operations into clear, numbered steps. For multi-step work, provide a
copyable checklist the agent ticks off as it goes. Clear steps stop the agent from
skipping validation.

## 7. Implement feedback loops `implement-feedback-loops`

Prefer the pattern: run a validator, fix the errors it reports, repeat until clean.
The "validator" can be a script or a reference document the agent checks against.
This lifts output quality more than any amount of prose instruction.

## 8. Avoid time-sensitive information `avoid-time-sensitive-information`

Do not write instructions that expire ("before August 2025, use the old API").
Put superseded guidance under a clearly labelled "Old patterns" section instead, so
the main content stays correct as time passes.

## 9. Use consistent terminology `use-consistent-terminology`

Pick one term per concept and use it everywhere (always "API endpoint", never a mix
of "endpoint / URL / route / path"). Consistency helps the agent parse and follow
the instructions.

## 10. Evaluation and iteration `evaluation-and-iteration`

Build evals **before** writing extensive docs. Identify gaps by running the task
without the skill, create three scenarios that test those gaps, set a baseline, then
write the minimum content that passes. Iterate against observed agent behavior, not
assumptions. Test with every model you plan to use.

## 11. Solve, don't punt `solve-dont-punt`

In scripts, handle error conditions explicitly rather than returning them for the
agent to sort out. Justify and document configuration values — no magic constants
(a `TIMEOUT = 47` with no reason is a defect).

## 12. Provide utility scripts `provide-utility-scripts`

Ship ready scripts for deterministic operations: they are more reliable than
generated code, save tokens (the code never enters context), save time, and stay
consistent. State clearly whether the agent should **run** a script or **read** it
as reference — running is preferred for most utilities.

## 13. Use visual analysis `use-visual-analysis`

When inputs can be rendered as images (a PDF page, a form layout), convert them and
let the agent analyze the image. Vision helps with layout and structure that text
extraction loses.

## 14. Create verifiable intermediate outputs `create-verifiable-intermediate-outputs`

For batch, destructive, or high-stakes work use plan → validate → execute: the agent
emits a structured plan file, a script validates it against a source of truth, and
only then does it run. Errors surface before anything is changed.

## 15. Package dependencies `package-dependencies`

List required packages in `SKILL.md`. Runtime environments differ: some can install
from npm/PyPI, others have no network at runtime. Prefer standard-library / zero-dep
scripts so the skill runs everywhere; verify availability before relying on a package.

## 16. Runtime environment `runtime-environment`

Skills run in a code-execution environment with a filesystem, bash, and script
execution. Metadata is preloaded; files are read on demand; scripts execute without
loading their source into context. Use descriptive file names, forward slashes, and
organize by domain so the agent can navigate and load exactly what it needs.

## 17. MCP tool references `mcp-tool-references`

When referencing MCP tools, always use the fully-qualified `Server:tool_name` form
(for example, `GitHub:create_issue`). Without the server prefix the agent may fail
to find the tool when several MCP servers are connected.

## 18. Avoid assuming tools are installed `avoid-assuming-tools-are-installed`

Never assume a package or CLI is present. State the install step explicitly, or
depend only on what the runtime guarantees. "Use the pdf library" is a trap; "install
`pypdf`, then …" is safe.

## 19. Token budgets `token-budgets`

Keep the `SKILL.md` body under 500 lines and under ~5000 tokens. When it grows past
that, split content into reference files using progressive disclosure. Reference
files and assets cost no context tokens until they are actually read.
