You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-008-dedicated-prompts-folder.md`
- Decision: Introduce a dedicated prompts/ folder in the target project layout and provide a prompt template.

GitHub Issue:
- Title: Dedicated prompts/ folder and prompt template (ADR-008)
- Number: #12
- Milestone: M5 - v-next
- Labels: feature, design, infra

Goal
Create a `prompts/` directory structure with a `_template.md` file and update `docs/repo-structure.md` to reflect the new layout so that issue prompts have a proper home in target projects.

Why it matters
Issue prompts currently live in `notes/`, which mixes planning notes with session prompts. A dedicated `prompts/` folder makes it easier to find, manage, and template session prompts, and keeps the project layout clean as the number of issues grows.

Requirements
- Create `prompts/_template.md` based on the existing `notes/issue-prompt.md` pattern
- Update `docs/repo-structure.md` to include the `prompts/` folder in the target project layout
- Update the install guide to mention the `prompts/` folder as part of the scaffolded structure
- Ensure the template includes all standard sections: Context, ADR, GitHub Issue, Goal, Requirements, Acceptance criteria, Scope, Evaluation, and Instructions
- Add a short README or header comment in the template explaining how to use it

Acceptance criteria
- `prompts/_template.md` exists and follows the established issue-prompt structure
- `docs/repo-structure.md` is updated to show the `prompts/` folder in the target project layout
- The install guide references the `prompts/` folder
- The template is consistent with the format used in `notes/issue1-prompt.md` through `notes/issue10-prompt.md`
- Existing notes/ files are not moved or broken

Scope and constraints
- Primary folders to touch: `prompts/` (new), `notes/`, `docs/`
- Folders to avoid unless absolutely necessary: `bin/`, `skills/`, `examples/`
- Do not migrate existing notes/issueN-prompt.md files in this issue
- Do not build automation to generate prompts from issues yet (that is a later issue)
- Keep the change lightweight and documentation-first

Evaluation & testing requirements
- Verify the template renders a coherent prompt when filled in manually
- Confirm `docs/repo-structure.md` accurately reflects the new folder
- Confirm the install guide is consistent with the updated structure
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-008-dedicated-prompts-folder.md`
   - `generic-project-workflow.md`
   - `notes/issue-prompt.md` and `notes/issue1-prompt.md` (as reference for the template)
   - `docs/repo-structure.md`
   - the current install guide in `docs/`
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the template structure and placeholder conventions,
   - which sections of repo-structure.md you will update,
   - which install guide sections you will update,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not migrate existing prompt files or build automation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
