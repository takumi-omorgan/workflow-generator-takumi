
# ADR-019: Write docs/claude-code-guide.md for kit usage guidance

**Status:** accepted
**Date:** 2026-04-17

## Context

`docs/install.md` references `docs/claude-code-guide.md` as "a later issue" — promised but not yet written. After installation, users lack guidance on how to use Claude Code with the kit: when to use plan mode, how to invoke skills, how the approve-then-implement loop works, and common pitfalls. This gap leaves new users guessing at the intended interaction model.

## Options considered

### Option A: Single standalone doc

- Pros: one place to look, easy to link from install output and CLAUDE.md.
- Cons: may overlap slightly with the workflow guide.

### Option B: Fold into workflow-guide.md

- Pros: fewer files.
- Cons: mixes tool-specific guidance with process guidance, harder to find.

### Option C: Leave at per-skill SKILL.md files and drop the reference

- Pros: no new file.
- Cons: scattered, no overview of the interaction model, breaks the promise in install.md.

## Decision

Write a single standalone `docs/claude-code-guide.md` covering plan mode, skill invocation via `/skill-name`, the approve-then-implement loop, and common pitfalls (e.g., running destructive commands, forgetting to stage files). The doc links to but does not duplicate the workflow guide or individual SKILL.md files.

## Consequences

- New users have a clear starting point after install.
- The broken reference in `docs/install.md` is resolved.
- Aligns with the execution model defined in ADR-006.
- Must be kept in sync when new skills are added, though it covers patterns rather than an exhaustive skill list.
