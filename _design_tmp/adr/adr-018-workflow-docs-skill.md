
# ADR-018: workflow-docs skill for target project documentation

**Status:** accepted
**Date:** 2026-04-17

## Context

`docs/repo-structure.md` references a skill that generates `README.md` and `Design/ai-summary.md` for target projects, but no source exists in `skills/`. Projects currently lack auto-generated documentation, so users either write these files by hand or skip them entirely. Both files are important: the README is the public entry point, and the AI summary gives Claude Code fast context on the project.

## Options considered

### Option A: Single skill generating both files

- Pros: one invocation, consistent voice, reads project context once.
- Cons: slightly larger skill, two output files with different audiences.

### Option B: Two separate skills

- Pros: separation of concerns, each skill is small.
- Cons: two commands to remember, duplicated context-reading logic.

### Option C: Fold into the installer script

- Pros: docs created at install time.
- Cons: can only run once, no way to refresh docs as the project evolves.

## Decision

Implement a single `/workflow-docs` skill that reads the PRD, MVP spec, ADRs, and `CLAUDE.md` to generate `README.md` and `Design/ai-summary.md` from templates. The skill is re-runnable so docs can be refreshed as the project evolves. Template variables are filled from project metadata; sections with no source data are omitted rather than left blank.

## Consequences

- Target projects get a README and AI summary with one command.
- The skill must gracefully handle missing inputs (e.g., no ADRs yet) by omitting those sections.
- Aligns with documentation architecture (ADR-005) and the CLAUDE.md template (ADR-007).
