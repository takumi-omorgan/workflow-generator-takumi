# ADR-035: `Design/state.md` and session-continuity artefacts

**Status:** accepted
**Date:** 2026-04-30

## Context

Today the kit relies entirely on git state, GitHub issue status, and
the prompt files in `prompts/` to convey "where are we?" That is
enough for a fresh session on a single issue, but for projects
spanning many issues and phases, every new session reconstructs
context from scratch. There is no cross-session memory beyond what
is in git, and no clean handoff for context-window-exhausting
sessions.

Inspired by GSD's `STATE.md`, `HANDOFF.json`, and `continue-here.md`
artefacts, the kit needs a small persistent pointer to current
position. ADR-031's planning layer and ADR-032's phases give state
something meaningful to track; ADR-038's executor changes are the
natural place to update it.

## Options considered

### Option A: Single `Design/state.md` updated by existing skills, plus `/resume` and optional `/pause` skills

- Pros: lightweight; reuses skills already in the chain
  (`prepare-issue`, `claude-issue-executor`, `pr-review-packager`);
  one canonical place to look; cross-skill traceability.
- Cons: drift if updates aren't enforced; merge conflicts in a
  single committed file when parallel branches both touch it.

### Option B: Standalone `/resume` and `/pause` with no shared state file

- Pros: simpler — no shared artefact to maintain.
- Cons: loses cross-skill traceability; each invocation
  reconstructs state from git/`gh` (slower, less precise).

### Option C: Per-issue state in `prompts/issue-NNN-state.md`

- Pros: granular; co-located with the prompt.
- Cons: fragmented — no single view of "the project's overall
  position"; harder to brief a fresh session.

### Option D: Do nothing — rely on git + issue board

- Pros: zero work.
- Cons: leaves the gap; long-running projects keep paying the
  context-reconstruction tax.

## Decision

Adopt **Option A**. Ship `Design/state.md` as a lightweight
committed artefact tracking: current phase (per ADR-032 if shipped,
else single implicit phase); in-flight issue number; recently
completed work (last 5 commits or merged PRs); known blockers; and
a "continue here" pointer to the next prompt or action. Updated by
`prepare-issue` (sets in-flight issue), `claude-issue-executor`
(marks progress, per ADR-038), and `pr-review-packager` (closes out
an issue). New `/resume` skill reads `state.md` and briefs the next
session in one short message. New `/pause` skill writes a richer
handoff for context-window-exhausting sessions, including a
markdown brief and an optional dated `notes/handoff-YYYY-MM-DD.md`.
`state.md` is committed (audit trail) rather than gitignored, and
stays under ~100 lines to avoid becoming a stale mirror of GitHub.
Conflict-resolution rule: on merge conflict, the most recently
merged PR's state wins; `/resume` re-derives from `gh` if the file
is suspect.

## Consequences

- Easier: fresh sessions catch up in seconds, not minutes; project
  status visible at a glance without `gh` calls; pause/resume
  across context resets has a clean home; ADR-038's executor has
  somewhere to write progress.
- Harder: drift if updates aren't enforced; merge conflicts in a
  single committed file with parallel branches; risk of the file
  becoming a stale mirror of GitHub if it grows past its scope.
- Maintain: format spec in `templates/state-template.md` is the
  source of truth; skills updating it must be idempotent;
  documented conflict-resolution rule; CI sanity check that the
  file stays under the line cap.
- Deferred: per-developer scratchpad mode and rich graph
  visualization are explicitly out of scope. State stays minimal
  and committed.
