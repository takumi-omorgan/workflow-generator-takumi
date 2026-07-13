# Claude Code Workflow Kit — State

**Last updated:** 2026-07-13
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** none — v5.0.1 is shipped and the public repo is live
- **Prompt:** n/a
- **Branch:** main
- **Status:** public repo `olivermorgan2/claude-workflow-kit` exists (created 2026-06-12, public). Releases `v5.0.0` (tag `a38a142`, 2026-06-12) and `v5.0.1` (tag `1c0eba3`, 2026-06-29, latest) are published. Source `kit.json` kitVersion is `5.0.1`. The identity-gated publish that blocked the release is done.

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #40 — none — guard: scan only added lines for placeholder tokens (was false-positiving on historical entries)
- #37 — none — apply the Hermes hardened-workflow overlay to the source repo
- #36 — none — release v5.0.1: prune the internal knowledge layer from the export, bump pins/changelog
- #35 — none — address the public-release review (jq prerequisite, verb-layer docs, github-setup)
- #34 — none — initialize the workflow-kit knowledge layer

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
backlog. Its ADR drafts (`adr-057` public-export integrity gate, `adr-058`
skill body budget, `adr-059` target-project kit lifecycle, `adr-060` ship-loop
adoption tier, `adr-061` runtime asset manifest) and the M6–M9 issue backlog
exist **only as untracked local drafts** — none has been proposed,
adversarially reviewed, or accepted. The overlay requires a phase's
prerequisite ADRs to be accepted (each carrying a `knowledge/reviews/` receipt,
which `guard` enforces) before its implementation issues open, so the next step
is to propose those ADRs — not to open M6 issues.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: adr-writer
args: propose adr-057..061 — one PR per ADR, each with a knowledge/reviews/ receipt
preconditions: [drafts moved onto a branch, adversarial reviewer available]
blocked-by: none
```

<!-- state:next-action:end -->
