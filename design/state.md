# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #58 — ratify ADR-061 and clear the ratification debt (bookkeeping only)
- **Status:** Oliver **ratified ADR-061** on 2026-07-14 (accepted under mandate in PR #54 / issue #53); the ratification-debt cap is **free**. Ratification is an **operator attestation** relayed through the Hermes supervision channel — anchored to issue [#58 comment 4966870880](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/58#issuecomment-4966870880), not to any Oliver-authored artifact in this repo. Recorded in state/knowledge, not in the ADR: the format has no ratification field and accepted ADRs are never edited in place. ADR-061's substance is unchanged — the manifest and `bin/list-runtime-assets` stay **decided, not built**. **ADR-059 and ADR-060 remain HALTED** (blocker 1); ratifying ADR-061 does **not** unhalt them.

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

**1. ADR-059 HALTED — needs Oliver's ruling (issue #55).** Its Decision ("the receipt
layer becomes the source of truth for what the kit owns") rests on a false premise: the
installer writes **no** receipt, receipts are **gitignored** (a fresh clone has none),
and the ADR-050 schema is **work-unit-keyed with no path/version/hash** — so
"unmodified since install" is unanswerable. It needs a **committed install manifest** —
a different artifact — and making receipts committed would contradict **accepted**
ADR-050. **ADR-060 is halted with it** (its Option C calls `doctor`, an ADR-059
surface). Analysis + option space: [halt note](../knowledge/reviews/2026-07-14-adr-059-halt.md).

**2. Open defect:** ADR-054 is still `proposed` though its helpers shipped under issue
#13 (17 `bin/` files cite it) — implementation merged without its ADR ever being
accepted. Needs its own gate.

**Not a blocker any more:** the ratification-debt cap. ADR-061 was its sole occupant
and is now ratified, so **no phase of ADRs is awaiting ratification**.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0/v5.0.1 are published to `olivermorgan2/claude-workflow-kit`; the source repo is
post-release under the Hermes hardened-workflow overlay.

**ADR-061 is accepted and ratified** (accepted in PR #54 / issue #53; ratified by
Oliver 2026-07-14, issue #58 — an **operator attestation** relayed through the Hermes
supervision channel, not a first-party artifact; see the in-flight section above for
the provenance). The debt cap is **free**. Still decided, not built — so ADR-061's
implementation issues, and the ADR-058 follow-ups (`bin/check-skill-budget`, the
generated baseline, the `docs/skills.md` section, migrating the five heaviest skills),
are now **fileable**.

**Do NOT simply "propose ADR-059" next — it is halted, not pending, and ratifying
ADR-061 did not unhalt it.** The cap was never what blocked it: its Decision rests on
a falsified premise and needs a *committed install manifest*, a different artifact.
Read the [halt note](../knowledge/reviews/2026-07-14-adr-059-halt.md) first: it lays
out three options and deliberately **chooses none**. That is Oliver's call, in #55.

Two review lessons, each of which cost a pass:
[ADR-061](../knowledge/reviews/2026-07-14-adr-061-review.md) — **an ADR may not depend
on a vocabulary defined by a downstream draft.**
[ADR-059](../knowledge/reviews/2026-07-14-adr-059-halt.md) — **"the X layer already
does Y" is a premise, not a citation**; open X and find Y.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: "Oliver rules on the ADR-059 redraft (issue #55) — receipt-layer premise falsified; needs a committed install manifest. ADR-059/060 stay halted until then. Meanwhile ADR-061 implementation issues and the ADR-058 follow-ups are fileable."
preconditions: ["ADR-061 ratified (operator attestation, issue #58)", "ratification-debt cap free"]
blocked-by: "awaiting-oliver (ADR-059 only; nothing else)"
```

<!-- state:next-action:end -->
