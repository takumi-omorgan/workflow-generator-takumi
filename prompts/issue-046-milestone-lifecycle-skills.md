You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-037-milestone-lifecycle.md`
- Decision: Adopt Option A — three composable skills (`/audit-milestone`, `/milestone-summary`, `/complete-milestone`) layered on ADR-032's phase structure, implemented after ADR-032 has shipped and at least one project has run a real milestone end-to-end.

GitHub Issue:
- Title: Add milestone lifecycle skills: /audit-milestone, /milestone-summary, /complete-milestone (ADR-037)
- Number: #46
- Milestone: none <!-- TODO: issue body says v-next; not attached as a GitHub milestone -->
- Labels: feature

Goal
Formalise the boundary between phases and releases. Give large projects visible delivery checkpoints and routine retrospective artefacts.

Why it matters
Today `/release` covers tag-and-publish but not "did we actually finish what this milestone promised?" These three skills close that gap once ADR-032's phases exist and have been exercised end-to-end on a real project.

Requirements
- Add `templates/milestone-summary-template.md` (what shipped, ADRs adopted, lessons learned, deferred work).
- Add `skills/audit-milestone/SKILL.md` — verifies all phases complete, all issues closed, all referenced ADRs have linked PRs; warns on failure but does not block `/complete-milestone`.
- Add `skills/milestone-summary/SKILL.md` — generates `Design/milestones/N-summary.md` from `git log`, the GitHub milestone, and accepted ADRs in the phase range.
- Add `skills/complete-milestone/SKILL.md` — closes the GitHub milestone, archives milestone-scoped state per ADR-035, and optionally chains `/release` (ADR-017).
- Document one-milestone-per-release as the default, with explicit decoupling option.
- Add a worked example showing milestone close → release on one of the example projects.

Acceptance criteria
- `/audit-milestone N` returns a clear pass/fail with gap list on a real (or seeded) project.
- `/milestone-summary N` produces a useful summary doc without further authoring.
- `/complete-milestone N` closes the GitHub milestone, archives state, and either invokes `/release` or skips it cleanly.
- The three skills compose: any order, any subset, no hidden coupling beyond the documented chain.

Scope and constraints
- Primary folders to touch: `skills/audit-milestone/`, `skills/milestone-summary/` (new), `skills/complete-milestone/` (new), `templates/`, `docs/workflow-guide.md`, `skills/README.md`.
- Folders to avoid unless absolutely necessary: `Design/adr/` (ADR-037 is accepted — do not edit), `bin/`, unrelated existing skills.
- Depends on ADR-032 (#41, phases) and ADR-035 (#44, `state.md`); both have shipped. Skills must use `gh` for all GitHub reads/writes (per ADR-004) and rewrite only between marker fences in `Design/state.md` (per ADR-035).

Evaluation & testing requirements
- Seed a minimal milestone (one phase, one issue, one ADR-linked PR) and run `/audit-milestone` against it; verify pass and fail paths.
- Run `/milestone-summary` end-to-end and verify the generated `Design/milestones/N-summary.md` matches `templates/milestone-summary-template.md`.
- Run `/complete-milestone` and verify the GitHub milestone is closed, `Design/state.md` is archived correctly, and the optional `/release` chain works in both modes (chained / skipped).
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-037-milestone-lifecycle.md`
   - `Design/adr/adr-032-build-out-plan-phases.md` (phase structure this layers on)
   - `Design/adr/adr-035-state-md-session-continuity.md` (state archive contract)
   - `skills/release/SKILL.md` (chain target)
   - `templates/` and `skills/` for existing patterns
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue
     (e.g. "feat(skills): add audit-milestone skill (ADR-037, #46)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
