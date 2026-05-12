<!--
  Draft GitHub issue body for "Repoint examples/*.md references to deleted issue-prompt files".
  Source: notes/refactoring-ideas.md entry #12.
  Surfaced as out-of-scope follow-up in PR #90 (issue #89) eval summary.
  Review, then file with: gh issue create --title "..." --body "$(cat this-file.md)"
-->

## Summary

Repoint the remaining `examples/*.md` references to the deleted `notes/issue-prompt.md` / `notes/issue-prompt-sample.md` / `docs/issue-prompt-guide.md` files. Same partial-cleanup root cause as #89, but in the `examples/` slice rather than the `docs/` slice — explicitly out of scope for #89's prompt (which named only four `docs/` surfaces) and surfaced as a follow-up in PR #90's eval summary.

## ADR

None required. Identical reasoning to #89: this relocates references onto `prompts/_template.md` (the actual successor — now self-documenting after #89), not retiring any kit convention.

## Why

Three shipped example walk-throughs in `examples/` still link to deleted files:

- `examples/idea-only-example.md` — lines 87, 91, 93, 118 (`notes/issue-prompt.md` ×2, `notes/issue-prompt-sample.md`, `docs/issue-prompt-guide.md`).
- `examples/custom-prd-example.md` — lines 113, 117, 118 (`notes/issue-prompt.md` ×2, `docs/issue-prompt-guide.md`).
- `examples/standard-prd-example.md` — lines 173, 177, 178 (`notes/issue-prompt.md` ×2, `docs/issue-prompt-guide.md`).

`examples/` is a primary onboarding surface — readers running through these end-to-end walk-throughs hit ~9 broken links before they reach the first execution session. The `notes/issue-prompt-sample.md` reference at `idea-only-example.md:91` is a 404 to a file deleted weeks ago.

This was the immediate trigger for filing: the `grep -rln` verification in PR #90 surfaced these hits and the PR comment correctly flagged that closing #89 with known-broken kit-example links is a partial finish.

## Scope

### What gets updated

For each of the three files, the "First execution session" step currently reads (paraphrased): *"User starts a Claude Code session with a filled `notes/issue-prompt.md` referencing `design/adr/adr-NNN-*.md` and the M1 context."* Rewrite to:

> User starts a Claude Code session with a filled `prompts/issue-NNN-*.md` (copied from `prompts/_template.md`) referencing `design/adr/adr-NNN-*.md` and the M1 context.

The follow-up bullets ("Sample filled prompt: …", "How to fill it: …", "Template and guide: …") that link to the deleted files should be **removed entirely**. They duplicate guidance that now lives in `prompts/_template.md`'s self-documenting header comment (added in PR #90).

Specifically:

- `examples/idea-only-example.md:87` — replace `notes/issue-prompt.md` link with `prompts/_template.md` (or rephrase to mention `prompts/issue-NNN-*.md`).
- `examples/idea-only-example.md:91` — delete the "Sample filled prompt" line (the sample file is gone; the template's header comment replaces it).
- `examples/idea-only-example.md:93` — delete the "How to fill it" line.
- `examples/idea-only-example.md:118` — repoint the "using `notes/issue-prompt.md` for each" mention.
- `examples/custom-prd-example.md:113,117,118` — same pattern; rewrite the narrative line, delete the follow-up "Template and guide" block.
- `examples/standard-prd-example.md:173,177,178` — same pattern; rewrite the narrative line, delete the follow-up "Template and guide" block.

### What is explicitly left alone

- Other anachronisms in these files. This is a broken-refs fix, not the full freshness audit (which is `notes/refactoring-ideas.md` entry #6 — major-release-boundary refresh). If a reference reads strangely but doesn't 404, leave it.
- The `examples/projects/` subdirectory. None of those files reference the deleted paths (verified via `grep -rln`).

## Tasks

- [ ] Rewrite the "First execution session" narrative in each of the three `examples/*.md` files to reference `prompts/issue-NNN-*.md` + `prompts/_template.md`.
- [ ] Delete the follow-up `→ Sample filled prompt`, `→ How to fill it`, and `→ Template and guide` bullets that point at deleted files.
- [ ] Run `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` from repo root and confirm zero hits in `examples/`.
- [ ] Move `notes/refactoring-ideas.md` entry #12 from **Unfiled** to **Filed** with this issue's number.

## Acceptance criteria

- `grep -n "issue-prompt" examples/*.md` returns zero hits.
- The three `examples/*.md` files contain no links to `notes/issue-prompt.md`, `notes/issue-prompt-sample.md`, or `docs/issue-prompt-guide.md`.
- Each file's "First execution session" step reads coherently end-to-end (manual smoke read).
- No skill or template changes — `examples/` only.

## Scope and constraints

- **Docs-only.** `examples/` slice only. One-shot single PR. ~3 files touched, ~9 link edits, net deletion.
- **Plan-first per ADR-006**, though trivially small — a short plan covering the three narrative rewrites and the bullet deletions is sufficient.
- **No new tooling.** The `grep` smoke check is a one-liner.
- **No ADR.** Same path as #89.

## Out of scope

- Other freshness issues in `examples/*.md` (covered by refactoring-ideas.md entry #6).
- `examples/projects/` content (no broken refs there).
- Any further consolidation of `prompts/_template.md`'s header — already settled in #89.

## Notes

Labels: `docs`, plus `tech-debt` if that label exists.
Milestone: open — assign at filing.

References:

- `notes/refactoring-ideas.md` entry #12 (origin)
- #89 / PR #90 (sibling cleanup that covered the `docs/` slice)
- `notes/eval-issue-089.md` Follow-ups section (where this was first surfaced)
