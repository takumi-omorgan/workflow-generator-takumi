# Claude Code Workflow Kit — State

**Last updated:** 2026-05-08
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #84 (Phase 3 of 3 — sidecar consistency; final phase)
- **Prompt:** prompts/issue-084-phase3-sidecar-consistency.md
- **Branch:** n/a (executor will create)
- **Status:** prepared

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)
- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

Run `/claude-issue-executor prompts/issue-084-phase3-sidecar-consistency.md` to ship Phase 3 of issue #84 (final phase): rename `skills/prd-normalizer/examples.md` → `example.md` and decide Option A (add `example.md` to `complete-milestone` and `milestone-summary`) vs Option B (document the orchestration-only exception in `docs/skills.md` with cross-links). Plan-mode required per issue body — Option A vs Option B is the headline plan decision. After this PR ships, issue #84 closes; post-merge bookkeeping flips `notes/refactoring-ideas.md` entry #9 to fully `shipped-#PR`.

<!-- state:continue-here:end -->
