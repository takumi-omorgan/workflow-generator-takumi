You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is GitHub-first and relies on consistent issue and PR structure.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADRs:
- File: `design/adr/adr-004-github-first-workflow-model.md`
- Decision: Use a GitHub-first workflow model in v1.
- File: `design/adr/adr-005-documentation-and-template-architecture.md`
- Decision: Generate documentation and templates directly into the target repository.

GitHub Issue:
- Title: Add GitHub issue templates and PR template to the repository (ADR-004, ADR-005)
- Number: #9
- Milestone: M3 - Execution Workflow
- Labels: docs, feature, infra

Goal
Create the `.github` templates that standardize issue creation and pull request quality.

Why it matters
GitHub templates are one of the simplest ways to enforce consistency in issue reporting and PR review.

Requirements
- Add `.github/ISSUE_TEMPLATE/feature-request.md`
- Add `.github/ISSUE_TEMPLATE/docs-task.md`
- Add `.github/pull_request_template.md`
- Ensure the template structure aligns with the workflow docs and ADR references
- Add brief usage notes in documentation

Acceptance criteria
- The repository contains issue and PR templates in supported GitHub locations
- Templates reflect the project workflow structure
- Contributors opening issues and PRs are guided into consistent formats
- The docs mention where these templates live and how they are used

Scope and constraints
- Primary folders to touch: `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`, possibly `docs/`
- Folders to avoid unless absolutely necessary: `skills/`, unrelated planning docs
- Keep template fields practical and aligned with your current issue/PR style
- Do not add excessive GitHub automation beyond templates in this issue

Evaluation & testing requirements
- No code tests required unless automation/scripts are added
- Verify that template file paths and names are valid for GitHub
- Confirm that the template content matches the issue structure already used in the repo

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-004-github-first-workflow-model.md`
   - `design/adr/adr-005-documentation-and-template-architecture.md`
   - `generic-project-workflow.md`
   - existing GitHub issue and PR conventions already used in the repo
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which template files you will create,
   - the fields/sections each template will contain,
   - whether a docs update is needed,
   - your verification approach for GitHub compatibility.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - compatibility checks performed,
   - any follow-up template improvements,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
