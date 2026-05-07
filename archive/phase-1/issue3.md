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
