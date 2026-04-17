You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-011-issue-planner-skill.md`
- Decision: Build an issue-planner skill that reads the MVP and build-out plan to create GitHub issues in batch.

GitHub Issue:
- Title: issue-planner skill (ADR-011)
- Number: #14
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build an issue-planner skill that reads `Design/mvp.md` and `Design/build-out-plan.md`, drafts GitHub issues with titles, bodies, labels, milestones, and ADR references, and creates them via `gh issue create` after user approval.

Why it matters
Turning a build-out plan into GitHub issues is one of the most tedious and error-prone steps in the workflow. Automating issue creation from the plan ensures consistency, saves time, and keeps issues tightly linked to ADRs and milestones.

Requirements
- Create the skill in `skills/issue-planner/`
- The skill must read `Design/mvp.md` and `Design/build-out-plan.md` to extract planned work items
- Draft issues with structured titles, bodies, labels, milestones, and ADR references
- Present the full batch of drafted issues to the user for review and approval before creating any
- Create approved issues via `gh issue create` with correct labels and milestone assignments
- Create a GitHub Project board and add the created issues to it (ADR-012)
- Handle edge cases: missing plan files, empty milestones, issues that already exist
- Support dry-run mode that shows what would be created without making API calls

Acceptance criteria
- `skills/issue-planner/` exists with the skill implementation
- The skill reads MVP and build-out plan files and produces well-structured issue drafts
- Each drafted issue includes title, body, labels, milestone, and ADR references where applicable
- The user must explicitly approve before any issues are created on GitHub
- Issues are created via `gh issue create` with correct metadata
- A GitHub Project board is created and issues are added to it
- Dry-run mode works and shows the planned issues without side effects
- The skill handles missing or malformed input files gracefully

Scope and constraints
- Primary folders to touch: `skills/issue-planner/`
- Folders to avoid unless absolutely necessary: `bin/`, `templates/`, `docs/` (except to document the skill)
- The skill must use `gh` CLI for all GitHub API interactions
- Do not build a web UI or dashboard
- Keep the skill focused on issue creation; do not add PR or branch automation

Evaluation & testing requirements
- Test the skill with a sample MVP and build-out plan
- Verify dry-run mode produces correct output without creating issues
- Verify created issues have correct titles, bodies, labels, milestones, and ADR references
- Verify the GitHub Project board is created and populated
- Confirm that all changes stay aligned with ADR-011 and ADR-012
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-011-issue-planner-skill.md`
   - `Design/adr/adr-012-github-project-board.md` (if it exists)
   - `generic-project-workflow.md`
   - `Design/mvp.md` and `Design/build-out-plan.md` (as reference for the input format)
   - existing skills in `skills/` for style and conventions
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - how the skill will parse the plan files,
   - the issue draft format and fields,
   - the approval flow,
   - how the GitHub Project board will be created,
   - your testing plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not add PR or branch automation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to test the skill myself.

Do not start editing files until I explicitly approve your plan.
