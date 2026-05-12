<!--
  Draft GitHub issue body for "Finish legacy notes/issue-prompt.md removal — collapse guide into prompts/_template.md and fix four broken references".
  Source: notes/refactoring-ideas.md entry #8.
  Review, then file with: gh issue create --title "..." --body "$(cat this-file.md)"
-->

## Summary

Finish the partial 2026-05-06 cleanup that deleted the legacy manual-fill template `notes/issue-prompt.md` and its worked sample `notes/issue-prompt-sample.md` but left four kit docs still pointing at them, plus a now-orphaned standalone guide (`docs/issue-prompt-guide.md`, 118 lines) built entirely around the deleted file.

Take **Path C** from the entry: collapse the still-useful manual-fill guidance (chiefly the placeholder mapping table) into `prompts/_template.md`'s existing header comment, then delete the standalone guide and repoint or remove the four references. The manual-fill flow remains supported — just relocated onto the template itself so it can't drift out of sync again.

## ADR

None required. The manual-fill path is being **relocated**, not retired — guidance moves from a separate doc into the template's own header. No kit convention that target projects depend on changes shape. Per the kit's ADR test (refactoring-ideas.md preamble: "ADR only when the refactor changes a kit convention that target projects depend on"), this is below the threshold.

## Why

Four shipped kit docs currently contain dead or stale references to a file that has been deleted from the repo for weeks:

- `docs/issue-prompt-guide.md` (whole 118-line guide; line 3 links `../notes/issue-prompt.md`; line 9 links `../notes/issue-prompt-sample.md` — both 404)
- `docs/README.md:26` — table row advertising `issue-prompt-guide.md` as how to "fill `notes/issue-prompt.md` by hand"
- `docs/claude-code-guide.md:147` — narrative step referring to "a filled `notes/issue-prompt.md`"
- `docs/claude-code-guide.md:291` — "see also" list entry pointing at the guide
- `docs/workflow-guide.md:1134` — "Where to look" table row pointing at the guide

Everyone hitting these reads them as live guidance. They aren't.

A `notes/bug-fixes.md` entry was opened for the same problem on 2026-05-06 and marked `superseded — see refactoring-ideas.md entry #8` the same day; the cleanup never landed. This issue finishes it.

The valuable content in `docs/issue-prompt-guide.md` is small and well-defined: the **placeholder mapping table** (lines 39–50) that tells a manual-fill user where each `{{PLACEHOLDER}}` value comes from. The rest (evaluation-summary worked example, "When the plan is wrong" prose) duplicates guidance that already lives in `prompts/_template.md` itself, in ADR-006, or in `/claude-issue-executor`.

`prompts/_template.md` already carries its own `<!-- How to use this file -->` header comment (lines 1–41) — the natural home for the surviving placeholder-mapping content. Self-documenting templates are an established kit pattern.

## Scope

### Path chosen: Path C (collapse-and-delete)

Three paths were considered in refactoring-ideas.md entry #8:

- **Path A** — rewrite `docs/issue-prompt-guide.md` against `prompts/_template.md` (keeps two surfaces; risks future drift again).
- **Path B** — delete `docs/issue-prompt-guide.md` entirely with no replacement (would retire the manual-fill flow; warrants an ADR).
- **Path C** — collapse manual-fill guidance into `prompts/_template.md`'s header, delete the standalone guide (chosen).

Path C eliminates the second surface, keeps the manual-fill flow supported, and puts the guidance where someone using the template would actually find it.

### What gets added to `prompts/_template.md`

Extend the existing `<!-- How to use this file -->` header block with a slimmed placeholder mapping table. Adapt from `docs/issue-prompt-guide.md:39–50`; drop rows whose values are now self-evident from the template body or have shifted under newer ADRs:

- Keep: `{{PROJECT_NAME}}`, `{{ONE_LINE_PROJECT_DESCRIPTION}}`, `{{WORKFLOW_DOC_PATH}}`, `{{ADR_FILE}}`/`{{ADR_ONE_LINE_SUMMARY}}`, `{{PRIMARY_FOLDERS}}`/`{{AVOID_FOLDERS}}`.
- Drop or shorten: the GitHub-issue placeholders (self-evident — copy from the issue); `{{PROJECT_SPECIFIC_CONSTRAINT_OR_DELETE_THIS_LINE}}` (the placeholder name already explains itself).
- Update: `{{WORKFLOW_DOC_PATH}}` row should now point at `docs/workflow-guide.md` as the default (the old guide pointed at `design/build-out-plan.md`, which is per-project rather than per-kit).

Target length for the new block: ≤25 lines of comment text. The template is already 111 lines; keep the header skim-readable.

### What gets deleted

- `docs/issue-prompt-guide.md` — entire file.
- The `notes/issue-prompt-sample.md` reference at `docs/issue-prompt-guide.md:9` — disappears with the guide.

### What gets updated

