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
