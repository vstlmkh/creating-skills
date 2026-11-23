# Kimi Code and Claude Code targets

Load this reference when choosing a target, adding host-specific frontmatter,
using arguments, or referencing bundled files from a generated skill.

## Contents

- Target selection
- Kimi Code
- Claude Code
- Portable output
- Official sources

## Target selection

Use `portable` unless the author explicitly targets one host. Use `kimi` for Kimi
Code CLI and `claude` for Claude Code. All three targets share the Agent Skills
requirements: directory-form `SKILL.md`, a valid `name` and `description`, concise
instructions, and supporting files inside the skill directory.

```bash
python3 scripts/new_skill.py my-skill --target portable
python3 scripts/new_skill.py my-skill --target kimi --with-scripts
python3 scripts/new_skill.py my-skill --target claude --with-scripts

python3 scripts/validate_skill.py my-skill --target kimi
python3 scripts/validate_skill.py my-skill --target claude
```

Do not validate a host-specific result only with the default `portable` profile:
that profile deliberately rejects host-only frontmatter and placeholders.

## Kimi Code

Directory-form skills require both `name` and `description`. Canonical locations:

- User: `$KIMI_CODE_HOME/skills/`, defaulting to `~/.kimi-code/skills/`.
- Shared user: `~/.agents/skills/`.
- Project: `.kimi-code/skills/` or `.agents/skills/` at the project root.
- Extra: directories listed in `extra_skill_dirs` in `config.toml`.

Kimi scans scopes in this priority order: Project > User > Extra > Built-in.
Changes in project source directories reload automatically.

Useful Kimi fields:

| Field | Values / purpose |
| --- | --- |
| `type` | `prompt` (default), `inline`, or `flow`; `flow` is manual-only |
| `whenToUse` | Extra triggering guidance; aliases `when-to-use` and `when_to_use` |
| `disableModelInvocation` | `true` disables automatic invocation; hyphen/underscore aliases exist |
| `arguments` | Named parameters, as a string array or whitespace-separated string |

Kimi expands `$ARGUMENTS`, `$ARGUMENTS[0]`, `$0`, named `$<name>` parameters, and
`${KIMI_SKILL_DIR}`. Use `${KIMI_SKILL_DIR}` for bundled scripts and references so
execution does not depend on the current working directory.

Invoke a Kimi skill manually with `/skill:<name>`; arguments follow the name.
Example: `/skill:review-pr #123`.

## Claude Code

Canonical locations:

- User: `~/.claude/skills/`.
- Project: `.claude/skills/`.
- Plugins: a skill subdirectory inside the plugin.

Useful Claude fields:

| Field | Values / purpose |
| --- | --- |
| `when_to_use` | Extra triggering guidance |
| `argument-hint` | Quoted autocomplete hint, for example `"[issue-number]"` |
| `arguments` | Named positional parameters |
| `disable-model-invocation` | `true` makes the skill manual-only |
| `user-invocable` | `false` hides the skill from manual invocation |
| `allowed-tools` | Tools pre-approved during the invoking turn |

Claude expands `$ARGUMENTS`, `$ARGUMENTS[0]`, `$0`, named `$<name>` parameters,
and `${CLAUDE_SKILL_DIR}`. Use `${CLAUDE_SKILL_DIR}` for bundled files.

Invoke a Claude skill manually with `/<name>`; plugin skills may also have a
plugin namespace. Quote `argument-hint`: an unquoted bracketed value can be parsed
as a YAML flow sequence instead of text.

## Portable output

Portable output uses only these frontmatter fields: `name`, `description`,
`license`, `compatibility`, `metadata`, and `allowed-tools`. Do not use
`${KIMI_SKILL_DIR}` or `${CLAUDE_SKILL_DIR}` in portable output: neither variable
is defined by the open standard. Host fields are allowed only in their matching
profile and must not be required for the core procedure to make sense.

## Official sources

- Kimi Code Agent Skills: https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Agent Skills specification: https://agentskills.io/specification
