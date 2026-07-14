# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #60 — ADR-059 redraft: accept the target-project kit lifecycle on a committed install ledger
- **Status:** **ADR-059 accepted under mandate; ratification pending.** Oliver ruled **Option A** on #55 — an **operator attestation** relayed through the Hermes supervision channel, anchored to [#55 comment 4967121740](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/55#issuecomment-4967121740), not to any Oliver-authored artifact in this repo. The Decision: the installer writes a committed, file-keyed, hashed `.claude/kit-lock.json` ledger; `upgrade`/`doctor`/`uninstall` are built on **manifest (ADR-061) + ledger (ADR-059)**. **ADR-050 is not superseded** — the redraft stops *depending* on receipts. Adversarial review READY on pass 3 of 3 (`qwen/qwen3.7-plus`). **Decided, not built**, and blocked on ADR-061's tooling.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling last five completed issues; oldest drops off. PR number, ADR, summary.

- #56 — none — record the ADR-059 HALT and the ADR-061 ratification request (docs only; #55 left open for Oliver's ruling)
- #54 — ADR-061 — accept the declarative runtime-asset manifest (installer's inline 12→13-entry list becomes a manifest; missing *required* asset becomes fail-fast)
- #52 — ADR-058 — ratify ADR-058 and clear the ratification debt
- #50 — ADR-058 — accept the SKILL.md body budget and progressive disclosure (per-skill ratcheting ceiling, not an advisory check)
- #48 — ADR-057 — ratify ADR-057 and clear the ratification debt

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

**1. ADR-059 ratification debt.** Accepted **under mandate**, awaiting Oliver's async
ratification. The overlay allows **one** such phase at a time: until he ratifies, **no further
phase of ADRs may be accepted** and ADR-059's implementation issues may not be filed. ADR-061
implementation and the ADR-058 follow-ups are **not** blocked by this.

**2. ADR-060 HALTED.** Untracked draft, downstream of ADR-059 (its Option C calls `doctor`).
Accepting ADR-059 does **not** unhalt it: it needs its own redraft — adding the ADR-061
citation its text lacks — and may not be proposed while blocker 1 stands.

**3. Open defect:** ADR-054 is still `proposed` though its helpers shipped under issue #13
(17 `bin/` files cite it) — merged without its ADR ever being accepted. Needs its own gate.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0/v5.0.1 are published to `olivermorgan2/claude-workflow-kit`; the source repo is
post-release under the Hermes hardened-workflow overlay.

**ADR-059 (accepted, unratified) and ADR-061 (accepted, ratified) are both decided, not
built.** Neither `runtime-assets.md` nor `bin/list-runtime-assets` exists; there is no
`doctor`/`upgrade`/`uninstall` code anywhere.

**Fileable now** (not blocked by the ratification debt): **ADR-061's implementation issues** —
its manifest and parser are the prerequisite for *every* ADR-059 deliverable, so this is the
natural next build — plus the ADR-058 follow-ups (`bin/check-skill-budget`, the generated
baseline, the `docs/skills.md` section, migrating the five heaviest skills).
**Blocked until Oliver ratifies ADR-059:** ADR-060's redraft, and ADR-059's implementation.

Three review lessons, each of which cost a pass:
[ADR-061](../knowledge/reviews/2026-07-14-adr-061-review.md) — **an ADR may not depend on a vocabulary defined by a downstream draft.**
[ADR-059 halt](../knowledge/reviews/2026-07-14-adr-059-halt.md) — **"the X layer already does Y" is a premise, not a citation**; open X and find Y.
[ADR-059 redraft](../knowledge/reviews/2026-07-14-adr-059-redraft-review.md) — **a field asked to mean two things will authorise the wrong one**; and **one agreeable review pass is not a gate**.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: "File ADR-061 implementation issues (runtime-assets.md + bin/list-runtime-assets) — the prerequisite for every ADR-059 deliverable. ADR-058 follow-ups are also fileable. Oliver must ratify ADR-059 before ADR-060's redraft or ADR-059's implementation issues."
preconditions: ["ADR-059 accepted under mandate (ratification pending)", "ADR-061 accepted and ratified"]
blocked-by: "awaiting-oliver (ADR-059 ratification — blocks ADR-060 redraft and ADR-059 implementation only)"
```

<!-- state:next-action:end -->
