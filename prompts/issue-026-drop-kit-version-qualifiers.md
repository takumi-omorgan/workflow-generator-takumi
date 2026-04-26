You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `Design/adr/`.

ADR:
- File: `Design/adr/adr-022-drop-version-qualifiers-from-kit-scope.md`
- Decision: Kit-self ADRs and docs do not version-qualify scope decisions;
  supersession is the one mechanism for scope changes. Supersedes ADR-002
  specifically; does not supersede ADR-001/003/004/006/014/016, whose
  decisions remain valid even though they mention "v1" in passing.

GitHub Issue:
- Title: Drop kit-self "v1" version qualifiers from kit-scope language (ADR-022)
- Number: #26
- Milestone: v3.0.0 — kit hygiene and licensing
- Labels: chore, docs

Goal
Remove the "v1" qualifier from kit-self language in `CLAUDE.md` and the
user-facing docs so kit scope statements read correctly across releases.

Why it matters
After the kit shipped v2.0.0, "v1 of the kit is for new projects only"
reads as version-gated when no scope decision actually changed at the
v1→v2 boundary. The qualifier creates the impression of a constraint
that might lift in a later version, when in fact the scope is stable.
Editing the qualifier at every release is busywork. Removing it lets
supersession do its job.

Requirements
- Reword `CLAUDE.md:14` to drop "v1" from the new-projects-only rule.
- Reword `docs/install.md:5` (the "Before you start" callout) and
  `docs/install.md:251` (non-GitHub providers) to drop "v1".
- Reword `docs/github-setup.md:4` to drop "v1" from the GitHub-first
  description.
- Mark `Design/adr/adr-002-new-project-only-scope.md` as superseded by
  ADR-022 in the `Status:` line **without editing the historical
  body** (per CLAUDE.md rule against in-place ADR edits). Add a short
  note immediately under the status pointing readers at ADR-022.
- Update the ADR index in `Design/adr/README.md` so ADR-002's row
  reads `superseded by ADR-022`.
- Write the new ADR `Design/adr/adr-022-drop-version-qualifiers-from-kit-scope.md`
  capturing the convention in full.

Acceptance criteria
- `grep -n "\bv1\b" CLAUDE.md docs/install.md docs/github-setup.md`
  returns no matches related to kit-self version qualifiers.
- ADR-002 file shows `Status: superseded by ADR-022` and the original
  text is preserved untouched below the supersession note.
- ADR-022 file exists, status `accepted`, and explains the convention,
  the supersession of ADR-002, and the explicit non-supersession of
  the other ADRs that mention "v1" only in passing.
- ADR index reflects ADR-002's new status and lists ADR-022 as
  accepted.
- Target-project MVP vocabulary ("In v1 / Not in v1") is **not**
  touched by this issue. That is product surface, handled separately
  by ADR-024 (see issue #28).

Scope and constraints
- Primary folders to touch: `CLAUDE.md`, `docs/`, `Design/adr/`.
- Folders to avoid: `templates/`, `skills/`, `examples/`,
  `generic-project-workflow.md`, `notes/`, MVP/build-out plan
  historical docs.
- Do not edit accepted ADRs in place. Use a new ADR (ADR-022) plus a
  status flip on the superseded one (ADR-002).

Evaluation & testing requirements
- Diff review: confirm only the kit-self surfaces changed.
- The kit ships markdown only for this change; no test runner exists
  for prose. Manual verification via `grep` is sufficient.
- All existing tests continue to pass (none are affected).
- If `bin/sync-adr-index` exists at the time of implementation, run
  it to refresh the ADR index after the status flip.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-002-new-project-only-scope.md`
   - `Design/adr/README.md`
   - `docs/install.md` and `docs/github-setup.md`
   - `templates/adr-template.md` (for ADR-022 structure)
2. Propose a short, step-by-step implementation PLAN for this issue,
   including:
   - the exact reword for each kit-self surface,
   - the supersession-note format on ADR-002,
   - the ADR-022 outline (Context, Options, Decision, Consequences),
   - the index update.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue
     (e.g. "docs: drop kit-self v1 qualifiers (ADR-022, #26)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (grep results),
   - any follow-up work needed for later issues (note: ADR-024 / issue
     #28 picks up the MVP vocabulary, which this issue deliberately
     leaves alone),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.

---

**Retrospective note (2026-04-26):** This prompt is the canonical
session brief that should have driven this work. The implementation
was actually performed interactively in a session that did not
follow the formal `/prepare-issue` → `/claude-issue-executor` flow.
This file is preserved here as the audit trail and as an exemplar
for future ADR-022-style cleanup issues.
