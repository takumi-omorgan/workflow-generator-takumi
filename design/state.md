# Claude Code Workflow Kit — State

**Last updated:** 2026-05-08
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #91
- **Prompt:** prompts/issue-091-examples-prompt-cleanup.md
- **Branch:** n/a
- **Status:** prepared

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #90 — none — finish legacy notes/issue-prompt.md removal: collapse guide into prompts/_template.md header + fix four broken references (closes #89)
- #88 — none — unify example.md naming and document orchestration-only skills (#84 Phase 3 — closes #84)
- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)
- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

Issue #91 prepared: `notes/refactoring-ideas.md` entry #12 (`examples/*.md` broken refs to deleted issue-prompt files) filed as #91 and prompt written to `prompts/issue-091-examples-prompt-cleanup.md`. Same shape as #89 — docs-only, no ADR, ~3 files / ~9 link edits. **Sequencing dependency:** PR #90 (issue #89) is still open against main; #91's narrative rewrites point at `prompts/_template.md`'s self-documenting header which lands via #90, so the executor should merge #90 first or read the PR-#90 branch's version of `_template.md`. Next: run `/claude-issue-executor prompts/issue-091-examples-prompt-cleanup.md` in a fresh session (and merge PR #90 first for cleanest base).

<!-- state:continue-here:end -->
