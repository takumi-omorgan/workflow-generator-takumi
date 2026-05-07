You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is explicitly GitHub-first in v1.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-004-github-first-workflow-model.md`
- Decision: Use a GitHub-first workflow model in v1.

GitHub Issue:
- Title: Write GitHub setup guide and define repo workflow assets (ADR-004)
- Number: #3
- Milestone: M1 - Foundation + ADRs
- Labels: design, docs, infra

Goal
Document the GitHub-first operating model and define the initial repo assets needed to support it.

Why it matters
The kit is explicitly GitHub-first in v1. Users need clear instructions for labels, milestones, branches, issue templates, PR templates, and optional branch protection.

Requirements
- Draft `docs/github-setup.md`
- Define the default label set for new repos
- Define milestone guidance for early project phases
- Define branch naming guidance using `main + feature branch`
- Outline optional branch protection rules
- Define the required `.github` assets to add in a later issue

Acceptance criteria
- The GitHub-first workflow is documented in a practical way
- The default label and milestone strategy is defined
- The branch strategy is clear and consistent with the ADRs
- The required `.github` assets are identified and ready for implementation

Scope and constraints
- Primary folders to touch: `docs/`, possibly `README.md` if cross-links are needed
- Folders to avoid unless absolutely necessary: `.github/` implementation files themselves, `skills/`, `templates/`
- Keep this issue documentation-focused; actual `.github` templates belong in Issue #9
- Stay aligned with existing labels and milestones already created in the repo

Evaluation & testing requirements
- No code tests required unless scripts/config are added
- Verify that branch and milestone guidance matches the current GitHub issue setup
- Confirm that the `.github` assets listed here can be implemented cleanly in Issue #9

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-004-github-first-workflow-model.md`
   - `generic-project-workflow.md`
   - current documentation under `docs/`
   - current labels/milestones guidance already referenced in the repo
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files you will create or update,
   - the section structure for `docs/github-setup.md`,
   - the exact GitHub assets you will define for later implementation,
   - your consistency checks.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - verification performed,
   - any follow-up work for Issue #9,
   - exact files I should inspect.

Do not start editing files until I explicitly approve your plan.
