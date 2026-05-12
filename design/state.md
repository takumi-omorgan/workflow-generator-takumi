# Claude Code Workflow Kit — State

**Last updated:** 2026-05-08
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #89
- **Prompt:** prompts/issue-089-legacy-prompt-cleanup.md
- **Branch:** legacy-prompt-cleanup
- **Status:** verified

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #88 — none — unify example.md naming and document orchestration-only skills (#84 Phase 3 — closes #84)
- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)
- #86 — none — rewrite 19 SKILL.md descriptions to canonical Use-when shape (#84 Phase 1)
- #85 — none — prune type-3 ADR attributions across 17 SKILL.md files
- #82 — ADR-045 — rename Design/ → design/ kit-wide for root-directory casing consistency

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

Issue #89 prepared: `notes/refactoring-ideas.md` entry #8 (legacy `notes/issue-prompt.md` removal) filed as #89 and the prompt written to `prompts/issue-089-legacy-prompt-cleanup.md`. Path C chosen — collapse the placeholder mapping table from `docs/issue-prompt-guide.md` into `prompts/_template.md`'s existing header, delete the standalone guide, fix four broken references (`docs/README.md:26`, `docs/claude-code-guide.md:147,291`, `docs/workflow-guide.md:1134`), mark the `notes/bug-fixes.md` superseded entry as resolved. Docs-only, no ADR. Next: run `/claude-issue-executor prompts/issue-089-legacy-prompt-cleanup.md` in a fresh session.

<!-- state:continue-here:end -->
