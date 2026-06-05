# Claude Code Workflow Kit — State

**Last updated:** 2026-06-05
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** M5 (roadmap Issues 22–28) — AI PR review integration
- **Prompt:** design/prd-addenda/001-ai-pr-review.md + design/workflow-generator-roadmap-and-issues-20260605.md §M5
- **Branch:** m5-ai-pr-review-integration
- **Status:** implemented; PR open for review (not merged)

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #94 — none — drop dated stub framing from CLAUDE.md (closes #93)
- #92 — none — repoint examples/*.md walk-throughs from deleted issue-prompt files to prompts/issue-NNN-*.md (closes #91)
- #90 — none — finish legacy notes/issue-prompt.md removal: collapse guide into prompts/_template.md header + fix four broken references (closes #89)
- #88 — none — unify example.md naming and document orchestration-only skills (#84 Phase 3 — closes #84)
- #87 — none — bring 4 over-budget SKILL.md files under L2 budget via sidecars (#84 Phase 2)

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

none

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

M5 (AI PR review integration) is implemented on branch `m5-ai-pr-review-integration` and open as a PR for review (do not merge). Adds the `/review-pr` skill, three `bin/*` surfaces (`review-pr`, `publish-review`, `review-eval`), the `ai-review/` prompt pack + config example + eval fixtures, two schemas, ADR-051 (supersedes ADR-046), and PRD addendum 001. Safe by default: review generation posts nothing; publishing needs the deterministic `--confirm publish-pr-N` token and writes a receipt. Deferred: installer distribution of the review tools to target projects, real diff chunking, full-codebase context (see ADR-051 / addendum Open questions). Next after merge: pick the next item from `notes/refactoring-ideas.md` Unfiled, or address the M5 deferrals.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: n/a
preconditions: []
blocked-by: none
```

<!-- state:next-action:end -->
