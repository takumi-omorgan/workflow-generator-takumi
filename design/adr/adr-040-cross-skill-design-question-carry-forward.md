# ADR-040: Cross-skill design-question carry-forward across the implementation chain

**Status:** accepted
**Date:** 2026-05-06

## Context

The implementation skill chain — `claude-issue-executor` (ADR-014) →
`pr-review-packager` (ADR-015) → `prepare-issue` (ADR-013) — produces
an audit trail of design decisions. When an issue's executor session
raises a design question that another, upcoming issue will need to
answer, the kit currently relies on chain-aware authoring to plumb
that question forward: the executor surfaces it in the eval summary,
the packager preserves it in the PR body, and `prepare-issue` picks
it up when generating the next issue's prompt.

The v3.3.0 baseline eval (research-tracker fixture) demonstrated this
end-to-end loop closing organically. On issues #4 + #5 (depth-scaled
note templates), `/claude-issue-executor 4` raised two design-coherence
questions in eval-summary follow-ups → `/pr-review-packager #16`
preserved them in the PR body's "Notes for #5" section →
`/prepare-issue 5` carried them into the next prompt as a load-bearing
section → `/claude-issue-executor 5` made both decisions with
documented reasoning → `/pr-review-packager #17` surfaced the
decisions with ✅ checkmarks. **Audit-trail-grade visibility — anyone
reading the PR sequence can trace the design-coherence work.**

The property emerged from the existing skills composing well, not
from a skill-spec hook requiring it. That is exactly the gap this ADR
exists to close: the kit aspires to deterministic cross-issue
design-coherence handoff but currently has only happy-accident
behaviour. Codifying it as a kit promise turns it from a property the
kit can demonstrate into a property the kit can guarantee regardless
of who is at the keyboard.

This ADR extends [ADR-038](adr-038-tighten-prompt-step.md) (auto-chain
prompt step). ADR-038 decided *whether* `/prepare-issue` runs
automatically; this ADR decides *what content* is plumbed through the
chain. It interacts with ADR-038's `--no-prompt` mode (which skips
`/prepare-issue` entirely on trivial issues — acceptable because
trivial issues by definition do not have cross-issue design coupling).
It also interacts with [ADR-034](adr-034-plan-checker.md) (plan
checker), since structured `design-questions:` output is a natural
consumer for the gate.

## Options considered

### Option A: All three skill-spec hooks together

- Pros: full chain-handoff loop becomes deterministic — every step
  from raising a question to answering it in the next issue's prompt
  is spec-mandated; cross-issue continuity is operator-visible in PR
  history without manual notes-for-future-self; closes the gap
  surfaced by the research-tracker eval; one shared schema across
  three skills makes the data flow auditable.
- Cons: three skills now share a structured-data contract that
  becomes load-bearing for cross-skill handoff; spec drift between
  the three would silently break the loop; over-eager population
  could clutter PR bodies on issues without genuine cross-issue
  design coupling.

### Option B: Executor + packager only — skip the prepare-issue hook

- Pros: smaller change surface; the carry-forward survives in PR
  history regardless of whether the next issue is run with
  `prepare-issue` or `--no-prompt`.
- Cons: operator-facing visibility ends at the PR body; the
  deterministic propagation into the next issue's prompt is lost,
  which is the highest-leverage step of the chain (it is what makes
  the executor *answer* the question rather than just *see* that one
  was raised).

### Option C: Document the pattern in the workflow guide only — no skill-spec change

- Pros: lightest possible change; no shared contract to maintain;
  preserves author judgment about when to use the pattern.
- Cons: the gap this ADR exists to close is precisely that
  author-discipline-based propagation is not deterministic; a
  documented pattern that depends on memory is what the kit already
  has, and it does not give the deterministic property.

## Decision

Adopt **Option A**. Add three coordinated skill-spec hooks across the
implementation chain, sharing one canonical `design-questions:`
schema:

1. **`claude-issue-executor`** — eval-summary's "Follow-ups" section
   gains a structured `design-questions:` subfield. Each entry
   carries: a one-line title, a target-issue reference (the upcoming
   issue the question affects), and a one-paragraph context note.
   Spec requires populating it when the executor's plan touches a
   load-bearing constraint shared with another upcoming issue;
   includes a "when not to populate" rule (no entry when the question
   is fully answered within the current issue, or when no upcoming
   issue depends on the answer).

2. **`pr-review-packager`** — when generating the PR body, scans the
   executor's eval-summary for `design-questions:` entries; emits
   each into a dedicated **"Notes for #N"** section in the PR body,
   one section per target-issue reference. This already happens
   organically on research-tracker; spec-mandating it removes the
   dependence on chain-aware authoring.

3. **`prepare-issue`** — when generating a prompt for issue #N, scans
   recently-merged PRs for "Notes for #N" sections; extracts and
   embeds them in a "Design questions carried forward from PR #M"
   subsection of the new prompt, with a clear instruction to the
   executor to address each one in its plan. Currently happens
   organically when run after the relevant PR merges; spec-mandate
   makes it deterministic.

The canonical schema lives in the workflow guide as a single source
of truth, cross-referenced from all three skill specs. When the
schema evolves, the three specs move together; alignment is enforced
at PR-review time.

`--no-prompt` mode (ADR-038) implicitly bypasses the hook because it
skips `prepare-issue` entirely. This is acceptable: `--no-prompt`
targets trivial issues, which by definition do not raise
cross-issue design questions worth carrying forward.

## Consequences

- Easier: design-coherence work that today depends on chain-aware
  authoring becomes deterministic regardless of operator memory or
  session-author identity; cross-issue continuity is operator-visible
  in PR history; the kit's audit-trail claim gains a structural
  enforcement point rather than relying on author convention.
- Harder: three skills now share a load-bearing structured-data
  contract; spec drift between them would silently break the loop;
  the "when to populate" rule in the executor needs to be tight
  enough that PR bodies do not accumulate noise on issues without
  genuine cross-issue coupling.
- Maintain: the `design-questions:` schema is new shared surface area
  with one canonical home in the workflow guide; changes require
  updates across three skill specs in lockstep; the schema and the
  spec-mandate rules are natural consumers of the [ADR-034](adr-034-plan-checker.md)
  plan-checker quality gate when implemented.
- Deferred: extending the carry-forward pattern to other skill chains
  (e.g. `prd-to-mvp` → `issue-planner`, or `audit-milestone` →
  `complete-milestone`) is out of scope for this ADR; revisit if the
  executor-chain pattern proves out. Cross-fixture validation that
  the pattern holds beyond research-tracker is also out of scope —
  belongs to the implementing issue's eval.
