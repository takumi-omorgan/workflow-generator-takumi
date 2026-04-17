You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-014-claude-issue-executor-skill.md`
- Decision: Build a claude-issue-executor skill that drives disciplined implementation sessions from prepared issue prompts.

GitHub Issue:
- Title: Build claude-issue-executor skill (ADR-014)
- Number: #16
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build the claude-issue-executor skill that drives disciplined implementation sessions. The skill reads a prepared prompt file, enters plan mode, enforces plan-first discipline, implements with incremental commits, and produces an evaluation summary.

Why it matters
The execution phase of the workflow currently relies on manual discipline. A dedicated skill that enforces the ADR-006 execution model ensures every implementation session follows the same plan-first, commit-incrementally, evaluate-at-the-end pattern without relying on the user to remember each step.

Requirements
- Read prepared prompt from `prompts/issue-NNN-*.md` (or `notes/issueN-prompt.md`) to bootstrap the session
- Enter plan mode and propose a step-by-step implementation plan for user approval
- After approval, create a feature branch following the repo's branch naming conventions
- Implement changes with incremental commits, each referencing the ADR and issue number
- Write tests alongside implementation where applicable
- Produce an evaluation summary at the end covering what changed, verification steps, and follow-up work
- Enforce the ADR-006 execution model throughout the session

Acceptance criteria
- The skill orchestrates a full implementation session from prompt file to evaluation summary
- Plan-first discipline is enforced: no edits happen before the user approves the plan
- Each commit references the relevant ADR and issue number
- An evaluation summary is produced at the end of the session
- The skill handles missing or malformed prompt files gracefully

Scope and constraints
- Primary folders to touch: `skills/claude-issue-executor/`
- Folders to avoid unless absolutely necessary: other skills, templates, or docs not related to execution
- Keep the skill focused on orchestration, not on duplicating logic from other skills
- Do not invent new workflow steps beyond what ADR-006 and ADR-014 describe

Evaluation & testing requirements
- Verify that the skill reads and parses a sample prompt file correctly
- Confirm that the plan-first gate works (no file edits before approval)
- Test with at least one real or synthetic issue prompt end-to-end
- All existing tests must continue to pass

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-014-claude-issue-executor-skill.md`
   - `Design/adr/adr-006-*` (execution model ADR)
   - `generic-project-workflow.md`
   - any existing skills in `skills/` for structure conventions
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files and folders you will create,
   - how the skill reads and validates the prompt file,
   - how plan-first discipline is enforced,
   - how commits are structured,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing ADR-014 and issue #16,
   - write tests alongside implementation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to verify the skill.

Do not start editing files until I explicitly approve your plan.
