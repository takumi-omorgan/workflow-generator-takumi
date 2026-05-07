# ADR-003: Distribution channels — RSS plus platform submission

**Status:** accepted
**Date:** 2026-04-30
**Phase:** 3

## Context

Phase 3 distributes the writer's feed. The choice is between owning
the feed end-to-end (RSS hosted on the writer's domain) and delegating
to a podcast host (Anchor, Buzzsprout, Transistor) that handles RSS
plus platform submission. The decision shapes ongoing operating cost
and the writer's control over their content.

## Options considered

### Option A: Self-hosted RSS feed plus manual platform submission

- Pros: full ownership of the feed URL; no vendor; one-time submission
  per platform; minimal recurring cost beyond domain + storage.
- Cons: writer is on the hook for uptime, feed validity, and
  platform-specific quirks (Apple's iTunes namespace, Spotify's
  optional fields).

### Option B: Delegate to a podcast host (Anchor / Buzzsprout / Transistor)

- Pros: zero feed-validity work; built-in submission to all major
  platforms; analytics included.
- Cons: per-month cost; vendor lock-in; feed URL is theirs by default
  (some hosts allow custom domains on paid tiers).

## Decision

Adopt **Option A**. The writer values ownership of the feed URL; the
operating cost is small (S3 for assets, a free domain redirect for
the feed URL), and the v1.0.0 cut is for one writer with a
handful of episodes — not enough scale to justify a host. Document
the platform-submission process in
`docs/distribution-checklist.md` so onboarding is repeatable.

## Consequences

- Easier: writer owns their feed and listener relationship; no
  recurring per-month cost beyond storage.
- Harder: writer is responsible for feed validity, submission, and
  any future migration; manual submission to each platform.
- Maintain: `docs/distribution-checklist.md`; periodic `pipeline
  validate-feed` runs to catch drift.
- Deferred: paid host migration if listener volume outgrows the
  self-hosted setup. Document the migration path in v1.1.
