# Claude Code Workflow Kit — State

**Last updated:** 2026-05-06
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

Last session bundled the post-MVP doc cleanup into a single commit: workflow-guide restructure (new §3 steady-state loop, §4 idea backlog, pruned ADR attributions, text diagram), new `docs/skills.md` functional reference, top-level `archive/` directory with the original methodology docs and phase-1 prompts moved into it, feature-ideas split into `archive/feature-ideas-ledger.md`, and 7 new refactoring entries in `notes/refactoring-ideas.md`. Next session: pick up the next refactoring item from `notes/refactoring-ideas.md` — entries #1-#7 are all queued; the natural first pick is #1 (archive shipped prompts) since it pairs with the archive restructure that just landed.

<!-- state:continue-here:end -->
