You are working in my `workflow-generator` repository.

Context:
- Claude Code Workflow Kit — a toolkit of skills, templates, and workflow docs that scaffolds a plan-first, ADR-driven workflow into new projects.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-032-implementation-phases.md`
- Decision: Extend `templates/build-out-plan-template.md` with `## Phase N: <name>` sections (goal, scope, ADR deps, exit criterion). `prd-to-mvp` (or `/planning` from ADR-031) emits the phased plan; `adr-writer` lets ADRs declare a `phase:` frontmatter tag; `issue-planner` creates one GitHub milestone per phase; `workflow-docs` surfaces phases in the README roadmap; `/release` treats one phase as the default release unit. Single-phase projects keep working unchanged — a plan with no `## Phase` headings is treated as one implicit phase.

GitHub Issue:
- Title: Add implementation phases to build-out plan (ADR-032)
- Number: #41
- Milestone: none
- Labels: feature

Goal
Establish phases as the executable unit between MVP scope and a release. Settle the artefact shape so ADR-036 (granularity) and ADR-037 (milestone lifecycle) can build on a stable contract.

Why it matters
Today the kit treats MVP scope as a single cut; for large projects this is too coarse. Phased delivery (foundation → core → polish → scale) needs a first-class home so downstream skills can sequence work, milestones, and releases. ADRs #36 (granularity) and #37 (milestone lifecycle) explicitly depend on this shape; landing #41 unblocks both.

Requirements
- Update `templates/build-out-plan-template.md` with `## Phase N: <name>` sections (goal, scope bullets, ADR dependencies, exit criterion)
- Update `skills/prd-to-mvp/SKILL.md` to emit a phased plan (default single phase for small projects)
- Update `skills/adr-writer/SKILL.md` to support a `phase:` frontmatter tag on ADRs (so the index and traceability chain pick it up)
- Update `skills/issue-planner/SKILL.md` to create one GitHub milestone per phase, assigning issues by phase
- Update `skills/workflow-docs/SKILL.md` to surface phases in the generated README's roadmap section
- Update `skills/release/SKILL.md` to default to one phase per release (still configurable)
- Update example projects under `examples/` to include at least one phased example (3-phase target)
- Document the single-phase fallback (a plan with no `## Phase` headings is one implicit phase) in the workflow guide

Acceptance criteria
- Phased build-out plans round-trip through the full chain (prd → plan → ADRs → issues → milestones → release)
- Flat (no-phase) plans continue to produce one milestone per project as today
- ADR phase tags surface in the ADR index and on linked issues
- An example project demonstrates a 3-phase build end-to-end

Scope and constraints
- Primary folders to touch: `templates/`, `skills/prd-to-mvp/`, `skills/adr-writer/`, `skills/issue-planner/`, `skills/workflow-docs/`, `skills/release/`, `examples/`, `docs/`
- Folders to avoid unless absolutely necessary: `design/adr/` (never edit accepted ADRs in place per CLAUDE.md), `bin/`, `.github/`
- Coordination note: issue #40 / PR #49 (ADR-031) is also touching `skills/adr-writer/SKILL.md` and `skills/issue-planner/SKILL.md` as Optional input additions. Branch off `main` *after* PR #49 merges, OR be prepared to rebase. The two changes are additive and should not conflict semantically, but ordering avoids merge churn.
- Single-phase fallback must be lossless: existing projects with flat build-out plans must continue producing identical issues, milestones, and release notes after this change lands.

Evaluation & testing requirements
- Manually invoke `prd-to-mvp` on a small sample and verify it emits a phased plan with sensible phase boundaries
- Manually verify a flat plan (no `## Phase` headings) still produces a single milestone via `issue-planner` and a single release via `/release`
- Verify the ADR index (`design/adr/README.md`) shows phase tags after running `bin/sync-adr-index` against a phase-tagged ADR
- Verify the worked example project under `examples/projects/` demonstrates a 3-phase build with phase-tagged ADRs and one milestone per phase
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-032-implementation-phases.md`
   - any existing modules under `templates/`, `skills/prd-to-mvp/`, `skills/adr-writer/`, `skills/issue-planner/`, `skills/workflow-docs/`, `skills/release/`, `examples/`
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
