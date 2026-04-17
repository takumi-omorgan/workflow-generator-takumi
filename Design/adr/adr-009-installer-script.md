
# ADR-009: Installer script for target project setup

**Status:** accepted
**Date:** 2026-04-17

## Context

Setting up a new project with the workflow kit is currently a manual sequence of `mkdir` and `cp -R` commands documented in `docs/install.md`. This is fine for a single project but becomes tedious as the user starts more projects. `docs/install.md:169` flags an installer script as a Phase 2 candidate. The script should automate the common path while keeping the manual flow available as a fallback.

## Options considered

### Option A: Bash script shipped in the kit

- Pros: no external dependencies, runs anywhere with a POSIX shell, easy to read and modify.
- Cons: limited input validation compared to a higher-level language.

### Option B: curl | bash one-liner

- Pros: zero-clone install.
- Cons: security concerns, harder to version, requires hosting.

### Option C: Claude Code setup skill

- Pros: interactive, can ask clarifying questions.
- Cons: requires Claude Code to already be configured, circular dependency for first-time setup.

### Option D: Keep manual

- Pros: no new code to maintain.
- Cons: friction stays high, inconsistent project structures across installs.

## Decision

Ship a **bash script** at `bin/install-workflow-kit` that scaffolds directories, copies skills into `.claude/skills/`, renders `CLAUDE.md` from the template (ADR-007), creates `prompts/` and `prompts/_template.md` (ADR-008), and makes an initial commit. The manual flow stays documented in `docs/install.md` as a fallback for users who prefer full control.

## Consequences

- New project setup drops from several minutes of copying to a single command.
- The script enforces a consistent directory layout across projects.
- Manual installation remains supported and documented.
- The script must be kept in sync with any changes to the generated file set.
- References: ADR-001 (project-local model), ADR-007 (CLAUDE.md template), ADR-008 (prompts/ folder).
