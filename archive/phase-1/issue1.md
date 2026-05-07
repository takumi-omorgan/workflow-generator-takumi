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
