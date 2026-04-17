
# ADR-014: claude-issue-executor skill for disciplined implementation sessions

**Status:** proposed
**Date:** 2026-04-17

## Context

The execution model (ADR-006) describes a plan-first, test-alongside discipline for Claude Code sessions, and `docs/repo-structure.md` references a claude-issue-executor skill, but no such skill exists yet. In v1 the prepared prompt alone guides the session, with no enforcement of branching, incremental commits, or evaluation summaries. As the workflow scales, relying solely on the prompt is insufficient to ensure consistent implementation quality.

## Options considered

### Option A: Full orchestration skill (plan, branch, implement, test, evaluate)

- Pros: enforces the full discipline from ADR-006, produces auditable artifacts at every stage.
- Cons: more complex to build, less flexibility for simple tasks.

### Option B: Lightweight skill (branch + context, then hand off)

- Pros: simpler, still automates the boilerplate.
- Cons: does not enforce plan approval, testing, or evaluation steps.

### Option C: No skill, keep prompt-only approach

- Pros: zero development effort.
- Cons: no enforcement, quality depends entirely on user discipline.

## Decision

Build a **full orchestration skill**. The claude-issue-executor reads the prepared prompt (ADR-013), enters plan mode and proposes a plan for user approval, creates a feature branch, implements with incremental commits that reference the relevant ADR and issue, writes tests alongside code, and produces an evaluation summary at the end.

## Consequences

- The execution model from ADR-006 is enforced by tooling rather than convention alone.
- Each implementation session produces a clean, reviewable commit history tied to a single issue.
- The skill depends on /prepare-issue (ADR-013) having written a prompt file first.
- Pairs with /pr-review-packager (ADR-015) to close the loop from issue to pull request.
