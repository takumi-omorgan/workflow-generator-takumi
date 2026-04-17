You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-018-workflow-docs-skill.md`
- Decision: Build a /workflow-docs skill that generates README.md and Design/ai-summary.md for target projects.

GitHub Issue:
- Title: Build /workflow-docs skill (ADR-018)
- Number: #20
- Milestone: M5 - v-next
- Labels: feature, design, docs

Goal
Build the /workflow-docs skill that generates README.md and Design/ai-summary.md for target projects by reading existing project artifacts and filling templates.

Why it matters
Every project needs a README and an AI-readable summary, but writing them from scratch is repetitive. A skill that reads the PRD, MVP spec, ADRs, and CLAUDE.md and generates these docs from templates saves time and ensures consistency across projects using the workflow kit.

Requirements
- Read PRD, MVP spec, ADRs, and CLAUDE.md from the target project
- Generate `README.md` from a README template, filling sections from source documents
- Generate `Design/ai-summary.md` from a summary template, providing a concise project overview for AI tools
- Re-runnable: running the skill again updates generated docs without clobbering manual edits (use markers or fenced sections)
- Sections with no source data are omitted rather than left empty or filled with placeholders
- Present the generated docs to the user for review before writing

Acceptance criteria
- The skill generates a useful README.md from project artifacts
- The skill generates a useful Design/ai-summary.md from project artifacts
- Re-running the skill updates generated sections without destroying manual edits outside marked regions
- Template variables are correctly filled from source documents
- Sections without source data are cleanly omitted
- The user reviews generated docs before they are written to disk

Scope and constraints
- Primary folders to touch: `skills/workflow-docs/`
- Folders to avoid unless absolutely necessary: other skills, core templates (read but do not modify), existing project docs outside the generated sections
- Keep the skill focused on doc generation; do not add publishing or deployment logic
- Do not overwrite files without user approval
- Respect existing manual content outside generated markers

Evaluation & testing requirements
- Verify that generated README.md contains correct content from source artifacts
- Verify that generated Design/ai-summary.md is concise and accurate
- Test re-run behavior: confirm manual edits outside markers are preserved
- Test with missing source documents (no PRD, no ADRs, etc.) to confirm graceful omission
- All existing tests must continue to pass

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-018-workflow-docs-skill.md`
   - `generic-project-workflow.md`
   - any existing skills in `skills/` for structure conventions
   - any existing templates in `templates/` that relate to README or summary generation
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files and folders you will create,
   - how source documents are read and parsed,
   - how templates are filled and sections are conditionally included,
   - how re-run safety (marker-based updates) works,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing ADR-018 and issue #20,
   - write tests alongside implementation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to verify the skill.

Do not start editing files until I explicitly approve your plan.
