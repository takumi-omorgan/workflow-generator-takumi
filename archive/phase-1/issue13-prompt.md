You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-009-installer-script.md`
- Decision: Provide a bin/install-workflow-kit bash script to automate the project-local installation flow.

GitHub Issue:
- Title: Installer script (ADR-009)
- Number: #13
- Milestone: M5 - v-next
- Labels: feature, infra

Goal
Create `bin/install-workflow-kit`, a bash script that automates the install flow: scaffolding folders, copying skills, rendering CLAUDE.md from the template, and making an initial commit in the target project.

Why it matters
The manual installation steps documented in the install guide are repetitive and error-prone. An installer script reduces friction, ensures consistency, and makes it practical to spin up new projects quickly while keeping the manual flow documented as a fallback.

Requirements
- Create `bin/install-workflow-kit` as a portable bash script
- The script must scaffold `Design/adr/`, `prompts/`, and `notes/` in the target project
- Copy skills from the kit repo into the target project's `.claude/skills/`
- Render `CLAUDE.md` from `templates/claude-md-template.md` (ADR-007), prompting for placeholder values or accepting them as arguments
- Make an initial commit with a clear message after scaffolding
- Support a `--with-docs` flag that also copies workflow docs into the target project (ADR-010)
- Update `docs/install.md` to document the script usage alongside the manual flow
- Update the README quick-start section to reference the installer script
- The script must be idempotent: running it twice should not break an already-scaffolded project

Acceptance criteria
- `bin/install-workflow-kit` exists, is executable, and runs successfully on a fresh git repo
- The script scaffolds the correct directory structure matching `docs/repo-structure.md`
- Skills are copied into `.claude/skills/`
- CLAUDE.md is rendered from the template with user-supplied values
- An initial commit is created
- `--with-docs` flag works and copies additional docs
- `docs/install.md` documents the script usage
- README quick-start references the installer
- The manual installation flow remains documented and functional

Scope and constraints
- Primary folders to touch: `bin/` (new), `docs/`
- Folders to avoid unless absolutely necessary: `skills/` (read-only source), `templates/` (read-only source)
- Keep the script simple and portable (bash, no exotic dependencies)
- Do not build a package manager or distribution mechanism
- The script should work on macOS and Linux

Evaluation & testing requirements
- Test the script on a fresh empty git repo and verify the resulting structure
- Test the `--with-docs` flag
- Test idempotency by running the script twice
- Verify the manual install flow still works independently
- Confirm that all changes stay aligned with ADR-009
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-009-installer-script.md`
   - `generic-project-workflow.md`
   - `docs/install.md`
   - `docs/repo-structure.md`
   - `templates/claude-md-template.md` (from ADR-007 / Issue #11)
   - the current README
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the script's argument interface and flags,
   - the scaffolding steps in order,
   - how CLAUDE.md rendering will work,
   - how idempotency will be handled,
   - your testing plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not add features beyond what is specified here.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to test the installer myself.

Do not start editing files until I explicitly approve your plan.
