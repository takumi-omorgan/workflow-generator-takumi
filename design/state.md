# Claude Code Workflow Kit — State

**Last updated:** 2026-07-14
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** #51 — ratify ADR-058 and clear the ratification debt
- **Prompt:** n/a (bookkeeping-only issue)
- **Branch:** `ratify-adr-058`
- **Status:** Oliver **ratified ADR-058** on 2026-07-14; the ratification-debt cap is free, so the `adr-059`..`adr-061` proposals may proceed. Ratification is an **operator attestation** relayed through the Hermes supervision channel — anchored to issue [#51 comment 4964025789](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/51#issuecomment-4964025789), not to any Oliver-authored artifact in this repo. It is recorded in the knowledge layer, not in the ADR: the format carries no ratification field and accepted ADRs are never edited in place. ADR-058's substance is unchanged — `bin/check-skill-budget`, the generated baseline, and the skill migrations remain **decided, not built**.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #50 — ADR-058 — accept the SKILL.md body budget and progressive disclosure (per-skill ratcheting ceiling, not an advisory check)
- #48 — ADR-057 — ratify ADR-057 and clear the ratification debt
- #46 — ADR-057 — accept the public export integrity gate (re-motivated after an audit falsified two of three premises)
- #40 — none — guard: scan only added lines for placeholder tokens (was false-positiving on historical entries)
- #37 — none — apply the Hermes hardened-workflow overlay to the source repo

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

**ADR-058 is accepted and ratified** (accepted in PR #50 / issue #49; ratified
by Oliver on 2026-07-14, issue #51 — an **operator attestation** relayed through
the Hermes supervision channel, not a first-party artifact; see the in-flight
section above for the provenance). The ratification-debt cap is **free**: no
phase of ADRs sits unratified, so `adr-059` (target-project kit lifecycle),
`adr-060` (ship-loop adoption tier) and `adr-061` (runtime asset manifest) may
now be proposed — one PR each, each carrying a review receipt. They are still
untracked local drafts. M6 implementation issues stay shut until they land.

Read the ADR-058 review before writing the next ADR. The draft proposed an
*advisory* budget check with a grace list that would "shrink each release"; the
reviewer killed it as "a hope that future-you will feel differently" — the cure
was a weaker form of the disease. The accepted design pins each over-budget
skill to its own current word count as a CI-blocking ceiling that can only fall.
Durable lesson: **a baseline is only a ratchet if the baseline itself is
ratcheted**, or one PR raises the ceiling and the body together and passes.

Follow-up issues, now fileable: `bin/check-skill-budget` (with the
monotonic-ceiling diff), the generated baseline, the `docs/skills.md` "what goes
where" section, and migrating the five heaviest skills (2,384–2,706 words).

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: none
args: propose ADR-059 (target-project kit lifecycle) — one PR, with a knowledge/reviews receipt; adr-060 and adr-061 follow
preconditions: [ADR-058 ratified, ratification-debt cap free]
blocked-by: none
```

<!-- state:next-action:end -->
