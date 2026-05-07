You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-007-claude-md-starter-template.md`
- Decision: Ship a CLAUDE.md starter template with meaningful placeholders so target projects get a useful starting point.

GitHub Issue:
- Title: CLAUDE.md starter template (ADR-007)
- Number: #11
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Create `templates/claude-md-template.md` with {{placeholders}} for project name, stack, workflow rules, and GitHub conventions so that new target projects can quickly generate a useful CLAUDE.md.

Why it matters
Every target project needs a CLAUDE.md to guide Claude Code, but writing one from scratch is tedious and error-prone. A well-designed template with documented placeholders lowers the barrier to adoption and ensures consistent quality across projects.

Requirements
- Create `templates/claude-md-template.md` with {{placeholder}} syntax for project name, tech stack, workflow rules, GitHub conventions, and any other project-specific fields
- Document each placeholder field with a short description and example value
- Ensure the template renders a useful, non-trivial CLAUDE.md when all placeholders are filled
- Design the template to work with both manual copy-and-fill and a future installer script
- Include sensible default content for sections that are common across most projects

Acceptance criteria
- `templates/claude-md-template.md` exists and uses consistent {{placeholder}} syntax
- All placeholders are documented (inline or in a companion section)
- Filling in the placeholders produces a CLAUDE.md that is immediately useful for Claude Code
- The template covers at minimum: project name, tech stack, repo conventions, workflow rules, and GitHub settings
- The template is compatible with the project-local installation model from ADR-001

Scope and constraints
- Primary folders to touch: `templates/`
- Folders to avoid unless absolutely necessary: `bin/`, `skills/`, `examples/`
- Keep the template focused and opinionated but not overly prescriptive
- Do not build any rendering or installer logic in this issue

Evaluation & testing requirements
- Manually fill in the template with a sample project to confirm it produces a coherent CLAUDE.md
- Verify placeholder syntax is consistent and grep-friendly
- Confirm that all changes stay aligned with ADR-007
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-007-claude-md-starter-template.md`
   - `generic-project-workflow.md`
   - existing files in `templates/`
   - the current CLAUDE.md in the kit repo as a reference
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the placeholder fields you will include,
   - the template structure and sections,
   - how placeholders will be documented,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not add installer or rendering logic.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
