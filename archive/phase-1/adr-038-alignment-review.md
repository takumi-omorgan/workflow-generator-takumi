# ADR-038 alignment review — content boundary audit

**Date:** 2026-04-30
**ADR:** [`Design/adr/adr-038-tighten-prompt-step.md`](../Design/adr/adr-038-tighten-prompt-step.md)
**Issue:** #47

## Why this audit exists

ADR-038's Decision section imposes a *mandatory* obligation:

> Before this ADR moves from `proposed` to `accepted`, audit the
> prompt's content shape against ADR-031 (`planning.md`), ADR-032
> (phase context in `build-out-plan.md`), ADR-033 (`decisions.md`),
> ADR-034 (plan checker criteria), ADR-035 (`state.md`), and
> ADR-037 (milestone summary). If any of those produces an artefact
> whose content the prompt currently duplicates, trim the prompt's
> content boundary so each artefact has one canonical home and the
> prompt links rather than restates. Record the resulting boundary
> changes in this ADR or a follow-up amendment ADR before
> implementing.

ADR-038 was accepted on 2026-04-30 with this obligation pending.
Per `CLAUDE.md`'s "never edit accepted ADRs in place" rule, the
result is recorded here (and as a one-paragraph editorial comment
in `prompts/_template.md`'s header) rather than as an amendment to
ADR-038 itself.

This is a one-shot audit; no marker fences. If the prompt template
or any of the six referenced ADRs evolves materially in the future,
re-run the audit and append a new section below rather than editing
this one.

## Audit method

For each of the six ADRs in scope, I asked: *does
`prompts/_template.md`'s current section content overlap with what
this ADR's artefact is supposed to hold?* Three possible verdicts:

- **(a) Trim** — overlap is real; the prompt section restates
  content the artefact owns. Trim the prompt section so it links
  rather than restates.
- **(b) No change** — scopes are orthogonal (issue-scope vs.
  project/session/phase-scope, or per-issue immutable vs.
  cross-cutting mutable). The artefacts coexist without duplication.
- **(c) Edge case** — not duplication today, but worth flagging in
  case Phase 1/2 work shifts the boundary.

## Per-ADR decisions

### ADR-031 — `Design/planning.md`

**What planning.md holds.** Project-wide discovery: requirements
decomposition, risks, assumptions, sequencing rationale across all
issues, open research questions.

**Prompt sections that could overlap.** `Why it matters` (one
paragraph on motivation), `Requirements` (the issue's bullet list).

**Verdict: (b) No change.** The prompt's `Why it matters` is the
*issue*-level motivation; planning.md's risks and assumptions are
*project*-level. The prompt's `Requirements` enumerates this issue's
work; planning.md's decomposition spans every issue in the project.
Orthogonal scopes — readers consult both.

### ADR-032 — `## Phase N` blocks in `build-out-plan.md`

**What phase blocks hold.** Per phase: goal, scope bullets, ADR
dependencies, deliverables, exit criterion.

**Prompt sections that could overlap.** `Context` (project-level
preamble; mentions the workflow doc and rules but no phase content),
`Why it matters` (issue motivation).

**Verdict: (b) No change.** The prompt already references the phase
by name when one applies (via the optional `**Phase:**` frontmatter
on linked ADRs); it does not restate phase scope or exit criteria.
Build-out-plan owns phase content; the prompt is downstream.

### ADR-033 — `Design/decisions.md`

**What decisions.md holds.** Informal-but-settled implementation
decisions below ADR weight: gray areas resolved before ADR
drafting, plus the rationale behind each.

**Prompt sections that could overlap.** `Scope and constraints`
(issue-specific guard rails — primary/avoid folders, project-
specific gotchas).

**Verdict: (b) No change.** The prompt's `Scope and constraints`
captures *this issue's* guard rails — what folders to touch, what
to avoid for *this work*. `decisions.md` is project-wide settled
context that downstream agents (planner, adr-writer, executor) all
consult. The prompt may *reference* a settled decision when scoping
this issue (`"per the decision to use Yjs (Design/decisions.md)"`),
but it doesn't restate the rationale or the alternatives weighed.

### ADR-034 — `/check-plan` criteria

**What check-plan criteria hold.** Structural validation rules for
ADRs and prompts (the criteria document at
`skills/check-plan/criteria.md`): does the artefact have its
required sections, do options have pros/cons, etc.

**Prompt sections that could overlap.** `Acceptance criteria`
(end-state outcomes for the issue), `Evaluation & testing
requirements` (verification steps).

**Verdict: (c) Edge case — flag, no change today.** The prompt's
`Acceptance criteria` is end-state outcomes (*"the user can do X"*);
`/check-plan`'s `PROMPT-C1` is a structural rule (*"does the
prompt's `Acceptance criteria` section exist and have ≥1 bullet?"*).
These are orthogonal — one is the content the user authors; the
other is the validator that confirms the section was authored. They
coexist without duplication.

The flag: if Phase 1/2 work in this PR (or a future PR) tightens
the prompt's content shape — say, introduces a new required section
— `criteria.md` will need a corresponding update, governed by
ADR-034's existing version-lock contract and
`bin/check-plan-criteria-drift`. No action here, but the link is
recorded so future authors see the dependency.

### ADR-035 — `Design/state.md`

**What state.md holds.** Project-wide session-mutable pointer:
current phase, in-flight issue, recent work (last 5 PRs), blockers,
"continue here" pointer.

**Prompt sections that could overlap.** `Context` (session-level
project description + workflow-doc pointer).

**Verdict: (b) No change.** The prompt is *per-issue and immutable*
— written once by `prepare-issue`, consumed once by
`claude-issue-executor`. `state.md` is *project-wide and
session-mutable* — refreshed by every step of the prepare → execute
→ review chain plus `/pause` and `/resume`. The two artefacts have
inverse temporal scopes and never overlap.

### ADR-037 — `/milestone-summary`

**What milestone-summary holds.** Phase-close retrospective: what
shipped, ADRs adopted in the phase, lessons learned, work deferred
to the next phase. Aggregated across every issue in the milestone.

**Prompt sections that could overlap.** None obvious.

**Verdict: (b) No change.** The prompt is strictly issue-scoped;
`/milestone-summary` aggregates across all issues in a phase. The
two artefacts have inverse aggregation scopes (one issue ↔ one
milestone of issues). They run at different temporal points
(prompt before issue execution; milestone-summary after phase
close).

## Summary

| ADR | Verdict |
|---|---|
| ADR-031 — `planning.md` | (b) No change |
| ADR-032 — phase blocks | (b) No change |
| ADR-033 — `decisions.md` | (b) No change |
| ADR-034 — check-plan criteria | (c) Edge case flagged; no change today |
| ADR-035 — `state.md` | (b) No change |
| ADR-037 — `/milestone-summary` | (b) No change |

**Six of six are "no architectural change."** No follow-up
amendment ADR is required.

## Action taken

1. **No section is removed from `prompts/_template.md`.**
2. **No new section is added to `prompts/_template.md`.**
3. **One editorial comment is added** to the header HTML-comment
   block in `prompts/_template.md`, capturing the content-boundary
   principle so future authors don't unknowingly reintroduce
   duplication. The comment is kept short and points at this audit
   note for full reasoning.

The downstream Phase 1/2 work (auto-chain `prepare-issue` and add
`--no-prompt`) lands on a content boundary that has been audited
and confirmed clean.

## Follow-ups

- **None required for this issue.**
- **Future trigger:** if any of the six referenced ADRs evolves —
  e.g. a new section is added to `planning.md` or `state.md` —
  re-run this audit and append a new section below rather than
  editing this one.
- **Future trigger:** if the prompt template gains a new section
  (Phase 1/2 work in this issue does *not* introduce one), re-run
  `bin/check-plan-criteria-drift` and update
  `skills/check-plan/criteria.md` accordingly.
