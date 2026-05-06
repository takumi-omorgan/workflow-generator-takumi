You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- None — this is a project management task to create the GitHub milestone and issues for v-next.

GitHub Issue:
- Title: Create GitHub milestone M5 and issues #11-#23 for v-next
- Number: #25
- Milestone: M5 - v-next
- Labels: infra

Goal
Create the GitHub milestone "M5 - v-next" and GitHub issues #11-#23 for all v-next features, so the project's GitHub issue tracker reflects the planned work and each issue links back to its ADR.

Why it matters
The v-next features have been scoped through ADRs (007-021) but do not yet exist as trackable GitHub issues. Creating the milestone and issues brings the project management layer in line with the design work, enabling assignment, prioritization, and progress tracking through GitHub's native tools.

Requirements
- Create GitHub milestone "M5 - v-next"
- Create GitHub issues for each ADR from 007 through 021 (13 issues total, numbered #11-#23)
- Each issue should have a clear title referencing its ADR number
- Each issue body should reference the relevant ADR file path and summarize the decision
- Apply appropriate labels to each issue (e.g., feature, docs, infra, design)
- Assign all issues to the M5 milestone

Acceptance criteria
- GitHub milestone "M5 - v-next" exists
- GitHub issues #11-#23 are created, one per ADR (007-021)
- Each issue title includes the ADR number
- Each issue body links to the corresponding ADR file
- All issues are assigned to the M5 milestone
- Labels are applied consistently and appropriately

Scope and constraints
- Primary folders to touch: none (this is GitHub-only work using `gh` CLI)
- Folders to avoid unless absolutely necessary: all — no file changes should be needed
- Use the `gh` CLI for all GitHub operations
- Do not modify any repository files

Evaluation & testing requirements
- Verify milestone exists via `gh api repos/:owner/:repo/milestones`
- Verify all issues exist via `gh issue list --milestone "M5 - v-next"`
- Confirm each issue body references the correct ADR
- Check that labels and milestone assignments are correct

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - list the ADR files under `Design/adr/` (007 through 021) to get titles and summaries
   - check existing GitHub milestones and issues via `gh` CLI
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the milestone creation command,
   - the list of issues to create with their titles, labels, and ADR references,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - create the milestone first,
   - create issues in order,
   - verify each was created correctly.
5. At the end, provide an evaluation summary:
   - what was created,
   - verification steps performed,
   - any issues that could not be created or need manual follow-up,
   - exact `gh` commands I should run to inspect the results.

Do not start editing files until I explicitly approve your plan.
