# ADR-033: Clarification step (`/clarify`) before ADR drafting

**Status:** accepted
**Date:** 2026-04-30

## Context

Today the kit jumps from MVP scoping (`prd-to-mvp`) straight to
`adr-writer`. Ambiguity about implementation choices gets resolved
either inside ADR drafts (mixing decisions with discovery — ADR
quality drops) or during issue execution (too late, costs a session
and may force a backout). ADR-006's plan-first execution model is
best served when the planner does not stall on ambiguity.

Inspired by the GSD project's `discuss-phase` command, a focused
clarification step would surface "gray areas" — undecided
implementation questions — before ADRs are drafted, so `adr-writer`
captures decisions and not exploration. This complements ADR-031's
deeper planning layer: the planning doc captures sequencing and
risk; the clarify step captures settled-but-informal context that
sits below ADR weight.

## Options considered

### Option A: New `/clarify` skill producing `design/decisions.md` between `prd-to-mvp` and `adr-writer`

- Pros: dedicated skill with narrow scope; opt-in (small projects
  skip it); clean handoff to `adr-writer` (decisions consumed as
  context); pairs well with ADR-031's `/planning` skill.
- Cons: one more skill and artefact; line between
  `decisions.md` (informal) and an ADR (formal) needs explaining.

### Option B: Extend `prd-to-mvp` to emit a clarification section

- Pros: no new skill.
- Cons: conflates scoping with decision capture; re-running for one
  re-emits the other; forces clarification at MVP-time even when
  questions surface later.

### Option C: Per-phase clarification tied to ADR-032's phase shape

- Pros: phase-scoped context co-located with phase plans.
- Cons: blocked on ADR-032 shipping; over-structured for v1;
  fragments context across multiple files.

### Option D: Do nothing — keep relying on ADRs to surface ambiguity

- Pros: zero work.
- Cons: leaves the gap; ADR drafts continue to mix decisions with
  exploration; execution-time surprises continue.

## Decision

Adopt **Option A**. Ship `/clarify` as an opt-in skill at
`skills/clarify/` that reads `design/prd-normalized.md`,
`design/mvp.md`, and `design/planning.md` (when ADR-031 has
shipped), scouts the codebase if any, surfaces a checklist of
unresolved implementation questions for user selection, conducts
deep-dive resolution per question, and appends settled decisions to
`design/decisions.md`. The skill skips areas already locked by
accepted ADRs to avoid re-asking. `decisions.md` is below ADR
weight by design — it captures informal-but-settled context that
downstream agents (planner, executor) can rely on without asking
again. Decisions that harden into architectural commitments
graduate into ADRs via the next `adr-writer` run; the line is
"would superseding this need a new ADR?" — yes means it should be
an ADR; no means it lives in `decisions.md`.

## Consequences

- Easier: ADRs stay decision-only; planner and executor have a
  single canonical place to look for "what was settled informally";
  reduces context-window pressure during execution.
- Harder: one more artefact and skill; risk of duplication with
  ADRs if the line is not drawn cleanly (mitigation: explicit
  "graduate to ADR" criteria documented in the skill).
- Maintain: small — append-only doc, no parser dependencies;
  `/clarify` and `adr-writer` must agree on graduation criteria.
- Deferred: per-phase clarification (Option C) is rejected for v1;
  a single `decisions.md` is sufficient. Revisit once ADR-032 has
  shipped and phase-scoped context proves necessary in practice.
