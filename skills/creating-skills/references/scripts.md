# Designing scripts for agentic use

Load this reference when a generated skill bundles a `scripts/` directory or
tells the agent to run commands. An agent reads a script's stdout/stderr to
decide what to do next, so scripts must be designed for that. Method condensed
from [agentskills.io/skill-creation/using-scripts](https://agentskills.io/skill-creation/using-scripts).

## Contents

- When to inline a command vs bundle a script
- Referencing bundled scripts
- Self-contained scripts (declare deps inline)
- Rules for agent-friendly scripts

## When to inline a command vs bundle a script

If an existing tool already does the job, reference it directly — no `scripts/`
needed. Many ecosystems auto-resolve dependencies at runtime:

```bash
uvx ruff@0.8.0 check .        # Python, via uv (isolated, cached)
pipx run 'ruff==0.8.0' check .  # Python, broader OS availability
npx eslint@9 --fix .          # Node, ships with npm
```

- **Pin versions** (`npx eslint@9.0.0`) so behavior is stable over time.
- **State prerequisites** in `SKILL.md` ("Requires Node.js 18+") or the
  `compatibility` frontmatter field — don't assume the environment has them.
- **Move complex commands into a script.** When a command grows too fiddly to
  get right first try, a tested script in `scripts/` is more reliable.

## Referencing bundled scripts

Use **relative paths from the skill root** — the agent resolves them
automatically, no absolute paths. List the scripts so the agent knows they
exist, then instruct it to run them:

```markdown
## Available scripts
- `scripts/validate.sh` — validates configuration files
- `scripts/process.py` — processes input data

## Workflow
1. `bash scripts/validate.sh "$INPUT_FILE"`
2. `python3 scripts/process.py --input results.json`
```

The same relative-path convention holds in `references/*.md` — execution paths
in code blocks are relative to the skill root, since the agent runs from there.

## Self-contained scripts (declare deps inline)

For reusable logic, bundle a script that declares its own dependencies inline,
so it runs with one command and no separate install step. Python via
[PEP 723](https://peps.python.org/pep-0723/):

```python
# /// script
# dependencies = ["beautifulsoup4>=4.12,<5"]
# ///
from bs4 import BeautifulSoup
...
```

Run with `uv run scripts/extract.py` (creates an isolated env, installs deps,
runs) or `pipx run`. Deno (`npm:`/`jsr:` specifiers), Bun (versioned imports),
and Ruby (`bundler/inline`) have equivalents. Pin versions in every case.

Prefer this over assuming packages are present — but note the strongest
portability is still **zero-dependency, standard-library** scripts (as this
skill's own `scripts/` demonstrate): they run even where there is no network.

## Rules for agent-friendly scripts

- **Never block on interactive prompts.** This is a hard requirement — agents
  run in non-interactive shells and a TTY prompt hangs forever. Take input via
  flags, env vars, or stdin; on missing input, exit with a clear usage error.
- **Document the interface with `--help`** — a brief description, the flags, and
  usage examples. It's how the agent learns the script. Keep it concise; it
  enters the context window.
- **Write helpful error messages** — say what went wrong, what was expected, and
  what to try. "Error: --format must be one of json, csv, table. Received: xml"
  beats "Error: invalid input".
- **Use structured output** — JSON/CSV/TSV over free-form text, so both the
  agent and tools like `jq`/`cut` can consume it. Send **data to stdout,
  diagnostics to stderr** so the agent captures clean parseable output.
- **Be idempotent** — agents retry; "create if not exists" beats "fail on
  duplicate".
- **Meaningful, documented exit codes** — distinct codes for distinct failures
  (not-found vs bad-args vs auth), listed in `--help`.
- **`--dry-run` for destructive ops**, and consider requiring `--confirm` /
  `--force`.
- **Predictable output size** — harnesses truncate large tool output (often
  10–30K chars). Default to a summary or limit, support `--offset`/`--output` so
  the agent can opt into more.
- **Solve, don't punt** — handle errors in the script rather than pushing raw
  crashes to the agent; justify every constant (no unexplained `TIMEOUT = 47`).
