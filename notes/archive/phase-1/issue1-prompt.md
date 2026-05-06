You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The architecture and product direction are described in the MVP spec and related design docs in the repository.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-001-project-local-installation-model.md`
- Decision: Use a project-local installation model for the workflow kit in v1.

GitHub Issue:
- Title: Create repository skeleton and project-local installation structure (ADR-001)
- Number: #1
- Milestone: M1 - Foundation + ADRs
- Labels: design, infra

Goal
Establish the base repo layout and the target-project installation model so the rest of the kit can be built on a stable structure.

Why it matters
ADR-001 decides that the workflow kit will be installed into each new target project instead of relying on a global shared install. The repo structure needs to reflect that decision clearly and consistently.

Requirements
- Create the top-level repository folders for `docs/`, `skills/`, `templates/`, and `examples/`
- Define the expected target-project structure for `.claude/skills/`, `Design/`, `notes/`, and `.github/`
- Add placeholder files where needed to make the structure explicit
- Document which files belong in the kit repo versus the target project
- Add a short note describing the installation flow at a structural level

Acceptance criteria
- The repository contains a clear and coherent base directory structure
- The project-local installation model is visible in the folder and file layout
- It is clear which artifacts stay in the kit repo and which are copied into a new target project
- The structure supports later work on docs, templates, and skills without rework

Scope and constraints
- Primary folders to touch: repository root, `docs/`, `skills/`, `templates/`, `examples/`, `notes/`, `Design/`
- Folders to avoid unless absolutely necessary: any future app/demo folders not related to the toolkit structure
- Keep the implementation lightweight and documentation-first
- Do not invent unnecessary automation yet
- Prefer placeholder files and clear folder conventions over premature code

Evaluation & testing requirements
- If no code is added, document verification steps instead of forcing unit tests
- If helper scripts or structured config files are added, include appropriate validation or tests
- Confirm that all changes stay aligned with ADR-001
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-001-project-local-installation-model.md`
   - the MVP/product spec in the repo
   - `generic-project-workflow.md`
   - the current root directory structure
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which folders and placeholder files you will create,
   - which existing files you will modify,
   - how you will document the difference between kit-repo artifacts and target-project artifacts,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue’s scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not start work on docs beyond what is necessary to explain the structure.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for Issues #2–#4,
   - exact commands I should run to inspect the repo structure myself.

Do not start editing files until I explicitly approve your plan.
