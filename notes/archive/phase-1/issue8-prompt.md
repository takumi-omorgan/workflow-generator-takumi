You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It uses an issue-by-issue, plan-first Claude Code execution model.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-006-claude-code-execution-model.md`
- Decision: Use issue-by-issue, plan-first Claude Code execution in v1.

GitHub Issue:
- Title: Implement issue execution workflow assets for Claude Code sessions (ADR-006)
- Number: #8
- Milestone: M3 - Execution Workflow
- Labels: design, docs, feature

Goal
Add the prompt and documentation assets required for issue-by-issue implementation with Claude Code.

Why it matters
The execution model is one of the strongest differentiators of the workflow kit. It needs explicit prompt structure and usage guidance.

Requirements
- Add `notes/issue-prompt.md`
- Adapt the generic issue prompt framework for this repository
- Document how to fill the prompt before each work session
- Document the required evaluation summary at the end of a session
- Add one sample filled issue prompt

Acceptance criteria
- The repo contains a reusable issue prompt for Claude Code sessions
- The prompt reflects the plan-first, test-alongside-code workflow
- Documentation explains when and how to use it
- A sample filled prompt makes the pattern easy to apply

Scope and constraints
- Primary folders to touch: `notes/`, possibly `docs/`
- Folders to avoid unless absolutely necessary: `skills/` beyond references, `.github/`
- Keep the prompt generic enough for repo reuse but concrete enough to be useful
- Align it closely with the example framework in the Space, adapted for this repository

Evaluation & testing requirements
- If only docs/templates are added, use verification and consistency checks rather than forced code tests
- Confirm that the prompt structure matches the intended execution workflow and references the right repo artifacts

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-006-claude-code-execution-model.md`
   - `generic-project-workflow.md`
   - the example issue prompt framework used in this project planning effort
   - existing `notes/` docs
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files you will create or update,
   - how you will adapt the prompt for this repository,
   - what documentation sections you will add,
   - what sample filled prompt you will include,
   - your verification approach.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - consistency checks performed,
   - any follow-up improvements,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
