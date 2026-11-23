# Changelog

## 0.3.0 — 2026-11-23

### Added

- Kimi Code installation via `--agent kimi`, including `KIMI_CODE_HOME` support.
- Portable, Kimi Code, and Claude Code generation targets via `--target`.
- Host-specific validation for frontmatter fields, Kimi skill types, booleans,
  compatibility length, and skill-directory placeholders.
- Kimi Code and Claude Code platform reference, templates, and project-local
  installation examples.
- Installer and host-target test coverage.

### Changed

- Portable output remains the default and rejects host-only fields and variables.
- Generated descriptions are YAML-quoted for safe punctuation handling.
