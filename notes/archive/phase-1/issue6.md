## Summary
Implement a skill that normalizes either a standard PRD or a custom user format into a stable internal planning structure.

## ADR
Related ADR: `Design/adr/adr-003-prd-intake-model.md`

## Goal
Support multiple PRD intake paths while keeping downstream workflow generation consistent.

## Why it matters
The MVP promises to accept both standard and custom PRD formats. This skill is what makes that promise practical.

## Tasks
- [ ] Define the normalization target structure
- [ ] Create `skills/prd-normalizer/SKILL.md`
- [ ] Describe how standard PRDs are handled
- [ ] Describe how custom PRDs are interpreted and normalized
- [ ] Add example transformations

## Acceptance criteria
- The skill clearly supports both standard and custom PRD inputs
- The normalized output is predictable and reusable
- Example transformations make the behavior easy to understand
- The skill reduces ambiguity for downstream planning steps

## Notes
Labels: `feature`, `design`
Milestone: `M2 - Planning Skills`
