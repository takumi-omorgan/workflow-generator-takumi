You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-020-end-to-end-workflow-guide.md`
- Decision: Write a distilled docs/workflow-guide.md covering the full workflow from idea to release.

GitHub Issue:
- Title: Write docs/workflow-guide.md — end-to-end workflow guide (ADR-020)
- Number: #22
- Milestone: M5 - v-next
- Labels: docs

Goal
Write docs/workflow-guide.md covering the full workflow from idea to release in one cohesive pass, distilled from the detailed generic-project-workflow.md into a practical, user-facing guide.

Why it matters
The generic-project-workflow.md is comprehensive but dense. Users need a streamlined guide that walks them through the happy path — idea to PRD to MVP to ADRs to issues to branches to PRs to merge to release — without needing to parse the full reference document. This guide also needs to address when the full workflow is overkill (bug fixes, chores, dependency bumps).

Requirements
- Cover the full happy path: idea → PRD → MVP → ADRs → issues → branches → PRs → merge → release
- Distill from generic-project-workflow.md without duplicating it wholesale
- Include a "when you don't need an ADR" section covering bug fixes, chores, and dependency bumps
- Link to skills by /skill-name throughout the guide
- Update README.md to link to this doc
- Update docs/install.md to link to this doc

Acceptance criteria
- docs/workflow-guide.md exists and covers the full happy path in a readable, sequential flow
- "When you don't need an ADR" section is included and covers bug fixes, chores, dependency bumps
- Skills are referenced by /skill-name where relevant
- README.md links to the new guide
- docs/install.md links to the new guide

Scope and constraints
- Primary folders to touch: `docs/`
- Folders to avoid unless absolutely necessary: `skills/`, `templates/`, `design/`
- Keep the guide practical and action-oriented — this is a "how to use" doc, not a reference spec
- Do not rewrite generic-project-workflow.md; link to it as the detailed reference
- Limit changes to README.md and docs/install.md to adding links only

Evaluation & testing requirements
- Verify the guide covers all workflow stages from idea to release
- Verify the ADR-free workflow section is present and accurate
- Confirm links from README.md and docs/install.md resolve correctly
- Check that skill references use /skill-name format consistently

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-020-end-to-end-workflow-guide.md`
   - `generic-project-workflow.md`
   - `README.md`
   - `docs/install.md`
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the structure and sections of the new guide,
   - how the guide relates to generic-project-workflow.md,
   - what changes are needed in README.md and docs/install.md,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not restructure existing docs beyond adding links.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to inspect the results.

Do not start editing files until I explicitly approve your plan.
