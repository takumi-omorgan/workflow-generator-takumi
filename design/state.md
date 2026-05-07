# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #80 — Rename `Design/` → `design/` kit-wide for root-directory casing consistency
- **Prompt:** `prompts/issue-080-rename-design-directory-lowercase.md`
- **Branch:** `rename-design-directory-lowercase`
- **Status:** verified

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

#80 implemented on branch `rename-design-directory-lowercase` in 13 commits: two-step rename via `_design_tmp` (commits 1+2), bulk `sed Design/ → design/` batched by category (commits 3-10), ADR-005 + ADR-045 status flips + ADR-044/045 editorial restoration + index regen (commit 11), CHANGELOG bulk-rewrite + v4.0.0 (UNRELEASED) entry (commit 12), example-project Design/ rename (commit 13). 1,186 → 0 path-string occurrences across 179 files; 14 deliberately-restored editorial `Design/` references remain in ADR-044/045 prose (where the literal old name is the subject of the rename) and CHANGELOG migration snippet. Verification clean: `git ls-files | grep ^Design/` → 0; `find -type d -name Design` → empty; `bin/sync-adr-index --check` → 0; `bin/check-state-cap` → 0; check-plan pass count unchanged from main (24/45 — pre-existing C4 failures on older ADRs preserved). Next: `/pr-review-packager` to package the PR. After merge, mark refactoring-ideas entry #7 as `shipped`.

<!-- state:continue-here:end -->
