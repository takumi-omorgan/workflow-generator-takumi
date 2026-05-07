# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #79 — Accept ADR-044 and cite mechanical-rewrite immutability exception in CLAUDE.md
- **Prompt:** `prompts/issue-079-accept-adr-044-immutability-exception.md`
- **Branch:** `accept-adr-044-immutability-exception`
- **Status:** verified

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #77 — none — persist eval summary for issue #71
- #76 — none — add infra verb to pr-review-packager classifier
- #75 — ADR-043 — bin/check-plan programmatic surface for chain points
- #74 — ADR-041 — auto-mode permission contract for strict-mode skill operations
- #73 — ADR-040 — cross-skill design-question carry-forward

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

#79 implemented on branch `accept-adr-044-immutability-exception` in three commits: (1) ADR-044 status flip proposed→accepted + index regen, (2) CLAUDE.md one-line citation under the immutability rule, (3) prompt + this state.md. ADR-044 still passes `bin/check-plan --criteria-set adr`. ADR-045 file is moved to `/tmp/adr-045-rename-design-directory-lowercase.md` for the duration of #79's branch — restore to `Design/adr/` for #80's branch. Next: run `/pr-review-packager` to package this branch into a PR (cat-3 explicit-yes gate per ADR-041). After PR merges, restore ADR-045 and run `/prepare-issue 80` for the rename itself.

<!-- state:continue-here:end -->
