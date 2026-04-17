You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-015-pr-review-packager-skill.md`
- Decision: Build a pr-review-packager skill that creates PRs with proper template, links, and summaries.

GitHub Issue:
- Title: Build pr-review-packager skill (ADR-015)
- Number: #17
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build the pr-review-packager skill that creates pull requests with proper template formatting, issue and ADR links, and change summaries derived from commit history.

Why it matters
Consistent, well-structured PRs make code review faster and maintain a clear audit trail from ADR decisions through implementation to merge. Automating the PR body from templates and commit history removes manual busywork and reduces the chance of missing links or context.

Requirements
- Draft the PR body from `templates/pr-template.md`
- Fill in `Closes #N` and ADR references automatically from the branch or commit history
- Derive a change summary from the commit history on the current branch
- Present the draft PR to the user for review and approval before creation
- Create the PR via `gh pr create` after approval
- Support setting labels, milestone, and reviewers if configured

Acceptance criteria
- The skill produces well-structured PRs matching the PR template
- Issue and ADR links are correct and present in the PR body
- The change summary accurately reflects the commits on the branch
- The user approves the PR draft before it is created
- The skill handles edge cases (no template file, no commits, detached HEAD) gracefully

Scope and constraints
- Primary folders to touch: `skills/pr-review-packager/`
- Folders to avoid unless absolutely necessary: other skills, core templates (read but do not modify `templates/pr-template.md`)
- Keep the skill focused on PR packaging, not on review feedback or CI checks
- Do not modify the PR template itself; consume it as-is

Evaluation & testing requirements
- Verify that the skill correctly parses the PR template and fills placeholders
- Confirm that ADR and issue references are extracted from commit messages
- Test with a branch that has multiple commits referencing different issues
- Confirm the user approval gate works (no PR created without explicit approval)
- All existing tests must continue to pass

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-015-pr-review-packager-skill.md`
   - `templates/pr-template.md`
   - `generic-project-workflow.md`
   - any existing skills in `skills/` for structure conventions
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files and folders you will create,
   - how the skill reads and fills the PR template,
   - how commit history is parsed for links and summaries,
   - how user approval is handled,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing ADR-015 and issue #17,
   - write tests alongside implementation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to verify the skill.

Do not start editing files until I explicitly approve your plan.
