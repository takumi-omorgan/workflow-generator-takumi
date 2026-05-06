## Summary
Write the installation documentation for the workflow kit and explicitly document the v1 scope as new-project-only.

## ADR
Related ADRs:
- `Design/adr/adr-001-project-local-installation-model.md`
- `Design/adr/adr-002-new-project-only-scope.md`

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
