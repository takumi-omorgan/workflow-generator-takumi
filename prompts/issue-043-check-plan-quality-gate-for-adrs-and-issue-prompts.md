You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-034-plan-checker.md`
- Decision: Ship `/check-plan` at `skills/check-plan/` as a single skill that takes an artefact path (ADR or issue prompt), detects type from path/frontmatter, runs a checklist tuned per type, returns pass/fail with specific revisions, and iterates with the user up to 3 rounds before yielding; `adr-writer` and `prepare-issue` chain it automatically as a pre-commit gate, with `--skip-check` opting out; the checker emits warnings (not hard errors) for dimensions it cannot verify deterministically; criteria live at `skills/check-plan/criteria.md`, version-locked to the templates.

GitHub Issue:
- Title: Add /check-plan quality gate for ADRs and issue prompts (ADR-034)
- Number: #43
- Milestone: none
- Labels: feature

Goal
Catch quality defects in ADRs and issue prompts at draft time — when the cost of fixing them is lowest — instead of at execution time, and make ADR/prompt quality independent of author discipline.

Why it matters
Bad ADRs (vague decisions, missing alternatives, inconsistent with accepted ones) and thin prompts (no acceptance criteria, oversized scope, missing ADR links) are caught only at execution time today, when a session may already be started and a branch already opened. A pre-commit gate moves that catch backwards in the flow.

Requirements
- Add `skills/check-plan/SKILL.md` that detects artefact type from path or frontmatter and routes to the matching criteria checklist.
- Add `skills/check-plan/criteria.md` with two version-locked checklists: one for ADRs (clear context / decision / consequences; references the right ADRs; doesn't conflict with accepted ones; options have both pros and cons; decision names one of the listed options) and one for issue prompts (acceptance criteria present; correct ADR links; fits the build-out-plan phase per ADR-032; single-PR scope; no ambiguous `TBD` placeholders).
- Update `skills/adr-writer/SKILL.md` to chain `/check-plan` as a pre-commit gate, with a documented `--skip-check` opt-out for known-good rapid iteration.
- Update `skills/prepare-issue/SKILL.md` to do the same.
- Iteration cap: 3 rounds of `/check-plan` revisions before the skill yields control to the user (the cap is enforced by `/check-plan` itself).
- Warnings (not errors) for dimensions the checker cannot verify deterministically — the user decides whether to fix.
- Document `--skip-check`, the criteria document, and the version-lock contract (criteria edited whenever ADR or prompt templates change).

Acceptance criteria
- `/check-plan path/to/adr.md` returns pass/fail with specific revisions for failing criteria; on fail, prompts the user to revise and re-checks (up to 3 rounds).
- `/check-plan path/to/prompt.md` does the same against prompt-specific criteria.
- `adr-writer` and `prepare-issue` both block commit / write on a failed check, except when `--skip-check` is passed.
- Editing `templates/adr-template.md` or `prompts/_template.md` without correspondingly updating `skills/check-plan/criteria.md` produces a CI warning (via `bin/`-style script) or, if CI is not wired in this kit, the warning is documented as a manual checklist rule.

Scope and constraints
- Primary folders to touch: `skills/check-plan/` (new), `skills/adr-writer/SKILL.md`, `skills/prepare-issue/SKILL.md`, plus a small drift-detection script under `bin/` if a CI hook is included (matching the `bin/sync-adr-index` style).
- Folders to avoid unless absolutely necessary: `Design/adr/` (do not edit accepted ADR-034), `examples/projects/`, `prompts/` (other than this issue's own prompt).
- v1 scope is **ADRs and issue prompts only**. Per ADR-034 "Deferred", do not add criteria for `build-out-plan.md` or `planning.md` — those are explicitly deferred to a follow-up ADR.
- Type detection (ADR vs prompt) must be unambiguous: ADRs live under `Design/adr/adr-NNN-*.md` and have a `**Status:**` line; prompts live under `prompts/issue-NNN-*.md` and follow `prompts/_template.md`'s section order. If both signals are absent or contradict, stop and ask — do not guess.
- Iteration cap is hard at 3. After the third failed round, surface the remaining failures to the user as items to fix manually and stop the loop; do not silently bypass.
- The chained gate in `adr-writer` and `prepare-issue` runs **after** the artefact would have been written and **before** the disk write — so a failed check leaves the working tree clean. `--skip-check` short-circuits the gate but is documented as opt-out, not opt-in.
- Criteria document is the source of truth; SKILL.md should reference its sections by stable IDs, not paste the criteria verbatim, so updates to the criteria don't require SKILL.md edits.

Evaluation & testing requirements
- Demonstrate the ADR pass path: run `/check-plan` against a known-good ADR (e.g. `Design/adr/adr-035-state-md-session-continuity.md`) and confirm pass with no revisions requested.
- Demonstrate the ADR fail path: run against a deliberately broken fixture (missing Decision section, or Decision references an option not in Options considered) and confirm specific revisions are surfaced.
- Demonstrate the prompt pass path: run against a known-good prompt (e.g. `prompts/issue-044-design-state-md-plus-resume-and-pause-skills.md`) and confirm pass.
- Demonstrate the prompt fail path: a fixture missing `Acceptance criteria` triggers a specific revision.
- Demonstrate the iteration cap: a fixture that cannot be repaired in 3 rounds yields to the user with the remaining failures listed.
- Demonstrate `--skip-check` in `adr-writer` and `prepare-issue`: on a failing artefact, the flag bypasses the gate and writes anyway, with a one-line breadcrumb in the output for traceability.
- Demonstrate the warnings path: a non-deterministic dimension (e.g. "decision rationale is convincing") produces a warning, not a failure, and does not block the commit.
- Verify the version-lock guard: editing `templates/adr-template.md` or `prompts/_template.md` without updating `skills/check-plan/criteria.md` triggers the documented warning (CI script or manual checklist).
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-034-plan-checker.md`
   - `Design/adr/adr-013-prepare-issue-skill.md` (parent for prepare-issue contract)
   - `templates/adr-template.md` and `prompts/_template.md` (the criteria's version-lock targets)
   - `skills/adr-writer/SKILL.md`, `skills/prepare-issue/SKILL.md`
   - `skills/clarify/SKILL.md` and `skills/planning/SKILL.md` (recent precedent for new-skill house style)
   - `bin/sync-adr-index` (precedent for the optional CI drift-check script)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - the criteria-document layout (section IDs, ADR vs prompt split, version-lock metadata),
   - your verification or test plan including which fixture artefacts you'll exercise.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope (no build-out-plan / planning.md criteria — explicitly deferred),
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(scope): add thing (ADR-034, #43)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
