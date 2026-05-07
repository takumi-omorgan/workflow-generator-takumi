# ADR-031: Deeper planning workflow between MVP scoping and ADR drafting

**Status:** accepted
**Date:** 2026-04-30

## Context

The kit's planning chain today goes from rough idea to GitHub issues
in five steps: `idea-to-prd` → `prd-normalizer` → `prd-to-mvp` →
`adr-writer` → `issue-planner`. For small projects this is the right
amount of scaffolding. For non-trivial projects it is too thin —
there is no canonical home for requirements decomposition,
risk/assumption logs, sequencing rationale beyond a flat build-out
plan, or research/spike findings that need to land before ADRs are
drafted.

ADR-006's plan-first execution model assumes a plan exists. For
large projects the plan needs scaffolding the kit doesn't currently
offer, so authors either retrofit it into ADRs (mixing decisions
with discovery) or carry it in their head (no audit trail). ADR-028
widened the kit's scope to be workflow-agnostic, which makes the
case for an explicit planning layer stronger — non-software projects
(research, curriculum, content) typically need decomposition before
commitment more than small software builds do.

This ADR establishes the planning artefact and skill that ADR-032
(phases), ADR-033 (clarification), ADR-035 (state.md), and ADR-037
(milestone lifecycle) all build on. Settling its shape here lets
those follow-on ADRs depend on a stable contract.

## Options considered

### Option A: New opt-in `/planning` skill producing `Design/planning.md`

- Pros: dedicated artefact between `Design/mvp.md` and ADRs;
  downstream skills (`adr-writer`, `issue-planner`) read it when
  present and ignore it when absent, so small projects are
  unaffected; clean handoff to ADR-032 (phases as a planning
  output) and ADR-033 (clarification can append to it).
- Cons: one more skill and template to teach; another file in the
  `Design/` tree.

### Option B: Extend `prd-to-mvp` to optionally emit a deeper planning section

- Pros: no new skill; single command to learn.
- Cons: conflates scoping (what's in the MVP) with planning (how
  it sequences and what risks it carries) into one artefact;
  re-running for one concern re-emits the other; harder to share a
  stable contract with downstream skills.

### Option C: Do nothing — keep the flat model

- Pros: zero work; the current chain ships.
- Cons: leaves the gap that prompted this ADR; ADR-032/033/035/037
  have nothing to anchor to.

## Decision

Adopt **Option A**. Ship a new opt-in `/planning` skill at
`skills/planning/` that reads `Design/prd-normalized.md` and
`Design/mvp.md`, prompts for requirements decomposition, risks,
assumptions, sequencing rationale, and open research questions,
and writes `Design/planning.md` from a new
`templates/planning-template.md`. Output is consumed by `adr-writer`
(decisions hardened from the planning doc) and `issue-planner`
(sequencing rationale informs phase ordering). The skill is opt-in;
small projects continue using the current lightweight flow without
change.

## Consequences

- Easier: large projects get a structured gap-filler between
  scoping and execution; risks and assumptions become first-class
  artefacts; ADR-032/033/035/037 have a stable contract to build on.
- Harder: one more optional skill, template, and artefact to teach;
  downstream skills must learn to read `planning.md` when present.
- Maintain: the planning template and skill stay in lockstep with
  `adr-writer`'s input expectations and the build-out plan format
  ADR-032 establishes.
- Deferred: phase decomposition (ADR-032), gray-area resolution
  (ADR-033), phase-density control (ADR-036), and milestone
  lifecycle (ADR-037) all build on this layer — implementing them
  is out of scope here.
