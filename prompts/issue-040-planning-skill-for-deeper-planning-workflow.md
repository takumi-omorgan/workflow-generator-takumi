You are working in my `workflow-generator` repository.

Context:
- Claude Code Workflow Kit — a toolkit of skills, templates, and workflow docs that scaffolds a plan-first, ADR-driven workflow into new projects.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-031-deeper-planning-workflow.md`
- Decision: Ship a new opt-in `/planning` skill at `skills/planning/` that reads `Design/prd-normalized.md` and `Design/mvp.md`, prompts for requirements decomposition, risks, assumptions, sequencing rationale, and open research questions, and writes `Design/planning.md` from a new `templates/planning-template.md`. The skill is opt-in; small projects continue using the current lightweight flow unchanged.

GitHub Issue:
- Title: Add /planning skill for deeper planning workflow (ADR-031)
- Number: #40
- Milestone: none
- Labels: feature

Goal
Establish the planning artefact and skill that ADR-032, ADR-033, ADR-035, and ADR-037 all build on. Settle the contract here so follow-on ADRs depend on a stable shape.

Why it matters
The current planning chain (`idea-to-prd` → `prd-normalizer` → `prd-to-mvp` → `adr-writer` → `issue-planner`) is too thin for non-trivial projects — there's no canonical home for requirements decomposition, risks, assumptions, or sequencing rationale beyond a flat build-out plan. ADR-006's plan-first execution model assumes a plan exists; this issue ships the scaffolding for that plan on large projects, while keeping small projects on the current lightweight flow.

Requirements
- Add `templates/planning-template.md` with sections for requirements decomposition, risks, assumptions, sequencing rationale, and open research questions
- Add `skills/planning/SKILL.md` that reads `Design/prd-normalized.md` and `Design/mvp.md`, prompts for each section, and writes `Design/planning.md`
- Skill is opt-in (no scaffolding of `Design/planning.md` on install)
- Update `skills/adr-writer/SKILL.md` to read `Design/planning.md` when present
- Update `skills/issue-planner/SKILL.md` to consume sequencing rationale from `Design/planning.md` when present
- Add `templates/README.md` index entry for the new template
- Add a worked example or update `examples/` to demonstrate the planning step

Acceptance criteria
- Running `/planning` on a project with PRD and MVP produces a usable `Design/planning.md` without further authoring
- Projects without `Design/planning.md` continue to work unchanged through `adr-writer` and `issue-planner`
- `templates/planning-template.md` mirrors the section structure recorded in ADR-031
- Re-running `/planning` is idempotent (preserves user edits via marker fences or asks before overwriting)

Scope and constraints
- Primary folders to touch: `skills/planning/`, `templates/`, `skills/adr-writer/`, `skills/issue-planner/`, `examples/`
- Folders to avoid unless absolutely necessary: `Design/adr/` (never edit accepted ADRs in place per CLAUDE.md), `bin/`, `docs/install.md`
- Skill must be opt-in — installer (`bin/install-workflow-kit`) must not auto-scaffold `Design/planning.md` in target projects

Evaluation & testing requirements
- Manually invoke the new skill against the kit's own `Design/prd-normalized.md` and `Design/mvp.md` (if present) and verify the output `Design/planning.md` mirrors the template's section structure
- Verify `adr-writer` and `issue-planner` produce identical output on a project that has no `Design/planning.md` (no regression on the lightweight path)
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-031-deeper-planning-workflow.md`
   - any existing modules under `skills/planning/`, `templates/`, `skills/adr-writer/`, `skills/issue-planner/`, `examples/`
   - any existing tests related to the modules you will change
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
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
