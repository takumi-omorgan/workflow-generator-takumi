# ADR-032: Implementation phases in PRD review and planning

**Status:** accepted
**Date:** 2026-04-30

## Context

Today the kit treats MVP scope as a single cut: every requirement is
either `In scope` or `Out of scope` (per ADR-024), and
`build-out-plan.md` is a flat list of work. For large projects this
is too coarse — useful work falls into multiple ordered phases
(foundation → core feature → polish → scale), each potentially with
its own ADRs and acceptance criteria. There is no first-class place
to express "this is in scope, but it's phase 2," and `issue-planner`
has nothing to key milestones off beyond the flat plan.

ADR-031 introduces a deeper planning layer. Phases are a natural
output of that layer, so the artefact shape needs deciding here so
ADR-036 (granularity), ADR-037 (milestone lifecycle), and any skill
that reads phase context can rely on a stable contract. Without
phase structure, ADR-037's milestone commands have nothing to group
phases into and ADR-036's granularity knob has nothing to dial.

## Options considered

### Option A: Phases as `## Phase N: <name>` sections in `build-out-plan.md`

- Pros: extends the existing artefact users already know; least
  disruption to the kit's surface; one source of truth for "the
  ordered plan."
- Cons: `build-out-plan.md` grows in scope; existing skills that
  read it need parsers extended; flat-plan projects need explicit
  single-phase fallback handling.

### Option B: Separate `Design/phases.md` as a first-class doc

- Pros: cleaner separation between "what's in MVP" and "how it's
  phased."
- Cons: another file to scaffold and keep in sync; users have to
  learn yet another artefact; risks duplicating content with the
  build-out plan.

### Option C: Phases as metadata only on ADRs and issues, no narrative artefact

- Pros: lightest; just a tag.
- Cons: loses the "what each phase is for" narrative; new users
  cannot read the plan and understand the phasing.

## Decision

Adopt **Option A**. Extend `templates/build-out-plan-template.md`
with `## Phase N: <name>` sections, each containing: goal, scope
bullets, ADR dependencies, and an exit criterion. `prd-to-mvp` (or
`/planning` from ADR-031) emits the phased plan. `adr-writer` lets
ADRs declare a phase tag in front-matter so the index and traceability
chain pick it up. `issue-planner` reads phases and creates one
GitHub milestone per phase, assigning issues accordingly.
`workflow-docs` surfaces phases in the generated README's roadmap
section. `/release` (ADR-017) treats one phase as the default
release unit. Single-phase projects keep working unchanged: a plan
with no `## Phase` headings is treated as one implicit phase.

## Consequences

- Easier: large projects get an honest delivery plan with explicit
  gates; ADRs and issues inherit phase context for traceability;
  release planning has a natural unit; ADR-036 and ADR-037 have a
  stable structure to build on.
- Harder: existing skills (`prd-to-mvp`, `adr-writer`,
  `issue-planner`, `workflow-docs`, `release`) all need
  phase-awareness; example projects need a phased version; the
  build-out-plan template doubles in conceptual surface.
- Maintain: phase metadata must stay consistent across PRD, plan,
  ADRs, issues, and milestones; drift silently breaks traceability
  (mitigation: lint phase references in `pr-review-packager` or a
  small validator script).
- Deferred: granularity defaults (ADR-036) and milestone lifecycle
  commands (ADR-037) build on this artefact shape; both are
  in-scope ideas but out of scope for this ADR.
