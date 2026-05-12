You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- none — issue is docs-cleanup only. The issue body's `## ADR` section is explicit: "None required. The manual-fill path is being relocated, not retired — guidance moves from a separate doc into the template's own header. No kit convention that target projects depend on changes shape." Plan-first execution per ADR-006 still applies.

GitHub Issue:
- Title: Finish legacy notes/issue-prompt.md removal — collapse guide into template, fix four broken references
- Number: #89
- Milestone: none
- Labels: none

Goal
Finish the partial 2026-05-06 cleanup that deleted `notes/issue-prompt.md` and its sample but left a 118-line standalone guide (`docs/issue-prompt-guide.md`) and four kit-doc references still pointing at them. Collapse the still-useful placeholder-mapping table into `prompts/_template.md`'s existing header comment, delete the standalone guide, and repoint or remove the four broken references.

Why it matters
Four shipped kit docs (`docs/issue-prompt-guide.md` itself; `docs/README.md:26`; `docs/claude-code-guide.md:147,291`; `docs/workflow-guide.md:1134`) currently advertise dead guidance built around files that have been gone from the repo for weeks. Anyone hitting them reads them as live. The valuable salvage is small and well-defined — the placeholder mapping table in `docs/issue-prompt-guide.md:39–50` — and it belongs on `prompts/_template.md` itself (which already has a self-documenting `<!-- How to use this file -->` header). Path C from `notes/refactoring-ideas.md` entry #8 was chosen over Path A (rewrite, two surfaces, drift risk) and Path B (delete with no replacement, would retire manual-fill and warrant an ADR).

Requirements
- Extend `prompts/_template.md`'s `<!-- How to use this file -->` header block with a slimmed placeholder mapping table (target ≤25 lines of new comment text). Adapt from `docs/issue-prompt-guide.md:39–50`. Keep these rows: `PROJECT_NAME`, `ONE_LINE_PROJECT_DESCRIPTION`, `WORKFLOW_DOC_PATH` (default value updated to `docs/workflow-guide.md`), `ADR_FILE`/`ADR_ONE_LINE_SUMMARY`, `PRIMARY_FOLDERS`/`AVOID_FOLDERS`. Drop the GitHub-issue placeholder rows (self-evident) and the `PROJECT_SPECIFIC_CONSTRAINT_OR_DELETE_THIS_LINE` row (the placeholder name explains itself).
- Delete `docs/issue-prompt-guide.md` in its entirety.
- Remove the `issue-prompt-guide.md` row from `docs/README.md`'s doc-index table (currently line 26).
- Update `docs/claude-code-guide.md:147` to reference `prompts/issue-NNN-*.md` (copied from `prompts/_template.md`) instead of "a filled `notes/issue-prompt.md`".
- Remove the `issue-prompt-guide.md` "see also" bullet from `docs/claude-code-guide.md` (≈line 291).
- Update or remove `docs/workflow-guide.md:1134` table row. Removing the row is preferred; if you keep it, point at `prompts/_template.md`.
- Mark the `notes/bug-fixes.md` entry at line 45 as `resolved-#89` (replacing `superseded`) with a one-line closing note.

Acceptance criteria
- `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` from repo root returns zero matches outside `archive/`.
- `docs/issue-prompt-guide.md` does not exist after merge.
- `prompts/_template.md`'s header block contains a placeholder-mapping table covering at minimum: `PROJECT_NAME`, `ONE_LINE_PROJECT_DESCRIPTION`, `WORKFLOW_DOC_PATH`, `ADR_FILE`/`ADR_ONE_LINE_SUMMARY`, `PRIMARY_FOLDERS`/`AVOID_FOLDERS`.
- `docs/README.md`, `docs/claude-code-guide.md`, and `docs/workflow-guide.md` contain no links to `issue-prompt-guide.md` or `notes/issue-prompt.md`.
- The `notes/bug-fixes.md` entry tied to this work is marked `resolved-#89` and the supersession-arrow language is removed.
- No skill behaviour change. Smoke check: `/prepare-issue` and `/claude-issue-executor` still run end-to-end with the new header.
- The PR body cross-references `notes/refactoring-ideas.md` entry #8 (already moved to Filed with this issue number).

Scope and constraints
- Primary folders to touch: `docs/`, `prompts/_template.md`, `notes/bug-fixes.md`.
- Folders to avoid unless absolutely necessary: `archive/` (historical only per CLAUDE.md — references inside archived files stay as-is), `skills/`, `templates/`, `examples/`, `design/`, `bin/`.
- Docs-only — zero skill body or template-logic changes beyond the `prompts/_template.md` header comment expansion. One-shot single PR.

Evaluation & testing requirements
- Run `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` after the edits land and confirm zero matches outside `archive/`. Paste the command output into the evaluation summary.
- Run `grep -n "issue-prompt" docs/README.md docs/claude-code-guide.md docs/workflow-guide.md` and confirm zero hits.
- Smoke-check the template change: `head -50 prompts/_template.md` shows the new placeholder-mapping table; `wc -l prompts/_template.md` reports a sane length (expect ≈130–140 lines, up from 111).
- All existing tests must continue to pass (kit has no automated test runner — docs-only changes covered by the grep checks).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `prompts/_template.md` (current header you'll be extending)
   - `docs/issue-prompt-guide.md` (the file you'll be deleting — read for placeholder-mapping content to salvage)
   - The four reference surfaces: `docs/README.md`, `docs/claude-code-guide.md`, `docs/workflow-guide.md`
   - `notes/bug-fixes.md` (specifically the entry at line 45)
   - `notes/refactoring-ideas.md` entry #8 (origin, Filed section — path-choice context)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the exact placeholder-mapping table you'll add to `prompts/_template.md` (show the new lines in the plan so I can review wording before you write),
   - the exact replacement text for `docs/claude-code-guide.md:147`,
   - the disposition of `docs/workflow-guide.md:1134` (remove vs. repoint),
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the issue (e.g. `docs: collapse issue-prompt guide into template header (#89)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (paste the grep outputs),
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
