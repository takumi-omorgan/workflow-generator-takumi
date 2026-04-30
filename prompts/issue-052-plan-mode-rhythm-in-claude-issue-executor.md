You are working in my `workflow-generator` repository.

Context:
- Claude Code Workflow Kit — a toolkit of skills, templates, and workflow docs that scaffolds a plan-first, ADR-driven workflow into new projects.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-039-plan-mode-for-significant-tasks.md`
- Decision: Update `skills/claude-issue-executor/SKILL.md` so the executor classifies each session against a documented "significant" checklist at session start and routes accordingly: auto-flag for plan mode entry on clearly-significant sessions, auto-skip on clearly-trivial sessions, ask once on borderline. The "trivial" checklist is shared with ADR-038's `--no-prompt` criteria — single source of truth.

GitHub Issue:
- Title: Implement plan-mode rhythm in claude-issue-executor (ADR-039)
- Number: #52
- Milestone: none
- Labels: feature

Goal
Wire ADR-039's hybrid plan-mode rhythm into the kit's executor so harness-level enforcement runs alongside the existing chat plan-gate.

Why it matters
The chat plan-gate is convention; plan mode is enforcement. Without this issue, the rhythm depends entirely on assistant discipline — the gap ADR-039 was written to close. ADR-039 documents the contract; this issue ships the executor changes that make the contract enforceable. The user explicitly asked for this rhythm to be the kit's standing default.

Requirements
- Add a "Plan-mode rhythm (per ADR-039)" section to `skills/claude-issue-executor/SKILL.md` documenting the hybrid path: auto-flag on clearly-significant, auto-skip on clearly-trivial, ask on borderline
- Add the "significant" checklist to `skills/claude-issue-executor/SKILL.md` (3+ files; edits skills/*/SKILL.md; edits templates/*; edits bin/*; modifies .claude/settings*.json; or any other "blast radius beyond a single small fix" property)
- Add the "trivial" checklist to `skills/claude-issue-executor/SKILL.md` (single typo; single-line doc tweak; status-line / config-default tweak; single-file rename in scratch space; feature-ideas.md status flip; ADR status flip; single-PR scope with no design decisions and no ADR linkage)
- Update the existing "The plan gate" section to call out that the chat plan-gate runs *inside* plan mode when the user has entered it — both can coexist
- Update `skills/claude-issue-executor/SKILL.md` Session protocol so step 1 (or earliest practical step) classifies the session and routes accordingly
- Cross-reference the trivial checklist from ADR-038 / `--no-prompt` criteria in `skills/claude-issue-executor/SKILL.md` so the two stay aligned; document the alignment-review obligation when either evolves
- Update `docs/workflow-guide.md` section 2.e (or equivalent) to document the rhythm with concrete shift+tab semantics
- Add a short note to `skills/claude-issue-executor/example.md` showing the hybrid path in action

Acceptance criteria
- The two checklists (significant, trivial) appear in `skills/claude-issue-executor/SKILL.md` as named, version-stable lists
- The Session protocol explicitly classifies the session at the start and routes accordingly
- The chat plan-gate continues to operate as today; the new rhythm is additive on top
- ADR-038's `--no-prompt` trivial criteria reference (or are referenced by) ADR-039's trivial checklist — single source of truth
- Workflow guide reflects the rhythm with concrete shift+tab semantics
- `bin/sync-adr-index --check` is clean (no ADR edits in this issue)

Scope and constraints
- Primary folders to touch: `skills/claude-issue-executor/`, `docs/`
- Folders to avoid unless absolutely necessary: `Design/adr/` (never edit accepted ADRs in place per CLAUDE.md), `bin/`, `templates/`, `.claude/`
- **Self-application: this issue's implementation is itself "significant" per ADR-039** — modifies a SKILL.md file, edits the workflow guide, multi-file. The executor must be entered in plan mode for this issue. The kit is its own first test case.
- Cross-skill consistency: `skills/prepare-issue/SKILL.md` and `skills/pr-review-packager/SKILL.md` are NOT modified in this issue — applying the rhythm to other skills is explicitly deferred to a follow-up (per ADR-039's "Deferred" consequence).

Evaluation & testing requirements
- Walk through the new "Plan-mode rhythm" section to confirm both checklists are present, named, and concrete
- Diff `skills/claude-issue-executor/SKILL.md` to confirm the chat plan-gate language is preserved (additive on top of, not replacing, the existing gate)
- Walk through the example.md update to confirm the hybrid path is illustrated end-to-end
- Confirm `docs/workflow-guide.md` section 2.e (or equivalent) describes the rhythm with explicit shift+tab toggles
- Confirm ADR-038 cross-reference is in place (the alignment-review obligation is explicitly documented)
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-039-plan-mode-for-significant-tasks.md`
   - `Design/adr/adr-038-tighten-prompt-step.md` (for the trivial-criteria alignment)
   - `skills/claude-issue-executor/SKILL.md` (the file you'll be modifying)
   - `skills/claude-issue-executor/example.md`
   - `docs/workflow-guide.md`
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key sections / structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue
     (e.g. "feat(scope): add thing (ADR-NNN, #NN)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
