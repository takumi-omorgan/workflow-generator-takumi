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
- **Branch:** examples-issue-prompt-cleanup
- **Status:** verified

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

PR #90 merged (squash `0a261e0`); issue #89 closed and `notes/refactoring-ideas.md` entry #8 marked `shipped-#90`. `prompts/_template.md` now carries the self-documenting placeholder mapping table — the sequencing dependency that held back #91 is resolved. Issue #91 prepared and ready for execution against this clean base: `notes/refactoring-ideas.md` entry #12 (`examples/*.md` broken refs to the deleted issue-prompt files), prompt at `prompts/issue-091-examples-prompt-cleanup.md`, ~3 files / ~9 link edits, docs-only, no ADR. Next: run `/claude-issue-executor prompts/issue-091-examples-prompt-cleanup.md` in a fresh session.

<!-- state:continue-here:end -->
