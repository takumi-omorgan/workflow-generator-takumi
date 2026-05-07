# ADR-034: Plan-checker quality gate for ADRs and issue prompts

**Status:** accepted
**Date:** 2026-04-30

## Context

The kit produces ADRs (via `adr-writer`) and issue prompts (via
`prepare-issue`), but neither has a structured quality check before
they are accepted. Bad ADRs (vague decisions, missing alternatives,
inconsistent with accepted ones) and thin prompts (no acceptance
criteria, oversized scope, missing ADR links) are caught only at
execution time, when the cost of fixing them is highest — a session
already started, sometimes a branch already opened.

Inspired by the GSD `gsd-plan-checker` agent, which validates a
plan on multiple dimensions and iterates up to a small fixed cap
until pass, the kit should have an analogous gate. ADR-029 is the
prompt-generation contract this checker enforces; ADR-038 may
adjust the prompt's content shape and so the criteria here.

## Options considered

### Option A: Standalone `/check-plan` skill, chained from `adr-writer` and `prepare-issue`

- Pros: reusable from any starting point; easy to invoke ad-hoc on
  an existing artefact; producers chain it as a pre-commit gate
  with `--skip-check` opt-out.
- Cons: one more skill; criteria source-of-truth needs a clear
  home.

### Option B: Inline check inside each producing skill

- Pros: no new skill at the top level.
- Cons: couples checker logic to each producer; duplication;
  cannot run ad-hoc on an artefact you didn't just generate.

### Option C: Two checkers (one for ADRs, one for prompts)

- Pros: criteria are tightly tuned per artefact.
- Cons: doubles the surface; most criteria (clarity, structure,
  references) overlap.

### Option D: Linter-style script for structural rules only

- Pros: fast and deterministic.
- Cons: cannot reason about content quality (e.g. "decision is
  vague") which is where most defects live.

## Decision

Adopt **Option A**. Ship `/check-plan` at `skills/check-plan/` as a
single skill that takes an artefact path (ADR or issue prompt),
detects type from path/frontmatter, runs a checklist tuned per type,
returns pass/fail with specific revisions, and iterates with the
user up to 3 rounds before yielding. `adr-writer` and
`prepare-issue` chain it automatically as a pre-commit gate;
`--skip-check` opts out for known-good rapid iteration. The
checker emits warnings (not hard errors) for dimensions it cannot
verify deterministically — the user decides whether to fix.
Criteria live at `skills/check-plan/criteria.md`, version-locked to
the templates the checker validates.

ADR criteria: clear context / decision / consequences; references
the right ADRs; doesn't conflict with accepted ones; options have
both pros and cons; decision names one of the listed options.

Prompt criteria: acceptance criteria present; correct ADR links;
fits the build-out-plan phase (per ADR-032 if shipped); single-PR
scope; no ambiguous "TBD" placeholders.

## Consequences

- Easier: fewer execution-time surprises; ADR/prompt quality stops
  depending on author discipline; new kit users get scaffolding-grade
  quality from day one.
- Harder: slower drafting loop (mitigation: 3-round cap and
  `--skip-check`); checklist drift if templates evolve without
  updating the criteria.
- Maintain: criteria document at `skills/check-plan/criteria.md` is
  the source of truth; must be updated whenever ADR or prompt
  templates change; consider a CI check that flags template edits
  without criteria edits.
- Deferred: plan-checking for the build-out plan and `planning.md`
  artefacts (ADR-031); v1 covers ADRs and issue prompts only.
  Build-out-plan and planning.md checks can be added in a follow-up
  ADR once their formats are exercised.
