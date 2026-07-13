# ADR-057: Public export integrity gate

**Status:** proposed
**Date:** 2026-07-08

## Context

ADR-056 established the two-repo public distribution model: the source
repo holds internal material (`design/adr/`, `archive/`, `notes/`,
contributor sections of `CLAUDE.md`), and a public export repo holds the
curated distribution. `bin/export-public` and `bin/check-public-export`
implement the export, and `docs/publishing.md` documents it.

An external review of the currently published repo found that the
published artifact does not honour the export contract:

1. **Identity mismatch.** The published repo lives under a different
   owner/name than the one referenced throughout its own README,
   `docs/install.md`, and `bin/bootstrap-workflow-kit`. A visitor cannot
   install the repo they are looking at; the quick start pulls a
   different repo.
2. **Internal exhaust shipped.** `archive/phase-1/` (historical issue
   prompts), `notes/` (dev eval logs), and the contributor-notes section
   of `CLAUDE.md` — all material the export contract says is stripped —
   are present in the published tree.
3. **No enforcement.** Nothing verifies, after publishing, that the
   public repo matches what the export pipeline was supposed to produce.
   The export can drift silently (or the wrong tree can be pushed to the
   public remote) and no check fires.

The kit's whole pitch is discipline; a published artifact that violates
its own distribution ADR is the single most credibility-damaging defect
it can have. We are optimising for: a visitor to the public repo can
trust that (a) the install instructions install *that* repo, and (b) the
tree contains only curated distribution content.

## Options considered

### Option A: Fix the current publish by hand and rely on care

- Pros: no new tooling; fastest path to a clean public repo.
- Cons: the drift already happened once with the tooling in place;
  nothing prevents recurrence; violates the kit's own script-vs-vigilance
  principle (ADR-043, ADR-054).

### Option B: Make the export identity-aware and add a post-publish verification gate

Extend `bin/export-public` to take the target repo identity
(`--public-repo=OWNER/NAME`) and rewrite every self-reference (install
one-liners, `WORKFLOW_KIT_REPO` default, release links) during export.
Add `bin/verify-published` that clones the public remote at its HEAD/tag
and asserts: no excluded paths present, no source-repo identity strings
remain, `CLAUDE.md` contributor section stripped, README directory table
matches the actual top-level tree. Wire the assertion set into
`bin/check-public-export` fixtures and run `verify-published` as the
final step of the `/release` flow for public releases.

- Pros: closes the gap mechanically; reuses the existing fixture/eval
  pattern; makes "the public repo is trustworthy" a checked invariant
  rather than an intention; identity rewrite also unblocks forks.
- Cons: one more script and fixture set to keep green; `/release` gains
  a network-dependent step (mitigated: advisory offline, blocking when
  the remote is reachable).

### Option C: Collapse to a single public repo and strip internal material from source

- Pros: no export step to drift; one identity.
- Cons: loses the internal ADR/notes audit trail from version control or
  forces it into a second private repo anyway; reverses ADR-056 for a
  problem that is enforceable within it.

## Decision

Option B. The export becomes identity-aware, and publishing is not
complete until `bin/verify-published` passes against the public remote.

## Consequences

- The published repo becomes self-consistent: its install path installs
  itself, and forks get correct references via `--public-repo`.
- `/release` (public shape) gains a verification step; a failed
  verification blocks announcing the release.
- The README directory table becomes a checked artifact (it must match
  the exported tree), fixing the undocumented-directories problem as a
  side effect.
- Hand-pushing to the public remote outside the export pipeline is now
  detectable and treated as an incident.
- Deferred: signing/checksumming the bootstrap release asset — tracked
  as a separate issue under ADR-055's versioning policy, not this ADR.
