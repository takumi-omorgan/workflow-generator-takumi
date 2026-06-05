# ADR-049: Follow-up PRD workflow for major feature updates

**Status:** accepted
**Date:** 2026-06-05

## Context

The kit's intake flow (ADR-003) is built for **starting** a project:
`idea-to-prd` → `prd-normalizer` → `prd-to-mvp` produce `design/prd.md`,
a normalized PRD, an MVP, and a build-out plan, all framed as the first
definition of a project. ADR-002 scoped the kit to new projects only,
and the steady-state loop in `workflow-guide.md` §3 deliberately skips
the scoping ceremonies after the first release, routing day-to-day work
through ad-hoc `gh issue create` and the per-issue loop.

That leaves a gap for **mature projects that need a major feature
update** — a new capability area, a change to assumptions baked into the
original PRD, work spanning multiple issues and ADRs. The roadmap
(Issue 21) names the two failure modes the gap produces:

1. **Overwriting the original PRD.** Re-running the intake flow rewrites
   `design/prd.md` as if the project were starting over, destroying the
   record of what the first release actually committed to.
2. **Forcing strategic change through ordinary issues.** Filing a major
   feature as a handful of `gh issue create` calls discards the
   PRD-level context — non-goals, affected assumptions, ADR impact,
   compatibility concerns — that a feature of that size needs.

The kit already has a precedent for the right shape: M2's machine-
readable contract layer was itself introduced as additive work that
extended the kit without resetting its definition. The roadmap asks for
that pattern to become a first-class, repeatable workflow with an
optional `/feature` (`/feature-prd`) verb, and to dogfood it by treating
the AI-PR-review feature (M5) as the first real addendum.

## Options considered

### Option A: Additive PRD addenda under `design/prd-addenda/`, plus a `feature-prd` skill and a template

A major feature becomes a numbered addendum
(`design/prd-addenda/NNN-feature-name.md`) that **extends** the original
PRD rather than replacing it. The addendum references current state and
ADRs, identifies changed assumptions, names ADR impact, includes an
explicit "what does not change" section, and decomposes the feature into
phased issues. A `feature-prd` skill (cat-1) drafts it from a template;
the verb layer (ADR-048) exposes it as `/feature`.

- Pros: original PRD stays intact as the historical record; each major
  feature has its own self-contained, reviewable definition; the
  decomposition feeds the existing `adr-writer` → `issue-planner` →
  per-issue loop unchanged; mirrors the existing ADR-per-decision and
  numbered-artefact conventions; the "what does not change" section
  makes scope stability explicit.
- Cons: a new artefact type and directory; authors must choose between
  "addendum" and "ordinary issue", needing a clear when-to-use rule.

### Option B: Append major features as new sections of the original PRD

- Pros: one PRD file; no new directory.
- Cons: `design/prd.md` grows unbounded and mixes the founding
  definition with every later expansion; diffs to "the PRD" become
  ambiguous; no clean per-feature review surface. Rejected.

### Option C: Versioned PRD snapshots (`prd-v1.md`, `prd-v2.md`)

- Pros: each version is a full, self-contained document.
- Cons: heavyweight — every update re-states the whole product; readers
  must diff full documents to see what a feature changed; encourages
  exactly the "starting over" framing the addendum model avoids.
  Rejected.

### Option D: Documentation-only pattern, no skill

- Pros: lightest; no new skill to maintain.
- Cons: the roadmap explicitly asks for an optional `/feature-prd` verb,
  and the value is in the skill enforcing the addendum's structure
  (ADR impact, affected assumptions, "does not change", phased
  decomposition) so a major feature is not under-specified. A template
  alone does not prompt the author through the analysis. Rejected in
  favour of a thin skill **plus** a template.

## Decision

Adopt **Option A**. Add a first-class follow-up PRD workflow.

**Artefact.** Major features are captured as numbered addenda under a
new `design/prd-addenda/` directory:

```text
design/prd.md
design/prd-addenda/
  001-agent-contract-layer.md
  002-ai-pr-review.md
```

The addendum **extends** `design/prd.md`; the original PRD is never
rewritten by this workflow.

**Template.** A new `templates/prd-addendum-template.md` defines the
structure: Context (original PRD, current milestone/state, trigger),
Problem, Goals, Non-goals, What changes, **What does not change**,
Affected assumptions, ADR impact, User stories, Requirements, Migration
and compatibility notes, Issue decomposition, Success metrics, Open
questions.

**Skill.** A new `feature-prd` skill (permission-category 1 — drafts a
local file, reviewed before any downstream `gh` action) fills the
template for one major feature. It reads the original PRD, current ADRs,
and `design/state.md`; identifies which ADRs need creation, revision, or
explicit supersession; decomposes the feature into phased issues with
dependencies and non-goals; and writes
`design/prd-addenda/NNN-feature-name.md`. It exits by naming the next
planning step (`/adr-writer` when decisions need ADRs, `/issue-planner`
when the decomposition feeds the backlog).

**Verb.** The addendum flow is the `/feature` verb in ADR-048's verb
layer; `/feature-prd` is its explicit slash name. The recommended flow:

```text
/feature-prd → /adr-writer → /issue-planner → /prepare-issue
            → /claude-issue-executor → /pr-review-packager
```

**When to use (and not).** Use a follow-up PRD when the change adds a
new capability area, changes original-PRD assumptions, needs multiple
issues or phases, requires one or more ADRs, or introduces
compatibility/migration/permission-boundary concerns. Do **not** use one
for one-off bugs, small docs fixes, obvious refactors, or a single
self-contained issue — those stay on the ordinary steady-state loop
(`workflow-guide.md` §3). When Claude Code is asked to implement a major
feature not already in the PRD or backlog, it proposes an addendum and
identifies ADR impact **before** implementing, rather than jumping into
code.

This is additive to ADR-003's intake model: `idea-to-prd` /
`prd-normalizer` / `prd-to-mvp` remain the **first-definition** path;
`feature-prd` is the **expansion** path. It does not supersede ADR-002's
new-project-only scope — a follow-up PRD operates on a project the kit
already owns, not on a foreign existing repo.

## Consequences

- Easier: mature projects extend their definition without overwriting
  it; each major feature gets a self-contained, reviewable PRD-level
  artefact that feeds the existing ADR/issue/PR machinery; scope
  stability is explicit via "what does not change"; the kit can manage
  its own roadmap expansions (M5 AI PR review enters as an addendum)
  the same way users manage theirs.
- Harder: one new artefact type, directory, template, and skill to
  maintain; authors need the when-to-use rule to avoid both
  over-formalising small work and under-specifying large work.
- Maintain: the addendum template and the `feature-prd` skill evolve
  with the intake flow; addendum numbering is sequential within
  `design/prd-addenda/`; the verb mapping (ADR-048) lists `/feature`.
- Deferred: automated linking of an addendum's "Issue decomposition"
  to created GitHub issues is left to `issue-planner`'s existing
  behaviour; no migration tooling is added (ADR-002). Retro-fitting
  addenda for features already shipped is out of scope.
