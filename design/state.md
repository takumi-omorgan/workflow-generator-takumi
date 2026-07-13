# Claude Code Workflow Kit — State

**Last updated:** 2026-07-13
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #47 — ratify ADR-057 and clear the ratification debt
- **Prompt:** n/a (bookkeeping-only issue)
- **Branch:** `ratify-adr-057`
- **Status:** Oliver **ratified ADR-057** on 2026-07-13; the ratification-debt cap is free, so the `adr-058`..`adr-061` proposals may proceed. Ratification is recorded in the knowledge layer, not in the ADR — the ADR format carries no ratification field and accepted ADRs are never edited in place. ADR-057's substance is unchanged: it rests on the one real, latent gap (nothing verifies after a publish that the remote matches the verified export artifact), and `bin/verify-published` remains **decided, not built** — implementation is a follow-up and risk R1 stays open until it ships.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #46 — ADR-057 — accept the public export integrity gate (re-motivated after an audit falsified two of three premises)
- #40 — none — guard: scan only added lines for placeholder tokens (was false-positiving on historical entries)
- #37 — none — apply the Hermes hardened-workflow overlay to the source repo
- #36 — none — release v5.0.1: prune the internal knowledge layer from the export, bump pins/changelog
- #35 — none — address the public-release review (jq prerequisite, verb-layer docs, github-setup)

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

None. The prior blocker (public repo not created, `gh` auth not yet
`olivermorgan2`) is cleared — the repo exists and both releases shipped.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0 and v5.0.1 are published to `olivermorgan2/claude-workflow-kit`. The
source repo is post-release and now carries the Hermes hardened-workflow
overlay (`CLAUDE.md` plus the `guard` workflow) from PR #37, with the guard's
placeholder scan corrected in PR #40. The next body of work is the M6–M9
backlog.

**ADR-057 is accepted and ratified** (accepted in PR #46 / issue #45; ratified
by Oliver on 2026-07-13) — the first of the backlog's prerequisite ADRs to
clear the gate. Getting it there required rewriting it:
its original premises about the published repo were audited and two of three
were **false**, so it was re-motivated around the single real gap (no
post-publish verification of the remote) and re-reviewed. See
[`knowledge/reviews/2026-07-13-adr-057-review.md`](../knowledge/reviews/2026-07-13-adr-057-review.md);
the durable lesson is to **observe an asserted defect before designing against
it**, which applies directly to the remaining drafts.

The remaining ADR drafts (`adr-058` skill body budget, `adr-059`
target-project kit lifecycle, `adr-060` ship-loop adoption tier, `adr-061`
runtime asset manifest) and the M6–M9 issue backlog still exist **only as
untracked local drafts** — none has been proposed, adversarially reviewed, or
accepted. The overlay requires a phase's prerequisite ADRs to be accepted (each
carrying a `knowledge/reviews/` receipt, which `guard` enforces) before its
implementation issues open, so the next step is to propose those ADRs — not to
open M6 issues.

The ratification-debt cap is **free**: ADR-057 is ratified, so no phase of ADRs
sits unratified and the next one may be proposed. Whichever ADRs land next will
consume the cap again until Oliver ratifies them.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: adr-writer
args: propose adr-058..061 — one PR per ADR, each with a knowledge/reviews/ receipt (adr-057 accepted in PR #46, ratified 2026-07-13)
preconditions: [drafts moved onto a branch, adversarial reviewer available, ratification debt clear]
blocked-by: none
```

<!-- state:next-action:end -->
