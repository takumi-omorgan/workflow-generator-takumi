You are working in my `workflow-generator` repository.

Context:
- Claude Code Workflow Kit — a toolkit of skills, templates, and workflow docs that scaffolds a plan-first, ADR-driven workflow into new projects.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-033-clarify-step.md`
- Decision: Ship `/clarify` as an opt-in skill at `skills/clarify/` that reads `Design/prd-normalized.md`, `Design/mvp.md`, and `Design/planning.md` (when ADR-031 has shipped), scouts the codebase, surfaces a checklist of unresolved implementation questions, conducts deep-dive resolution per question, and appends settled decisions to `Design/decisions.md`. Below ADR weight by design — captures informal-but-settled context that downstream agents (planner, executor) can rely on without re-asking.

GitHub Issue:
- Title: Add /clarify skill producing Design/decisions.md (ADR-033)
- Number: #42
- Milestone: none
- Labels: feature

Goal
Resolve ambiguity before ADRs are drafted, so `adr-writer` captures decisions and not exploration. Closes a gap that today gets paid at execution time.

Why it matters
ADR drafts currently mix decisions with discovery, and the planner stalls on ambiguity at session start. A focused clarification step keeps ADRs decision-only and reduces context-window pressure during execution. Pairs naturally with `/planning` (ADR-031, already shipped via PR #49) — `/clarify` is invocable standalone or as a step in the deeper planning flow.

Requirements
- Add `templates/decisions-template.md` (append-only, with section per gray area: question, options weighed, decision, rationale)
- Add `skills/clarify/SKILL.md` that reads PRD, MVP, planning.md (when present), scouts the codebase, surfaces a checklist of gray areas, runs deep-dive resolution per question, and appends to `Design/decisions.md`
- Skip areas already locked by accepted ADRs (parse `Design/adr/*.md` headings + status; if a question's topic maps to an accepted ADR, it's settled)
- Document the "graduate to ADR" criterion ("would superseding this need a new ADR?") in the skill
- Update `skills/adr-writer/SKILL.md` to read `Design/decisions.md` when present (additive Optional input, mirroring how planning.md was wired in PR #49)
- Add `templates/README.md` index entry for the new template
- Add `skills/clarify/example.md` (worked walk-through, matching the convention of every other skill in the kit)
- Add `skills/clarify/` row to `skills/README.md` index

Acceptance criteria
- Running `/clarify` on a project produces `Design/decisions.md` with at least the user-selected gray areas resolved
- Re-running `/clarify` skips areas already in `decisions.md` and areas locked by accepted ADRs
- `adr-writer` references decisions from `decisions.md` when drafting (no duplication of context across files)
- Clear documented test for "this should be an ADR, not a decision" (the graduation criterion)

Scope and constraints
- Primary folders to touch: `skills/clarify/`, `templates/`, `skills/adr-writer/`, `skills/README.md`
- Folders to avoid unless absolutely necessary: `Design/adr/` (never edit accepted ADRs in place per CLAUDE.md), `bin/`, `docs/install.md`, `skills/issue-planner/`, `skills/claude-issue-executor/`
- Skill must be opt-in — installer (`bin/install-workflow-kit`) must not auto-scaffold `Design/decisions.md` in target projects
- Decisions.md is append-only by design — re-runs should never delete or rewrite earlier entries; they only add new sections or skip already-settled questions
- This issue's implementation is **clearly-significant** per ADR-039 (new `skills/*/SKILL.md`, new `templates/*` file, edits `skills/adr-writer/SKILL.md`, ≥ 4 files) — plan mode should be entered before the executor runs against this issue, per the rhythm wired in via PR #53

Evaluation & testing requirements
- Manually invoke the new skill against the kit's own context (no `Design/prd-normalized.md` or `Design/mvp.md` exists in this kit, but the skill should degrade gracefully — flag this as a manual verification step rather than a runtime test)
- Verify `adr-writer` produces identical output on a project that has no `Design/decisions.md` (no regression on the lightweight path)
- Confirm `Design/decisions.md` re-run idempotency: running the skill twice with the same gray areas does not duplicate sections
- Confirm the "graduate to ADR" criterion is documented and concrete enough to apply in practice
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-033-clarify-step.md`
   - `skills/planning/SKILL.md` (the peer skill from ADR-031, for shape)
   - `skills/adr-writer/SKILL.md` (the file you'll be modifying)
   - existing modules under `skills/clarify/`, `templates/`, `examples/`
   - any existing tests related to the modules you will change
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
