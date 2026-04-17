
# ADR-020: End-to-end workflow guide doc

**Status:** proposed
**Date:** 2026-04-17

## Context

Users can see individual pieces — skills, templates, ADRs — but no single document walks the full flow from idea to shipped release. `docs/install.md` references a planned `docs/workflow-guide.md`, and `generic-project-workflow.md` (~29 KB) contains detailed source material but is too long and kit-internal to serve as user-facing guidance. Users also need clarity on when work does *not* require an ADR (bug fixes, chores, dependency bumps).

## Options considered

### Option A: One time-boxed guide covering the happy path

- Pros: single reference, easy to maintain, answers the most common question ("what do I do next?").
- Cons: may not cover every edge case.

### Option B: Multi-doc split per phase

- Pros: each phase is self-contained.
- Cons: fragmented, harder to follow the narrative, more files to maintain.

### Option C: Leave at skill-level SKILL.md files

- Pros: no new file.
- Cons: no connected narrative, users must piece together the flow themselves.

## Decision

Write a single `docs/workflow-guide.md` covering one full pass of: idea → PRD → MVP spec → ADRs → issues → branches → PRs → merge → release. Distilled from `generic-project-workflow.md` into a concise, user-facing format. Includes an explicit "when you don't need an ADR" section covering bug fixes, chores, and dependency bumps as ADR-free work.

## Consequences

- Users get a single walkthrough of the entire kit workflow.
- The broken reference in `docs/install.md` is resolved.
- The "when you don't need an ADR" section reduces ceremony for routine work.
- This is the capstone doc — it references all prior ADRs and ties the kit together.
