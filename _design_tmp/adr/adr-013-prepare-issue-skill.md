
# ADR-013: /prepare-issue skill for auto-filling issue prompts

**Status:** accepted
**Date:** 2026-04-17

## Context

Before starting a Claude Code implementation session, the user must fill an issue prompt template by copying context from the GitHub issue body, linked ADRs, and the build-out plan. This is the biggest point of friction between "issue exists" and "Claude Code session is briefed." The process is repetitive, error-prone, and discourages the disciplined execution model described in ADR-006.

## Options considered

### Option A: Skill writes file and prints path (user starts session separately)

- Pros: clear separation between preparation and execution, user reviews the prompt before use.
- Cons: two-step process.

### Option B: Skill writes file and immediately starts execution

- Pros: one step from issue to implementation.
- Cons: removes the review checkpoint, risks executing with a bad prompt.

### Option C: Script outside Claude Code

- Pros: no skill authoring needed.
- Cons: loses access to Claude Code's context-reading and summarization capabilities.

## Decision

Create a **/prepare-issue** skill that takes a GitHub issue number, pulls the issue body and linked ADR references via `gh`, reads the relevant sections of the build-out plan, and auto-fills the prompt template. The result is written to `prompts/issue-NNN-short-title.md` (ADR-008). The user starts the implementation session separately, preserving the review checkpoint.

## Consequences

- Eliminates manual copy-paste when preparing issue prompts.
- The prompts/ folder (ADR-008) becomes the canonical handoff point between planning and execution.
- The skill must handle missing or incomplete issue metadata gracefully.
- Pairs naturally with ADR-014 (claude-issue-executor), which consumes the prepared prompt.
