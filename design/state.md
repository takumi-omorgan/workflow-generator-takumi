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
- **Branch:** issue-084-phase2-body-slimming
- **Status:** verified

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

Phase 2 of issue #84 is **fully shipped on branch** `issue-084-phase2-body-slimming` (6 commits: 4 per-skill lifts + CSV re-score + eval). Branch is unpushed. All 19 cohort skills now under both 500L and 5k-token thresholds. Eval at `notes/eval-issue-084.md` (overwrites Phase 1's; Phase 1 content preserved in git at `6aefd6d`). **Next:** run `/pr-review-packager` — it will halt at preflight asking for `git push -u origin issue-084-phase2-body-slimming` first (per kit's standing rule). After PR opens, partial-shipped flip on `notes/refactoring-ideas.md` entry #9 is post-merge bookkeeping (suggested format in eval doc); don't fully mark `shipped-#PR` until Phase 3 ships. Phase 3 (sidecar consistency: `examples.md` → `example.md` rename, `complete-milestone`/`milestone-summary` policy) is the smallest of the three and is the only remaining phase against #84.

<!-- state:continue-here:end -->
