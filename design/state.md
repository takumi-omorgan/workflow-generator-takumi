# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #49 — ADR-058: adopt the SKILL.md body budget and progressive disclosure
- **Prompt:** n/a (decision-only ADR acceptance)
- **Branch:** `accept-adr-058-skill-body-budget`
- **Status:** ADR-058 **accepted under mandate**, awaiting Oliver's async ratification. Decision-only: `bin/check-skill-budget`, the baseline file, and the skill migrations are **decided, not built**. Adversarial review reached READY (4/5, zero blockers) on the second pass — see [`knowledge/reviews/2026-07-14-adr-058-review.md`](../knowledge/reviews/2026-07-14-adr-058-review.md).

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #48 — ADR-057 — ratify ADR-057 and clear the ratification debt
- #46 — ADR-057 — accept the public export integrity gate (re-motivated after an audit falsified two of three premises)
- #40 — none — guard: scan only added lines for placeholder tokens (was false-positiving on historical entries)
- #37 — none — apply the Hermes hardened-workflow overlay to the source repo
- #36 — none — release v5.0.1: prune the internal knowledge layer from the export, bump pins/changelog

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

None blocking the open PR. One **open defect**: ADR-054 is still marked
`proposed` even though its helpers shipped under issue #13 (17 `bin/` files
cite it). Implementation merged without its ADR ever being accepted. Needs its
own gate; out of scope for a decision-only PR.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0/v5.0.1 are published to `olivermorgan2/claude-workflow-kit`. The source
repo is post-release under the Hermes hardened-workflow overlay. The current
body of work is proposing the M6–M9 prerequisite ADRs, one PR each, each with a
`knowledge/reviews/` receipt (which `guard` enforces).

**ADR-058 is accepted** (issue #49) and **consumes the ratification-debt cap**.
Per the overlay, at most one phase of ADRs may sit "accepted under mandate,
awaiting ratification" — so `adr-059` (target-project kit lifecycle), `adr-060`
(ship-loop adoption tier) and `adr-061` (runtime asset manifest) **must wait for
Oliver to ratify ADR-058** before they are proposed, and no M6 implementation
issues may be filed until then. Those three remain untracked local drafts.

Read the ADR-058 review before writing the next ADR. The draft proposed an
*advisory* budget check with a grace list that would "shrink each release"; the
reviewer killed it as "a hope that future-you will feel differently" — the cure
was a weaker form of the disease. The accepted design pins each over-budget
skill to its own current word count as a CI-blocking ceiling that can only fall.
Durable lesson: **a baseline is only a ratchet if the baseline itself is
ratcheted**, or one PR raises the ceiling and the body together and passes.

Follow-up issues to file once the cap frees: `bin/check-skill-budget` (with the
monotonic-ceiling diff), the generated baseline, the `docs/skills.md` "what goes
where" section, and migrating the five heaviest skills (2,384–2,706 words).

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: await Oliver's ratification of ADR-058 (accepted under mandate, PR for issue #49) — the debt cap is consumed until then
preconditions: [ADR-058 PR merged]
blocked-by: ratification-debt cap (adr-059..061 may not be proposed until ADR-058 is ratified)
```

<!-- state:next-action:end -->
