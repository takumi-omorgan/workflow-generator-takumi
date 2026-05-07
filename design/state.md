# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** none
- **Prompt:** n/a
- **Branch:** n/a
- **Status:** none

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency
- #81 — ADR-044 — accept ADR-044 mechanical-rewrite immutability exception
- #77 — none — persist eval summary for issue #71
- #76 — none — add infra verb to pr-review-packager classifier
- #75 — ADR-043 — bin/check-plan programmatic surface for chain points

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

PR #82 opened against `main` from branch `rename-design-directory-lowercase` (14 commits: two-step rename + 8 batched path-string rewrites + ADR status flips + CHANGELOG entry + example-project rename + session orchestration). 217 files changed, 1,473/1,206 +/-. Review and merge #82; v4.0.0 is the natural release version (MAJOR — breaking change). After #82 merges: (1) `git checkout main && git pull` (rebase if needed — same un-pushed-local-commit pattern as the post-#81 merge); (2) edit `notes/refactoring-ideas.md` to move entry #7 from Unfiled to Filed with `shipped-#82` status; (3) optional: run `/release` to cut v4.0.0, which will also fix the CHANGELOG entry's UNRELEASED → date+SHA. The kit no longer has any TitleCase root directory.

<!-- state:continue-here:end -->
