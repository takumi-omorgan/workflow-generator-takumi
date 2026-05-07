## Summary
Implement the first planning skill that helps a user go from a rough project idea to a usable PRD draft.

## ADR
Related ADR: `design/adr/adr-003-prd-intake-model.md`

## Goal
Support the “no PRD yet” path by creating a structured `idea-to-prd` skill.

## Why it matters
Many users will not start with a polished PRD. This skill lowers adoption friction and makes the workflow useful earlier in the product lifecycle.

## Tasks
- [ ] Define the purpose and boundaries of the `idea-to-prd` skill
- [ ] Create `skills/idea-to-prd/SKILL.md`
- [ ] Define required inputs and expected outputs
- [ ] Ensure the output is suitable for later normalization or MVP scoping
- [ ] Add one example input/output pair

## Acceptance criteria
- The repository contains a working first draft of the `idea-to-prd` skill
- The skill is clearly scoped to rough idea capture
- The output is compatible with the later planning workflow
- An example demonstrates expected usage

## Notes
Labels: `feature`, `design`
Milestone: `M2 - Planning Skills`
