
# ADR-011: issue-planner skill for automated issue creation

**Status:** proposed
**Date:** 2026-04-17

## Context

After the `prd-to-mvp` skill produces an MVP spec and build-out plan, users currently create GitHub issues by hand. This is the most tedious step in the workflow and the one most likely to be skipped. `docs/repo-structure.md:87` lists an issue-planner skill as expected but it has not been built, and no GitHub issue tracks the work yet.

## Options considered

### Option A: Skill creates issues directly via gh

- Pros: fastest path from plan to backlog.
- Cons: no review step; mistakes end up as live issues that need manual cleanup.

### Option B: Skill drafts markdown for review, then creates

- Pros: user can review and edit before anything is published.
- Cons: two-step process may feel slow.

### Option C: Hybrid draft-approve-create

- Pros: combines speed with a safety net — the skill drafts all issues, presents them for approval, then creates approved issues in one batch.
- Cons: slightly more complex implementation.

## Decision

Use the **hybrid approach**. The `issue-planner` skill reads the build-out plan, drafts a set of GitHub issues with titles, bodies, labels, milestones, and ADR references, then presents the batch for user approval. On confirmation it creates the issues via `gh issue create`. This keeps the workflow GitHub-first (ADR-004) and consistent with the execution model (ADR-006) where Claude Code acts but the human approves.

## Consequences

- The gap between planning and execution shrinks to a single skill invocation plus a review step.
- Issues are created with consistent structure, labels, and cross-references.
- The approval gate prevents accidental issue spam.
- The skill depends on `gh` CLI being authenticated, which is already a prerequisite of the kit.
- References: ADR-004 (GitHub-first), ADR-006 (execution model).
