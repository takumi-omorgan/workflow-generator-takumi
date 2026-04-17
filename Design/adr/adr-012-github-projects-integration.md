
# ADR-012: Integrate GitHub Projects for visual workflow tracking

**Status:** proposed
**Date:** 2026-04-17

## Context

The kit currently uses milestones, labels, and issues to organize work (ADR-004), but provides no visual status view. Users see a flat issue list in the GitHub Issues tab, which makes it hard to track what is in progress, in review, or done. GitHub Projects offers board and table views with customizable status columns, giving teams a lightweight kanban without leaving GitHub.

## Options considered

### Option A: Bake into the issue-planner skill

- Pros: one-step setup, board is always in sync with created issues, no extra command to remember.
- Cons: couples board creation to issue creation, harder to re-run independently.

### Option B: Standalone /setup-project skill

- Pros: separation of concerns, user can choose when to create the board.
- Cons: extra manual step, board may fall out of sync if issues are created first.

### Option C: Document-only

- Pros: zero code, flexible.
- Cons: manual, error-prone, defeats the purpose of automation.

## Decision

Bake GitHub Projects integration into the **issue-planner skill** (ADR-011). When issues are created, the skill also creates a GitHub Project board via `gh` and adds every new issue to it. Default columns: **Todo**, **In Progress**, **Review**, **Done**. The board name follows the pattern `<repo> — <milestone>`.

## Consequences

- Users get a visual status board immediately after issue planning, with no extra step.
- The issue-planner skill gains a dependency on `gh project` commands, which require the `project` OAuth scope.
- Teams that prefer their own board layout can delete or rename columns after creation.
- Aligns with the GitHub-first model (ADR-004) by using native GitHub features rather than external tools.
