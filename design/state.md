# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #84 (Phase 1 of 3 — description rewrites only)
- **Prompt:** prompts/issue-084-skills-audit-cohort.md
- **Branch:** issue-084-phase1-skills-descriptions
- **Status:** prepared

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception
- #77 — none — persist eval summary for issue #71
- #76 — none — add infra verb to pr-review-packager classifier

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

Run `/claude-issue-executor prompts/issue-084-skills-audit-cohort.md` to ship Phase 1 of issue #84: rewrite all 19 skill description fields to Anthropic's canonical `[what]. Use when [trigger].` template plus boundary clauses for 5 adjacent-skill clusters. Four planned commits on branch `issue-084-phase1-skills-descriptions`: prep (prompt + state.md), the 19-description rewrite, CSV re-score, eval summary. Verification via `python3 notes/skills-audit-2026-05-07/audit.py` and an awk-filter on `skills-audit-judgment-v2.csv`. Phase 2 (body slimming) and Phase 3 (sidecar consistency) explicitly deferred to separate sessions.

<!-- state:continue-here:end -->
