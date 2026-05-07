
# ADR-006: Use issue-by-issue, plan-first Claude Code execution

**Status:** accepted
**Date:** 2026-04-12

## Context

The strongest part of your current workflow is the disciplined implementation model: work is scoped through GitHub issues, Claude Code reads the relevant project context, proposes a plan before editing, writes tests alongside code, and produces an evaluation summary at the end. This reduces scope creep and makes AI-assisted development more reviewable and auditable.

## Options considered

### Option A: Use broad, flexible Claude Code sessions without strict issue structure

- Pros: lower ceremony, faster for tiny tasks.
- Cons: more context drift, weaker traceability, harder review, and less reliable testing discipline.

### Option B: Use issue-by-issue, plan-first execution

- Pros: clearer scope, better testing discipline, stronger traceability to ADRs and issues, and cleaner PRs.
- Cons: slightly more structure for the user.

## Decision

Adopt an **issue-by-issue, plan-first execution model** for v1. Claude Code should be guided by:

- project docs,
- relevant ADRs,
- a filled issue prompt,
- explicit plan approval before edits,
- tests written before or alongside implementation,
- and a final evaluation summary.

## Consequences

- The workflow remains disciplined and reviewable.
- The kit needs a strong issue prompt template and `CLAUDE.md` conventions.
- Pull requests become easier to review because they map cleanly to issues and ADRs.
- The product favors reliable, incremental delivery over ad hoc AI coding sessions.
