You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is designed for project-local installation and supports new projects only in v1.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADRs:
- File: `design/adr/adr-001-project-local-installation-model.md`
- Decision: Use a project-local installation model for the workflow kit in v1.
- File: `design/adr/adr-002-new-project-only-scope.md`
- Decision: Limit v1 to new-project setup only.

GitHub Issue:
- Title: Write install guide and document v1 scope constraints (ADR-001, ADR-002)
- Number: #2
- Milestone: M1 - Foundation + ADRs
- Labels: design, docs

Goal
Create installation and scope documentation that explains how the kit is used and what it does not support in v1.

Why it matters
The product boundary is one of the most important parts of the MVP. Users need to understand that this is a project-local toolkit for new projects, not a retrofit tool for existing repositories.

Requirements
- Draft `README.md` overview content for the product boundary
- Draft `docs/install.md`
- Explain prerequisites such as Git, GitHub CLI, and Claude Code
- Explain the project-local install model
- Clearly document that v1 is for new projects only
- Add a short quick-start flow for first-time users

Acceptance criteria
- The installation path is clearly documented
- The new-project-only scope is explicit and easy to understand
- A first-time user can tell whether the kit is a fit for their project
- The docs reduce ambiguity about how and where the kit is installed

Scope and constraints
- Primary folders to touch: `README.md`, `docs/install.md`, possibly `docs/`
- Folders to avoid unless absolutely necessary: `skills/`, `templates/`, `.github/`
- Keep the docs practical and concise
- Do not claim support for existing project migration
- Keep wording aligned with ADR-001 and ADR-002

Evaluation & testing requirements
- Documentation changes do not require code tests unless scripts/config are added
- Verify internal consistency across README and install guide
- Ensure the quick-start steps are realistic for a first-time user
- If commands are included, make sure they are coherent and in the right order

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-001-project-local-installation-model.md`
   - `design/adr/adr-002-new-project-only-scope.md`
   - `generic-project-workflow.md`
   - the current `README.md` and `docs/` structure
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files you will create or update,
   - the section structure for `README.md` and `docs/install.md`,
   - how you will explain prerequisites and quick start,
   - your verification approach for clarity and consistency.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - consistency checks performed,
   - any follow-up doc gaps,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
