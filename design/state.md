# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** none. #53 (ADR-061) merged as PR #54.
- **Status:** **ADR-061 accepted under mandate**, ratification pending Oliver. **ADR-059 and ADR-060 are HALTED** — ADR-059's premise was verified false and the fix reaches its Decision, so it was stopped before review rather than patched (blocker 1). Both remain untracked drafts.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling last five completed issues; oldest drops off. PR number, ADR, summary.

- #54 — ADR-061 — accept the declarative runtime-asset manifest (installer's inline 12→13-entry list becomes a manifest; missing *required* asset becomes fail-fast)
- #52 — ADR-058 — ratify ADR-058 and clear the ratification debt
- #50 — ADR-058 — accept the SKILL.md body budget and progressive disclosure (per-skill ratcheting ceiling, not an advisory check)
- #48 — ADR-057 — ratify ADR-057 and clear the ratification debt
- #46 — ADR-057 — accept the public export integrity gate (re-motivated after an audit falsified two of three premises)

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

**1. ADR-059 HALTED — needs Oliver's ruling (issue #55).** Its Decision ("the receipt
layer becomes the source of truth for what the kit owns") rests on a false premise: the
installer writes **no** receipt, receipts are **gitignored** (a fresh clone has none),
and the ADR-050 schema is **work-unit-keyed with no path/version/hash** — so
"unmodified since install" is unanswerable. It needs a **committed install manifest** —
a different artifact — and making receipts committed would contradict **accepted**
ADR-050. **ADR-060 is halted with it** (its Option C calls `doctor`, an ADR-059
surface). Analysis + option space:
[halt note](../knowledge/reviews/2026-07-14-adr-059-halt.md).

**2. Ratification debt is AT the cap** (one phase: ADR-061). No further phase of ADRs
may be accepted, and M6+ implementation issues stay shut, until Oliver ratifies.

**3. Open defect:** ADR-054 is still `proposed` though its helpers shipped under issue
#13 (17 `bin/` files cite it) — implementation merged without its ADR ever being
accepted. Needs its own gate.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0/v5.0.1 are published to `olivermorgan2/claude-workflow-kit`; the source repo is
post-release under the Hermes hardened-workflow overlay.

**ADR-061 is accepted (issue #53 / PR #54), ratification pending** — the one piece of
the M6–M9 prerequisite trio that landed. Decided, not built.

**Do NOT simply "propose ADR-059" next — it is halted, not pending.** Read the
[halt note](../knowledge/reviews/2026-07-14-adr-059-halt.md) first: it lays out three
options and deliberately **chooses none**. That is Oliver's call, tracked in #55.

Two review lessons, each of which cost a pass:
[ADR-061](../knowledge/reviews/2026-07-14-adr-061-review.md) — **an ADR may not depend
on a vocabulary defined by a downstream draft.**
[ADR-059](../knowledge/reviews/2026-07-14-adr-059-halt.md) — **"the X layer already
does Y" is a premise, not a citation**; open X and find Y.

ADR-058 follow-ups (`bin/check-skill-budget`, the generated baseline, the
`docs/skills.md` section, migrating the five heaviest skills) are fileable once the
ratification debt clears.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: Oliver ratifies ADR-061, and rules on the ADR-059 redraft (issue #55) — receipt-layer premise falsified; needs a committed install manifest
preconditions: []
blocked-by: awaiting-oliver
```

<!-- state:next-action:end -->
