# Claude Code Workflow Kit — State

**Last updated:** 2026-05-07
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #83
- **Prompt:** prompts/issue-083-prune-adr-attributions.md
- **Branch:** issue-083-prune-adr-attributions
- **Status:** verified

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

Run `/claude-issue-executor prompts/issue-083-prune-adr-attributions.md` to prune 71 high-confidence + 5 medium-confidence type-3 ADR attributions across 17 of 19 SKILL.md files, per the audit harness output at `notes/skills-audit-2026-05-07/adr-attributions.md`. Six planned commits on branch `issue-083-prune-adr-attributions`: prep (prompt + state.md), CLAUDE.md style rule, then four prune batches grouped by audit density. Verification via `python3 notes/skills-audit-2026-05-07/adr-audit.py` after each commit; final `high_conf_count` ≤ 5.

<!-- state:continue-here:end -->
