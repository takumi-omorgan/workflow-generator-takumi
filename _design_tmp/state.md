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

PR #81 is open against `main` from branch `accept-adr-044-immutability-exception` (4 commits: ADR-044 status flip + index, CLAUDE.md citation, prompt + state, eval summary). Review and merge #81; ADR-044 becomes the kit-wide authority for mechanical path-string rewrites. After #81 merges: (1) `git checkout main && git pull`, (2) `mv /tmp/adr-045-rename-design-directory-lowercase.md Design/adr/` to restore the ADR-045 draft, (3) `/prepare-issue 80` to draft the prompt for the rename itself, (4) executor → packager chain to ship #80.

<!-- state:continue-here:end -->
