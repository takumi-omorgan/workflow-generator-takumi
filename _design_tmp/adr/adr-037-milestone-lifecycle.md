# ADR-037: Milestone lifecycle commands (audit, summary, complete)

**Status:** accepted
**Date:** 2026-04-30

## Context

ADR-032 introduces phases as the executable unit between MVP scope
and a release. Phases group naturally into milestones — the
multi-phase delivery unit between phase and release. The kit's
closest analogue today is `/release` (ADR-017), but `/release`
covers tag-and-publish, not "did we actually finish what this
milestone promised?" There is no skill that audits a milestone for
completeness, summarises what shipped, or formally closes it out.

Inspired by the GSD `audit-milestone`, `milestone-summary`, and
`complete-milestone` commands, milestone lifecycle ops formalise the
boundary between phases and releases. They are only meaningful once
ADR-032's phase structure exists, so this ADR explicitly defers
implementation until ADR-032 has shipped and at least one project
has run a real milestone end-to-end.

## Options considered

### Option A: Three discrete skills — `/audit-milestone`, `/milestone-summary`, `/complete-milestone`

- Pros: composable; each is small and single-purpose; users can
  run audit standalone without committing to closing the milestone.
- Cons: three commands to learn; users may forget the order.

### Option B: Single `/finish-milestone` skill that does all three in sequence

- Pros: one command.
- Cons: less composable; cannot run audit standalone; harder to
  partially re-run if one step needs fixing.

### Option C: Fold into `/release`

- Pros: simplest call site.
- Cons: conflates "milestone done" with "release tagged" — they
  may differ (multiple milestones per release, or a milestone
  closed without an immediate release).

### Option D: Manual checklist in the workflow guide

- Pros: zero implementation cost.
- Cons: abandons the kit's automation principle; unverifiable;
  drifts from reality.

## Decision

Adopt **Option A**. Three composable skills layered on ADR-032,
implemented after ADR-032 has shipped:

- `/audit-milestone`: verifies all phases in the milestone are
  complete, all issues closed, and all referenced ADRs have linked
  PRs. Returns pass/fail with a gap list. Warns on failure but
  does not block `/complete-milestone` — the user decides.
- `/milestone-summary`: generates `Design/milestones/N-summary.md`
  capturing what shipped, ADRs adopted, lessons learned, and
  deferred work. Sourced from `git log`, the GitHub milestone, and
  accepted ADRs in the milestone's phase range.
- `/complete-milestone`: closes the GitHub milestone, archives
  milestone-scoped state in `Design/state.md` (per ADR-035), and
  optionally invokes `/release` (ADR-017) when the milestone maps
  to a release boundary.

Default: one milestone == one release, but the two are decoupled —
`/complete-milestone` and `/release` can run independently when a
project chooses to bundle milestones into a release.

## Consequences

- Easier: large projects get visible delivery checkpoints;
  retrospectives become routine artefacts, not a manual exercise;
  release notes have richer source material when `/release` runs.
- Harder: three more skills to maintain; only valuable when ADR-032
  (phases) is real and exercised; coordination between
  `/complete-milestone` and `/release` needs documenting.
- Maintain: tightly coupled to ADR-032's phase shape and ADR-035's
  `state.md` format; format spec for `Design/milestones/N-summary.md`
  lives at `templates/milestone-summary-template.md`.
- Deferred: implementation waits on ADR-032 shipping. Cross-milestone
  reporting (e.g. multiple milestones aggregated into one release
  note) is out of scope; `/release` already groups commits by tag
  range and is sufficient.
