# ADR-036: Granularity / density control for phased plans

**Status:** accepted
**Date:** 2026-04-30

## Context

ADR-032 introduces phased plans but leaves phase count to author
judgment. Without an explicit knob, decomposition varies
project-to-project, making example projects and the workflow guide
harder to write consistently. Authors faced with a blank
`build-out-plan.md` template have no anchor for "how many phases is
the right number for a project this size."

GSD's `granularity` setting (`coarse` 3-5 phases, `standard` 5-8,
`fine` 8-12) suggests a small modifier that gives users a sane
default and keeps examples comparable across projects. This is a
follow-up to ADR-032, not a blocker for it.

## Options considered

### Option A: Three-tier `--granularity={coarse|standard|fine}` flag on `prd-to-mvp` / `/planning`

- Pros: matches GSD's well-tested taxonomy; easy to teach; bands
  give the planning skill a target without forcing exact counts.
- Cons: one more flag to document; bands are heuristic, not
  prescriptive.

### Option B: Free-form `--phases=N`

- Pros: exact control.
- Cons: harder to recommend defaults; users without intuition for
  the right number get no guidance.

### Option C: Auto-pick from project size estimate

- Pros: clever — no flag needed.
- Cons: unreliable on the first pass (PRDs vary too much); risks
  surprising users with unwanted phase counts.

### Option D: No knob — let users shape phases manually

- Pros: simplest.
- Cons: example projects and the workflow guide lose a
  prescriptive default; first-time authors get no anchor.

## Decision

Adopt **Option A**. Both `prd-to-mvp` and `/planning` (ADR-031)
accept `--granularity={coarse|standard|fine}`, default `standard`
(5-8 phases). The choice is recorded in `build-out-plan.md`'s
metadata so re-runs and downstream skills are consistent. `coarse`
fits small projects (1-3 phases), `standard` typical multi-month
builds, `fine` large scope where each phase warrants its own
milestone. Phase count is a target band, not a hard cap — the
planning skill chooses the actual count within the band and
justifies the choice inline so the user can adjust.

## Consequences

- Easier: example projects and the workflow guide can prescribe
  defaults; first-time authors get sane starting points without
  designing the phase shape themselves.
- Harder: one more option to document; risk of users tuning
  granularity instead of fixing real scope issues (mitigation:
  workflow guide's "right phase count" section explicitly addresses
  this anti-pattern).
- Maintain: minimal — a parameter passed through skills, recorded
  once in `build-out-plan.md` metadata.
- Deferred: domain-specific defaults for software vs research vs
  content (per ADR-028's workflow-agnostic framing). Same default
  for all in v1; revisit if usage data warrants a per-domain split.
