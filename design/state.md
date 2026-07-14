# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #53 — propose ADR-061 (declarative runtime-asset manifest)
- **Branch:** `adr-061-manifest`
- **Status:** **ADR-061 accepted under mandate** (Qwen review READY on pass 2; receipt at `knowledge/reviews/2026-07-14-adr-061-review.md`). **Ratification pending Oliver.** First of the three M6–M9 prerequisite ADRs; `adr-059` and `adr-060` follow in the same phase. Decided, not built.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling last five completed issues; oldest drops off. PR number, ADR, summary.

- #52 — ADR-058 — ratify ADR-058 and clear the ratification debt
- #50 — ADR-058 — accept the SKILL.md body budget and progressive disclosure (per-skill ratcheting ceiling, not an advisory check)
- #48 — ADR-057 — ratify ADR-057 and clear the ratification debt
- #46 — ADR-057 — accept the public export integrity gate (re-motivated after an audit falsified two of three premises)
- #40 — none — guard: scan only added lines for placeholder tokens (was false-positiving on historical entries)

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

One **open defect**: ADR-054 is still marked `proposed` even though its helpers
shipped under issue #13 (17 `bin/` files cite it) — implementation merged without
its ADR ever being accepted. Needs its own gate; out of scope for a decision-only PR.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0/v5.0.1 are published to `olivermorgan2/claude-workflow-kit`; the source repo
is post-release under the Hermes hardened-workflow overlay. Current body of work:
the three M6–M9 prerequisite ADRs — **one PR each, each carrying a
`knowledge/reviews/` receipt** (which `guard` enforces).

**Order is load-bearing: ADR-061 → ADR-059 → ADR-060.** 061 first because both
others consume its manifest (059 reads its ownership column, 060 its profiles
column); 059 before 060 because ADR-060's design calls `doctor` from ADR-059, and
no artifact may cite an ADR that is not in-tree.

**ADR-061 is accepted (2026-07-14, issue #53), ratification pending.** Next: propose
**ADR-059** (target-project kit lifecycle), then **ADR-060** (ship-loop adoption
tier). Both are still untracked local drafts.

Read [the ADR-061 receipt](../knowledge/reviews/2026-07-14-adr-061-review.md) before
writing the next ADR — it cost a review pass: **an ADR may not depend on a vocabulary
defined by a downstream draft.** If X sequences before Y because Y consumes X, every
enumerated value X exposes must be closed by X. (Earlier lessons are in
[`knowledge/log.md`](../knowledge/log.md).)

**Ratification debt is AT the cap (one phase: 059/060/061).** No further phase of ADRs
may be accepted, and M6+ implementation issues stay shut, until Oliver ratifies.
ADR-058 follow-ups (`bin/check-skill-budget`, the generated baseline, the
`docs/skills.md` section, migrating the five heaviest skills) are fileable once the
debt clears.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: propose ADR-059 (target-project kit lifecycle) — one PR, with a knowledge/reviews receipt; adr-060 follows
preconditions: [ADR-061 accepted and in-tree]
blocked-by: none
```

<!-- state:next-action:end -->
