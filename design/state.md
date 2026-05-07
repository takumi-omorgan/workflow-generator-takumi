# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #80 — Rename design/ → design/ kit-wide for root-directory casing consistency
- **Prompt:** `prompts/issue-080-rename-design-directory-lowercase.md`
- **Branch:** n/a
- **Status:** prepared

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception
- #77 — none — persist eval summary for issue #71
- #76 — none — add infra verb to pr-review-packager classifier
- #75 — ADR-043 — bin/check-plan programmatic surface for chain points
- #74 — ADR-041 — auto-mode permission contract for strict-mode skill operations

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

PR #81 merged (squash, 3e2d290 on main). ADR-044 is now `accepted` with tightened 6-criterion mechanical-rewrite definition (per pre-merge review feedback). ADR-045 restored from /tmp to `design/adr/`. Prompt for #80 written and gate-passed at `prompts/issue-080-rename-design-directory-lowercase.md`. Next: `/claude-issue-executor prompts/issue-080-rename-design-directory-lowercase.md`. The executor session is **clearly significant** per ADR-039 (3+ files, all 19 SKILL.md, templates/, bin/, 16 ADR bodies) — it will request plan-mode entry before proposing the plan. After PR for #80 merges, mark refactoring-ideas entry #7 as `shipped`.

<!-- state:continue-here:end -->
