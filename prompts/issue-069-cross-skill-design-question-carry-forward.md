You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-040-cross-skill-design-question-carry-forward.md`
- Decision: Adopt Option A — add three coordinated skill-spec hooks across the implementation chain (`claude-issue-executor` → `pr-review-packager` → `prepare-issue`), sharing one canonical `design-questions:` schema documented in the workflow guide.

GitHub Issue:
- Title: Implement cross-skill design-question carry-forward (ADR-040)
- Number: #69
- Milestone: v3.4.0 - eval baseline fixes
- Labels: feature

Goal
Make the executor → packager → prepare-issue carry-forward of design questions a spec-mandated property rather than emergent behaviour, so the audit-trail-grade visibility the kit aspires to becomes deterministic regardless of session author.

Why it matters
The v3.3.0 baseline eval (research-tracker fixture) showed the loop closing organically across issues #4 + #5 — design questions raised in the executor's eval summary were preserved in the PR body's "Notes for #5" section, then carried into the next prompt and answered. Audit-trail-grade visibility, but it depended on chain-aware authoring. ADR-040 turns the property from happy-accident into a kit guarantee.

Requirements
- Define the canonical `design-questions:` schema (title + target-issue ref + one-paragraph context) in `docs/workflow-guide.md` as the single source of truth.
- Update `skills/claude-issue-executor/SKILL.md` eval-summary spec: add a structured `design-questions:` subfield under "Follow-ups", with a documented "when to populate / when not to populate" rule.
- Update `skills/pr-review-packager/SKILL.md`: scan the executor's eval-summary for `design-questions:` entries and emit one "Notes for #N" section per target-issue reference in the PR body.
- Update `skills/prepare-issue/SKILL.md`: scan recently-merged PRs for "Notes for #N" sections matching the new issue's number and embed them in a "Design questions carried forward from PR #M" subsection of the generated prompt.
- Cross-reference the schema and spec rules from all three skill specs back to the workflow guide (avoid restating the schema in each).
- Document the `--no-prompt` (ADR-038) interaction: `--no-prompt` skips `prepare-issue` and therefore the carry-forward — acceptable by design since trivial issues do not raise cross-issue design questions.

Acceptance criteria
- The schema appears in `docs/workflow-guide.md` as a named, versioned section.
- All three affected skill specs reference the workflow-guide schema rather than restating it.
- A worked example in `skills/pr-review-packager/example.md` shows the executor → packager → prepare-issue handoff end-to-end.
- The "when not to populate" rule is concrete enough that an executor session can route correctly without operator judgment.
- `bin/sync-adr-index --check` is clean (no ADR edits in this issue).

Scope and constraints
- Primary folders to touch: `skills/claude-issue-executor/`, `skills/pr-review-packager/`, `skills/prepare-issue/`, `docs/workflow-guide.md`
- Folders to avoid unless absolutely necessary: `design/adr/` (ADR-040 is accepted; do not edit), `bin/`, other `skills/*/` directories not listed above
- Per ADR-039, this issue is **significant** (modifies 3+ `skills/*/SKILL.md` files plus the workflow guide). Plan mode (shift+tab shift+tab) should be entered before any mutating edit.

Evaluation & testing requirements
- Verify by reading: each of the three affected skill specs cites the workflow-guide schema section and does not restate it inline.
- Verify by example: the worked example in `skills/pr-review-packager/example.md` demonstrates the round-trip on a synthetic two-issue pair.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-040-cross-skill-design-question-carry-forward.md`
   - `design/adr/adr-038-tighten-prompt-step.md` (this issue extends it)
   - `skills/claude-issue-executor/SKILL.md`, `skills/pr-review-packager/SKILL.md`, `skills/prepare-issue/SKILL.md`
   - `docs/workflow-guide.md`
   - `notes/adr-038-alignment-review.md` (content-boundary review for the prompt artefact)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(skills): add design-questions schema to workflow guide (ADR-040, #69)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
