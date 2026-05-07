You are working in my workflow-kit repository.

Goal:
Create the initial GitHub project-management setup for the MVP using the approved issue drafts below.

Requirements:
- Use GitHub CLI (`gh`) for GitHub operations.
- First verify `gh auth status`.
- If labels already exist, do not fail; skip or update safely.
- Create exactly these labels if missing:
  - `feature` color `0E8A16`
  - `bug` color `D73A4A`
  - `design` color `1D76DB`
  - `infra` color `FBCA04`
  - `security` color `B60205`
  - `docs` color `0075CA`
- Create this milestone if missing:
  - `M1 - Foundation + ADRs`
- Then create the following GitHub issues with the exact titles and bodies below.
- Before creating anything, show me the exact `gh` commands you plan to run.
- Wait for my approval before executing the commands.
- After execution, give me:
  - the labels created or confirmed,
  - the milestone created or confirmed,
  - the issue numbers and URLs,
  - and any errors or skipped items.

Issue 1 Title:
Create repository skeleton and project-local installation structure (ADR-001)

Issue 1 Body:
## Summary
Create the initial repository skeleton for the Claude Code Workflow Kit and define the project-local installation structure used in v1.

## ADR
Related ADR: `design/adr/adr-001-project-local-installation-model.md`

## Goal
Establish the base repo layout and the target-project installation model so the rest of the kit can be built on a stable structure.

## Why it matters
ADR-001 decides that the workflow kit will be installed into each new target project instead of relying on a global shared install. The repo structure needs to reflect that decision clearly and consistently.

## Tasks
- [ ] Create the top-level repository folders for `docs/`, `skills/`, `templates/`, and `examples/`
- [ ] Define the expected target-project structure for `.claude/skills/`, `design/`, `notes/`, and `.github/`
- [ ] Add placeholder files where needed to make the structure explicit
- [ ] Document which files belong in the kit repo versus the target project
- [ ] Add a short note describing the installation flow at a structural level

## Acceptance criteria
- The repository contains a clear and coherent base directory structure
- The project-local installation model is visible in the folder and file layout
- It is clear which artifacts stay in the kit repo and which are copied into a new target project
- The structure supports later work on docs, templates, and skills without rework

## Notes
Labels: `infra`, `design`
Milestone: `M1 - Foundation + ADRs`

Issue 2 Title:
Write install guide and document v1 scope constraints (ADR-001, ADR-002)

Issue 2 Body:
## Summary
Write the installation documentation for the workflow kit and explicitly document the v1 scope as new-project-only.

## ADR
Related ADRs:
- `design/adr/adr-001-project-local-installation-model.md`
- `design/adr/adr-002-new-project-only-scope.md`

## Goal
Create installation and scope documentation that explains how the kit is used and what it does not support in v1.

## Why it matters
The product boundary is one of the most important parts of the MVP. Users need to understand that this is a project-local toolkit for new projects, not a retrofit tool for existing repositories.

## Tasks
- [ ] Draft `README.md` overview content for the product boundary
- [ ] Draft `docs/install.md`
- [ ] Explain prerequisites such as Git, GitHub CLI, and Claude Code
- [ ] Explain the project-local install model
- [ ] Clearly document that v1 is for new projects only
- [ ] Add a short quick-start flow for first-time users

## Acceptance criteria
- The installation path is clearly documented
- The new-project-only scope is explicit and easy to understand
- A first-time user can tell whether the kit is a fit for their project
- The docs reduce ambiguity about how and where the kit is installed

## Notes
Labels: `docs`, `design`
Milestone: `M1 - Foundation + ADRs`

Issue 3 Title:
Write GitHub setup guide and define repo workflow assets (ADR-004)

Issue 3 Body:
## Summary
Create the GitHub setup guide and define the first GitHub-native workflow assets for the kit.

## ADR
Related ADR: `design/adr/adr-004-github-first-workflow-model.md`

## Goal
Document the GitHub-first operating model and define the initial repo assets needed to support it.

## Why it matters
The kit is explicitly GitHub-first in v1. Users need clear instructions for labels, milestones, branches, issue templates, PR templates, and optional branch protection.

## Tasks
- [ ] Draft `docs/github-setup.md`
- [ ] Define the default label set for new repos
- [ ] Define milestone guidance for early project phases
- [ ] Define branch naming guidance using `main + feature branch`
- [ ] Outline optional branch protection rules
- [ ] Define the required `.github` assets to add in a later issue

## Acceptance criteria
- The GitHub-first workflow is documented in a practical way
- The default label and milestone strategy is defined
- The branch strategy is clear and consistent with the ADRs
- The required `.github` assets are identified and ready for implementation

## Notes
Labels: `docs`, `infra`, `design`
Milestone: `M1 - Foundation + ADRs`

Issue 4 Title:
Create documentation and template scaffold for generated project artifacts (ADR-005)

Issue 4 Body:
## Summary
Create the initial scaffold for documentation and template files that will be generated into target projects.

## ADR
Related ADR: `design/adr/adr-005-documentation-and-template-architecture.md`

## Goal
Define and add the first template set for core workflow artifacts so later skills can generate consistent outputs.

## Why it matters
The workflow kit depends on consistent repo-local artifacts such as ADRs, issue templates, PR templates, `CLAUDE.md`, and AI summaries. These should start from clear templates rather than ad hoc generation.

## Tasks
- [ ] Create `templates/adr-template.md`
- [ ] Create `templates/issue-template.md`
- [ ] Create `templates/pr-template.md`
- [ ] Create `templates/claude-md-template.md`
- [ ] Create `templates/ai-summary-template.md`
- [ ] Create `templates/mvp-template.md`
- [ ] Create `templates/build-out-plan-template.md`
- [ ] Add brief notes on intended use for each template

## Acceptance criteria
- All core templates for the MVP exist in the repo
- The template names and responsibilities are clear
- The templates reflect the repo-local documentation strategy from ADR-005
- Later skill work can consume these templates without redefining structure

## Notes
Labels: `docs`, `feature`
Milestone: `M1 - Foundation + ADRs`
