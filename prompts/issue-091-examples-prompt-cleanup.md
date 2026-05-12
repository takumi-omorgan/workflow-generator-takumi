You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- none — issue is docs-cleanup only. Identical reasoning to the sibling issue #89: this relocates references onto `prompts/_template.md` (the actual successor — self-documenting after #89's collapse-into-header work lands), not retiring any kit convention. Per the issue body's `## ADR` section, no kit convention that target projects depend on changes shape. Plan-first execution per ADR-006 still applies.

GitHub Issue:
- Title: Repoint examples/*.md references to deleted issue-prompt files
- Number: #91
- Milestone: none
- Labels: none

Goal
Finish the partial-cleanup pattern in the `examples/` slice — three shipped walk-throughs (`examples/idea-only-example.md`, `examples/custom-prd-example.md`, `examples/standard-prd-example.md`) still link to deleted `notes/issue-prompt.md`, `notes/issue-prompt-sample.md`, and `docs/issue-prompt-guide.md` files. Repoint the narrative steps to `prompts/issue-NNN-*.md` / `prompts/_template.md` and remove the now-duplicative follow-up bullets that point at deleted files.

Why it matters
`examples/` is a primary onboarding surface — readers running the end-to-end walk-throughs hit ~9 broken links before they reach the first execution session. The `idea-only-example.md:91` reference to `notes/issue-prompt-sample.md` is a 404 to a file deleted weeks ago. This issue was surfaced as an explicit out-of-scope follow-up in PR #90's eval summary (the sibling #89 covered the `docs/` slice; this covers `examples/`). Same root cause, different blast radius. After this lands, the kit has no remaining broken references to the deleted issue-prompt files outside `archive/`.

Requirements
- Rewrite the "First execution session" narrative in `examples/idea-only-example.md`, `examples/custom-prd-example.md`, and `examples/standard-prd-example.md` to reference `prompts/issue-NNN-*.md` (copied from `prompts/_template.md`) instead of `notes/issue-prompt.md`.
- Delete the follow-up "Sample filled prompt: …", "How to fill it: …", and "Template and guide: …" bullets in each file. These linked at the deleted `notes/issue-prompt-sample.md` and `docs/issue-prompt-guide.md`. The guidance they contained now lives in `prompts/_template.md`'s self-documenting header comment (added in PR #90).
- Verify against the per-file line locations in the issue body: `idea-only-example.md:87,91,93,118`; `custom-prd-example.md:113,117,118`; `standard-prd-example.md:173,177,178`.

Acceptance criteria
- `grep -n "issue-prompt" examples/*.md` returns zero hits.
- `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` returns zero hits in `examples/`.
- Each of the three rewritten files reads coherently end-to-end (manual smoke read; no orphaned bullets, no broken sentence flow at the deletion points).
- No skill or template changes — `examples/` only.
- The PR body cross-references `notes/refactoring-ideas.md` entry #12 (already filed as #91 in the Filed section).

Scope and constraints
- Primary folders to touch: `examples/` (3 files: `idea-only-example.md`, `custom-prd-example.md`, `standard-prd-example.md`).
- Folders to avoid unless absolutely necessary: `examples/projects/` (no broken refs there — verified via grep), `docs/`, `skills/`, `templates/`, `prompts/`, `notes/` (the entry-#12 status update is a separate one-line edit at PR time), `design/`, `bin/`, `archive/` (historical only per CLAUDE.md).
- Docs-only — one-shot single PR. ~3 files touched, ~9 link edits, net deletion.
- Plan-first per ADR-006 still applies but the change is small enough that a short plan covering the three narrative rewrites + bullet deletions is sufficient.

Evaluation & testing requirements
- After the edits land, run `grep -n "issue-prompt" examples/*.md` and confirm zero hits. Paste the command output into the evaluation summary.
- Run `grep -rln "docs/issue-prompt-guide\|notes/issue-prompt\.md\|notes/issue-prompt-sample\.md" --include="*.md"` from repo root and confirm zero hits outside `archive/` (`docs/` slice is covered by sibling #89 / PR #90).
- Manual smoke read of each of the three rewritten files — confirm the "First execution session" step still flows naturally after the bullet deletions.
- All existing tests must continue to pass (kit has no automated test runner — docs-only changes covered by the grep checks).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `prompts/_template.md` (the new successor — see its header comment for the canonical "how to fill" reference that the deleted `docs/issue-prompt-guide.md` used to provide; this header lands via PR #90 — if #90 is not yet merged, read the PR-#90 branch's version)
   - `examples/idea-only-example.md`, `examples/custom-prd-example.md`, `examples/standard-prd-example.md`
   - The sibling issue PR for context: PR #90 / issue #89 (same partial-cleanup pattern, `docs/` slice)
   - `notes/refactoring-ideas.md` entry #12 (origin)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the exact replacement text for each of the three "First execution session" narrative steps (show me the new wording in the plan before you write),
   - the exact bullets to delete in each file with their line numbers,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the issue (e.g. `docs: repoint examples/*.md issue-prompt refs (#91)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (paste the grep outputs),
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