- `docs/README.md:26` — remove the table row entirely. The doc-index doesn't need a placeholder for a deleted guide.
- `docs/claude-code-guide.md:147` — rewrite the narrative step. Today it says the session starts from "a filled `notes/issue-prompt.md`"; change to refer to "a filled `prompts/issue-NNN-*.md` (copy from `prompts/_template.md`)".
- `docs/claude-code-guide.md:291` — remove the "see also" bullet pointing at the deleted guide.
- `docs/workflow-guide.md:1134` — remove the "Fill a Claude Code session prompt by hand" table row, or replace its right-hand cell with `prompts/_template.md` (the template self-documents now).
- `notes/bug-fixes.md` entry (line 45) — mark `resolved-#NN` (this issue's number) instead of `superseded`.

### What is explicitly left alone

- Per-project `templates/claude-md-template.md` references to target-project `notes/` — those point at downstream-user files, not the kit-internal deleted ones. Already noted as out of scope in the original `bug-fixes.md` entry.
- Archived files referencing `notes/issue-prompt.md` (e.g., shipped issue prompts in `archive/`, the archived `generic-project-workflow.md`). Archives are historical-only per `CLAUDE.md`.

## Tasks

- [ ] Extend `prompts/_template.md`'s header `<!-- How to use this file -->` block with the slimmed placeholder mapping table (≤25 lines).
- [ ] Delete `docs/issue-prompt-guide.md`.
- [ ] Remove the `issue-prompt-guide.md` row from `docs/README.md`'s doc-index table.
- [ ] Update `docs/claude-code-guide.md:147` narrative step to reference `prompts/_template.md`/`prompts/issue-NNN-*.md`.
- [ ] Remove the `issue-prompt-guide.md` bullet from `docs/claude-code-guide.md`'s "see also" list (≈line 291).
- [ ] Update or remove `docs/workflow-guide.md:1134` table row pointing at the deleted guide.
- [ ] Mark the `notes/bug-fixes.md` entry (line 45) `resolved-#NN` and add a one-line closing note.
- [ ] Run `grep -rln "issue-prompt-guide\|notes/issue-prompt" --include="*.md"` from repo root and confirm zero hits outside `archive/`.
- [ ] Move `notes/refactoring-ideas.md` entry #8 from **Unfiled** to **Filed** with this issue's number.

## Acceptance criteria

- `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` returns zero matches outside `archive/`.
- `prompts/_template.md`'s header block contains a placeholder mapping table covering at minimum: `PROJECT_NAME`, `ONE_LINE_PROJECT_DESCRIPTION`, `WORKFLOW_DOC_PATH`, `ADR_FILE`/`ADR_ONE_LINE_SUMMARY`, `PRIMARY_FOLDERS`/`AVOID_FOLDERS`.
- `docs/issue-prompt-guide.md` does not exist on `main` after merge.
- `docs/README.md`, `docs/claude-code-guide.md`, and `docs/workflow-guide.md` contain no links to `issue-prompt-guide.md` or `notes/issue-prompt.md`.
- The `notes/bug-fixes.md` entry tied to this work is marked `resolved-#NN` (this issue's number).
- No skill behaviour changes. Smoke check: `/prepare-issue`, `/claude-issue-executor` still run end-to-end against `examples/projects/kb-lookup`.

## Scope and constraints

- **Docs-only.** Zero skill body or template-logic changes beyond the `prompts/_template.md` header comment.
- **One-shot PR.** ~6 files touched, ~120 lines net deletion. Trivially small for a single PR; phasing would be churn.
- **Plan-first per ADR-006.** A short plan is still appropriate — the docs touched have load-bearing positions in onboarding flow, and the placeholder-table extraction needs surfacing for confirmation before the delete lands.
- **No new tooling shipped.** The `grep` smoke check is a one-liner, not a script.
- **No ADR.** This relocates the manual-fill flow rather than retiring it.

## Out of scope

- Retiring the manual-fill flow entirely (would be Path B and would warrant an ADR).
- Refreshing other anachronistic doc framings (covered by refactoring-ideas.md entry #4 — CLAUDE.md stub framing).
- Archiving shipped prompts to `archive/issues/` (covered by refactoring-ideas.md entry #1).
- The broader `prompts/_template.md` audit — header re-ordering, ADR-038 boundary annotations, etc. If extending the header surfaces other issues with the template body, file a separate issue.

## Notes

Labels: `docs`, plus `tech-debt` if that label exists.
Milestone: open — assign at filing.

References:

- `notes/refactoring-ideas.md` entry #8 (origin)
- `notes/bug-fixes.md` line 45 (superseded entry — finishes here)
- Path-choice reasoning: refactoring-ideas.md entry #8 "Open questions" block + recent session decision (Path C selected over A and B)
- Precedent for collapse-into-template pattern: `prompts/_template.md`'s existing self-documenting header (lines 1–41)
