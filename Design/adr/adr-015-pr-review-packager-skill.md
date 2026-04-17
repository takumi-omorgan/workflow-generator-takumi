
# ADR-015: pr-review-packager skill for automated PR creation

**Status:** proposed
**Date:** 2026-04-17

## Context

After implementation, users manually create pull requests and fill the PR template with issue references, ADR links, and change summaries. This is referenced in `docs/repo-structure.md` but not yet built. The built-in `/review` command reviews existing PRs but does not package new ones. Manual PR creation is slow and inconsistent, especially when the commit history already contains the information needed to populate the template.

## Options considered

### Option A: Skill creates PR end-to-end without approval

- Pros: fastest path from implementation to PR.
- Cons: no review checkpoint, risk of publishing incomplete or incorrect PR descriptions.

### Option B: Skill drafts PR body for approval, then creates

- Pros: user reviews the PR description before it goes live, catches errors early.
- Cons: one extra confirmation step.

### Option C: Keep manual PR creation

- Pros: no development effort.
- Cons: slow, inconsistent, and disconnected from the automated workflow.

## Decision

Build a **/pr-review-packager** skill that drafts the PR body using `templates/pr-template.md` (ADR-005), fills in `Closes #N`, ADR references, and a change summary derived from the commit history, then presents the draft for user approval before creating the PR via `gh pr create`.

## Consequences

- PR descriptions are consistent and always reference the originating issue and ADRs.
- The approval step preserves human oversight without requiring manual template filling.
- Depends on the GitHub-first model (ADR-004) and the template architecture (ADR-005).
- Completes the pipeline: /prepare-issue -> claude-issue-executor -> /pr-review-packager.
