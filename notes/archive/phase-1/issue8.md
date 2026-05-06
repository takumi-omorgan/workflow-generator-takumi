## Summary
Create the issue execution workflow assets that support plan-first Claude Code implementation sessions.

## ADR
Related ADR: `Design/adr/adr-006-claude-code-execution-model.md`

## Goal
Add the prompt and documentation assets required for issue-by-issue implementation with Claude Code.

## Why it matters
The execution model is one of the strongest differentiators of the workflow kit. It needs explicit prompt structure and usage guidance.

## Tasks
- [ ] Add `notes/issue-prompt.md`
- [ ] Adapt the generic issue prompt framework for this repository
- [ ] Document how to fill the prompt before each work session
- [ ] Document the required evaluation summary at the end of a session
- [ ] Add one sample filled issue prompt

## Acceptance criteria
- The repo contains a reusable issue prompt for Claude Code sessions
- The prompt reflects the plan-first, test-alongside-code workflow
- Documentation explains when and how to use it
- A sample filled prompt makes the pattern easy to apply

## Notes
Labels: `feature`, `design`, `docs`
Milestone: `M3 - Execution Workflow`
