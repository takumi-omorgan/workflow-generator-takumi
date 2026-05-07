You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It relies on repo-local documentation and templates for generated workflow artifacts.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-005-documentation-and-template-architecture.md`
- Decision: Generate documentation and templates directly into the target repository.

GitHub Issue:
- Title: Create documentation and template scaffold for generated project artifacts (ADR-005)
- Number: #4
- Milestone: M1 - Foundation + ADRs
- Labels: docs, feature

Goal
Define and add the first template set for core workflow artifacts so later skills can generate consistent outputs.

Why it matters
The workflow kit depends on consistent repo-local artifacts such as ADRs, issue templates, PR templates, `CLAUDE.md`, and AI summaries. These should start from clear templates rather than ad hoc generation.

Requirements
- Create `templates/adr-template.md`
- Create `templates/issue-template.md`
- Create `templates/pr-template.md`
- Create `templates/claude-md-template.md`
- Create `templates/ai-summary-template.md`
- Create `templates/mvp-template.md`
- Create `templates/build-out-plan-template.md`
- Add brief notes on intended use for each template

Acceptance criteria
- All core templates for the MVP exist in the repo
- The template names and responsibilities are clear
- The templates reflect the repo-local documentation strategy from ADR-005
- Later skill work can consume these templates without redefining structure

Scope and constraints
- Primary folders to touch: `templates/`, possibly `docs/` for template usage notes
- Folders to avoid unless absolutely necessary: `skills/`, `.github/`, app/demo code
- Keep the templates lightweight but practical
- Do not overfit the templates to one specific product example

Evaluation & testing requirements
- Documentation/template changes do not require code tests unless scripts/config are added
- Verify consistency of headings, terminology, and intended outputs across templates
- Ensure templates align with the ADR and the existing issue/PR workflow model

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-005-documentation-and-template-architecture.md`
   - `generic-project-workflow.md`
   - existing `templates/` and `docs/` folders if present
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which template files you will create,
   - the intended structure of each template,
   - whether any documentation file should be updated alongside them,
   - your validation approach for consistency.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - template validation checks,
   - any open questions for later skills,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
