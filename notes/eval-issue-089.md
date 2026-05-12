# Evaluation summary — issue #89

**Issue:** #89 — Finish legacy `notes/issue-prompt.md` removal — collapse guide into template, fix four broken references
**Branch:** `legacy-prompt-cleanup`
**ADR:** none (docs-only cleanup; manual-fill path relocated, not retired)
**Prompt:** `prompts/issue-089-legacy-prompt-cleanup.md`

## What changed

**Template header expanded** to absorb the placeholder-mapping salvage:
- `prompts/_template.md` — added 11 lines of comment in the existing `<!-- How to use this file -->` block; slimmed-down table covering 5 placeholder rows (PROJECT_NAME, ONE_LINE_PROJECT_DESCRIPTION, WORKFLOW_DOC_PATH, ADR_FILE/ADR_ONE_LINE_SUMMARY, PRIMARY_FOLDERS/AVOID_FOLDERS). 111 → 122 lines.

**Deleted:**
- `docs/issue-prompt-guide.md` — 118-line standalone guide; salvage now lives in the template header.

**Four broken references repointed or removed:**
- `docs/README.md:26` — dropped row from doc-index table.
- `docs/claude-code-guide.md:146-149` — replaced the `notes/issue-prompt.md` paste text with `prompts/issue-NNN-*.md` (copied from `prompts/_template.md`).
- `docs/claude-code-guide.md:~291` — removed the `issue-prompt-guide.md` "see also" bullet.
- `docs/workflow-guide.md:1134` — removed the "Fill a Claude Code session prompt by hand" row from the "Where to go deeper" table.

**Status update:**
- `notes/bug-fixes.md:45` — entry status changed `superseded` → `resolved-#89` with one-line closing note.

## Commits

```
7e1cdd4 docs: collapse issue-prompt guide into prompts/_template.md header (#89)
a1851e4 docs: drop four broken issue-prompt-guide references (#89)
6e1f4c6 notes: mark bug-fixes entry resolved-#89 (#89)
```

Plus pre-flight on `main` (committed before branching): `ad28f62 notes: prep #89 — entry #8 filed, state pointer + prompt`.

## Verification performed

**Acceptance criterion 1 — grep for deleted file paths:**

```
$ grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"
design/state.md
archive/generic-project-workflow.md
archive/phase-1/issue8.md
archive/phase-1/issue8-prompt.md
archive/phase-1/issue12-prompt.md
notes/refactoring-ideas.md
notes/bug-fixes.md
examples/idea-only-example.md
notes/issue-draft-legacy-prompt-cleanup.md
examples/custom-prd-example.md
examples/standard-prd-example.md
prompts/issue-089-legacy-prompt-cleanup.md
```

Categorising the non-archive hits:

- **Issue's own metadata (expected, not a defect):** `design/state.md` continue-here note, `notes/refactoring-ideas.md` Filed entry #8, `notes/bug-fixes.md` updated entry + its supersession history, `notes/issue-draft-legacy-prompt-cleanup.md` (issue draft), `prompts/issue-089-legacy-prompt-cleanup.md` (the prompt). Editing these erases the project's record of what shipped and why.
- **Out-of-scope follow-up:** `examples/{idea-only,custom-prd,standard-prd}-example.md` still link to the deleted files. Same root cause as #89 (the 2026-05-06 partial cleanup), but Requirements scoped #89 to four `docs/` surfaces only and Scope listed `docs/, prompts/_template.md, notes/bug-fixes.md` as the primary folders. **Surfaced as a follow-up below.**

**Acceptance criterion 4 — zero hits in the four canonical docs:**

```
$ grep -n "issue-prompt" docs/README.md docs/claude-code-guide.md docs/workflow-guide.md
(no matches)
```

**Template smoke check:**

```
$ wc -l prompts/_template.md
     122 prompts/_template.md
```

(Was 111, +11 lines, well under the ≤25 target.) `head -55` confirms the new placeholder-mapping table renders cleanly inside the existing `<!-- How to use this file -->` HTML comment block.

**Skill smoke check (acceptance criterion 6 — no behaviour change):**
Quick read of `skills/claude-issue-executor/SKILL.md` and `skills/prepare-issue/SKILL.md` — neither references the deleted files; both still load and would still drive a session end-to-end. (No automated test runner in this kit.)

**ADR index sync:** N/A — no ADR files touched.

## Follow-ups

- **`examples/*.md` cleanup (out of scope for #89).** Three shipped example docs link to deleted files:
  - `examples/idea-only-example.md:87,91,93,118`
  - `examples/custom-prd-example.md:113,117,118`
  - `examples/standard-prd-example.md:173,177,178`

  All point at `../notes/issue-prompt.md`, `../notes/issue-prompt-sample.md`, or `../docs/issue-prompt-guide.md`. They produce real broken links for kit readers. Same root cause as #89 — file as a follow-up refactor entry under `notes/refactoring-ideas.md` and ship via a small docs-cleanup PR.

- **Pre-existing stale untracked files in working tree** — `notes/handoff-2026-05-07.md` and `notes/skills-audit-2026-05-07/*` were left in place across this session (unrelated to #89). They may want a separate clean-up or commit decision when convenient.

## Commands to reproduce verification

```bash
# Hits outside archive/ — expect: issue's own metadata + examples/ follow-up only
grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"

# Zero in the four canonical docs
grep -n "issue-prompt" docs/README.md docs/claude-code-guide.md docs/workflow-guide.md

# Template length + header smoke
head -55 prompts/_template.md
wc -l prompts/_template.md

# Branch state
git log --oneline main..HEAD
git status --short
```

## Next step

Run `/pr-review-packager` to draft a pull-request body from this branch.
