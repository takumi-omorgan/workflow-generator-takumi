# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #84 (Phase 2 of 3 — body slimming for 4 over-budget skills)
- **Prompt:** prompts/issue-084-phase2-body-slimming.md
- **Branch:** n/a (executor will create)
- **Status:** prepared

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception
- #77 — none — persist eval summary for issue #71

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

Run `/claude-issue-executor prompts/issue-084-phase2-body-slimming.md` to lift content from 4 over-budget SKILL.md files (`claude-issue-executor` 586L/6.7k, `pr-review-packager` 471L/5.6k, `release` 474L/5.4k, `prepare-issue` 405L/5.2k) into one-level-deep sidecars until each is ≤500L AND ≤5k tokens. Single PR for all 4 skills. Plan-mode required per issue body. Phase 1 (description rewrites) shipped in PR #86; Phase 3 (sidecar consistency) is a separate later session. Audit harness curated subset is now tracked (commit `aafd34b`); `audit.py` is the per-commit verification tool. Rich handoff: `notes/handoff-2026-05-07.md`.

<!-- state:continue-here:end -->
