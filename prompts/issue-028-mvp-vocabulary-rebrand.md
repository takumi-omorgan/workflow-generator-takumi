You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-024-mvp-vocabulary-versus-v1.md`
- Decision: Replace "In v1 / Not in v1" with "In scope / Out of scope"
  across the kit's MVP scoping framework. Keep the filename
  `design/mvp.md` and skill name `prd-to-mvp` unchanged.

GitHub Issue:
- Title: Replace MVP "In v1 / Not in v1" headings with neutral
  "In scope / Out of scope" (ADR-024)
- Number: #28
- Milestone: v3.0.0 — kit hygiene and licensing
- Labels: feature, docs

Goal
Rebrand the kit's MVP scoping vocabulary from "In v1 / Not in v1" to
"In scope / Out of scope" across templates, skills, examples, and
the reference workflow, so the kit reads correctly for the widest
range of project shapes.

Why it matters
"v1" headings exclude project shapes that don't use a versioning
model (libraries on semver where v1 has a specific meaning,
refactors, infrastructure projects, websites, hobby projects,
research code). The kit's design goal is widest applicability; the
heading should not bake in a project-shape assumption. Neutral
phrasing works for every shape; the temporal "first cut, more
later" signal is recoverable in the filename and surrounding prose.

Requirements
- `templates/mvp-template.md`: rename `### In v1` → `### In scope`,
  `### Not in v1` → `### Out of scope`. Update the guidance prose
  in the file's leading comment and the acceptance-criteria
  section to match. Reword the lower "Out of scope (deferred)"
  section to "Deferred to later" to avoid clashing with the new
  "Out of scope" heading.
- `templates/readme-template.md`: rename placeholders
  `{{IN_V1_BULLETS}}` → `{{IN_SCOPE_BULLETS}}`,
  `{{NOT_IN_V1_BULLETS}}` → `{{OUT_OF_SCOPE_BULLETS}}`. Update
  rendered headings (`## What is in v1` → `## What is in scope`,
  `### Not in v1` → `### Out of scope`) and the placeholder-table
  comment.
- `templates/prd-template.md`: reword the line "v1 is the MVP's
  job, not the PRD's" to drop "v1" while keeping the meaning.
- Update skills:
  - `skills/prd-to-mvp/SKILL.md` and `example.md`
  - `skills/idea-to-prd/SKILL.md` and `example.md`
  - `skills/prd-normalizer/SKILL.md` and `examples.md`
  - `skills/issue-planner/SKILL.md` and `example.md` (incl.
    validation-language section)
  - `skills/workflow-docs/SKILL.md` and `example.md` (incl.
    placeholder-mapping table and section-detection table)
  - `skills/adr-writer/SKILL.md` and `example.md` (incidental
    "v1 scope" leaks)
  - `skills/claude-issue-executor/SKILL.md` (drop
    "v1 of this skill" language)
- Rebuild example projects:
  - `examples/projects/kb-lookup/design/mvp.md`,
    `design/prd.md`, `CLAUDE.md`, `README.md`,
    `issues/issue-002-kb-cli-command.md`,
    `design/adr/adr-001-shortcut-data-format.md`
  - `examples/projects/slug-utils/design/mvp.md`,
    `design/prd.md`, `README.md`,
    `issues/issue-002-unslugify-and-publish.md`,
    `design/adr/adr-001-public-api-surface.md`
- Update top-level walkthroughs:
  `examples/idea-only-example.md`,
  `examples/custom-prd-example.md`,
  `examples/standard-prd-example.md`.
- Leave `generic-project-workflow.md` "v1" mentions alone — those
  are real-product domain examples (deprecated v1 API endpoints,
  semver milestone planning), not MVP scoping vocabulary.
- Update `notes/feature-ideas.md` entry #21 status to `shipped`
  with the ADR link.

Acceptance criteria
- `grep -rn -E "(In v1|Not in v1|IN_V1|NOT_IN_V1)" templates/ skills/ examples/`
  returns no matches.
- `grep -rn "\bv1\b" templates/ skills/ examples/` returns only
  legitimate semver/target-project examples (the changelog flag
  defaults `--from=v1.2.0`, the AI-summary placeholder example
  `{{e.g. MVP, Beta, v1.0}}`).
- `design/mvp.md` filename and `prd-to-mvp` skill name unchanged.
- The "first cut, more later" signal is preserved via the
  filename, the skill name, and section intro prose — readers do
  not lose the temporal meaning.
- ADR-024 is `accepted` and the ADR index reflects that.

Scope and constraints
- Primary folders to touch: `templates/`, `skills/`, `examples/`,
  `design/adr/`, `notes/`.
- Folders to avoid: `bin/`, `docs/`, `design/` (other than
  `design/adr/`), the kit's own `CLAUDE.md`.
- No backwards-compat shim — the kit has not shipped externally,
  so old placeholder names do not need to remain accepted.
- Do not rename `design/mvp.md` or the `prd-to-mvp` skill.

Evaluation & testing requirements
- After the sweep, run the two grep commands listed in
  Acceptance criteria.
- Open `templates/mvp-template.md` and confirm the rendered
  structure still makes sense as an MVP scoping doc.
- Open `examples/projects/kb-lookup/design/mvp.md` and
  `examples/projects/slug-utils/design/mvp.md` and confirm both
  read coherently after the rebrand.
- All existing tests continue to pass.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-024-mvp-vocabulary-versus-v1.md`
   - all template files under `templates/`
   - all skill files listed in Requirements
   - all example files listed in Requirements
2. Propose a short, step-by-step PLAN:
   - groupings for the sweep (templates → skills → examples →
     walkthroughs → feature-ideas update),
   - any non-obvious phrasing decisions,
   - how to handle the existing "Out of scope (deferred)" section
     in `mvp-template.md` (rename to avoid clashing with the new
     "Out of scope" heading).
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one logical commit per concern (templates, skills, examples,
     walkthroughs),
   - each commit references ADR-024 and #28.
5. At the end, provide an evaluation summary:
   - what changed (file count by category),
   - grep verification results,
   - any follow-up work for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.

---

**Retrospective note (2026-04-26):** This prompt is the canonical
session brief that should have driven this work. The implementation
was performed interactively in a session that did not follow the
formal `/prepare-issue` → `/claude-issue-executor` flow. This file
is preserved as the audit trail and as an exemplar for future
large-sweep rebrands.
