# ADR-043: Programmatic equivalent of `/check-plan` for in-skill invocation

**Status:** accepted
**Date:** 2026-05-06

## Context

[ADR-034](adr-034-plan-checker.md) shipped `/check-plan` as a quality
gate skill. Five skills currently document a `/check-plan` chain
point as a sub-step:

- `/adr-writer` — pre-write gate per ADR-034 step 7.
- `/prepare-issue` — pre-write gate on the prompt artefact.
- `/changelog` — content gate on grouped release notes (inlined when
  invoked from `/release`).
- `/milestone-summary` — content gate on the milestone summary
  (inlined when invoked from `/complete-milestone`).
- `/pr-review-packager` — ADR-references check on PR body.

The v3.3.0 baseline eval surfaced a kit-architectural friction that
reproduces across all five: **slash-commands aren't invokable from
inside another skill's execution**. `/check-plan`'s slash-command
surface assumes operator invocation; when a skill tries to chain to
it programmatically, the runtime cannot deliver. Every affected
skill currently self-flags this with a transparency note (cross-skill
consistency on the behaviour across all 5 — the eval found
identical wording patterns) and substitutes the deterministic check
logic inline against the criteria list from ADR-034.

The substitution works at runtime — the gate's logic does run, just
not via the slash-command surface — but the spec says one thing and
the runtime delivers another. Every skill author who adds a new
chain point has to know the substitution pattern, the spec drifts
from what is actually executed, and skill specs accumulate
caveat-language that says *"would invoke `/check-plan` here, but
runs the criteria inline because of …"*. This is the gap.

Two fix shapes are available, with materially different design
implications. Path 1 ships a non-slash-command interface to
`/check-plan`'s logic so skills can invoke it deterministically.
Path 2 formalises the inline-substitution pattern as canonical and
removes the slash-command-chain language from skill specs. The
choice is between *spec-grade enforcement* (the same logic always
runs, regardless of how it is invoked) and *spec-runtime alignment*
(the spec matches what the runtime can actually do, with no
fiction).

This ADR cross-references [ADR-034](adr-034-plan-checker.md) (the
plan-checker skill being amended) and is consumed by every skill
with a `/check-plan` chain point. The choice has implications for
[ADR-041](adr-041-auto-mode-permission-contract.md) (the
permission contract — a programmatic invocation surface is a new
kind of operation that needs category classification).

## Options considered

### Option A: Path 1 — programmatic equivalent

Ship a non-slash-command interface to `/check-plan`'s logic. Likely
shapes: a script under `bin/check-plan` (or `bin/check-plan-criteria`)
that skills invoke as a subprocess; or a kit-internal helper module
that skill specs reference directly. The slash-command form remains
for direct operator use.

- Pros: spec aligns with runtime — skills that document a chain
  point actually execute the kit's canonical check logic, not a
  per-skill inline approximation; spec-grade enforcement
  (deterministic execution regardless of skill author); central
  source of truth for the criteria list (skills consume the same
  logic rather than each maintaining their own inline copy);
  amendment to the criteria list propagates automatically.
- Cons: new code surface to maintain; programmatic-vs-slash-command
  duality must stay consistent (criteria changes update both
  surfaces, or one surface drifts); operator-interactive parts of
  `/check-plan` (any asks-for-confirmation steps) need a
  non-interactive variant for the programmatic path — strictly
  more code to write and maintain.

### Option B: Path 2 — formalise inline-substitution as canonical

Document that skills with `/check-plan` chain points run the
deterministic check logic inline rather than invoking the
slash-command. Update affected skill specs to make the inline
pattern canonical, not a workaround. Pure documentation change; no
new code.

- Pros: spec matches what the runtime can actually do; no
  programmatic-vs-slash-command duality to maintain; no new code
  surface; cheapest landing.
- Cons: every skill with a chain point carries its own inline
  substitution, which means the deterministic check criteria are
  duplicated across skill specs; spec drift between skills (one
  updates its inline copy, another does not) becomes a silent
  consistency-failure mode; future skills with chain points have
  to know the substitution pattern from day 1; the kit accumulates
  five-plus near-identical inline check blocks.

### Option C: Both — programmatic equivalent AND canonical inline pattern

- Pros: skills that want spec-grade enforcement use the
  programmatic surface; skills that want minimal coupling use the
  inline pattern; flexibility per skill.
- Cons: rejected — exactly the worst of both; two ways to do the
  same thing; spec drift between the two becomes a third failure
  mode; no clarity on which to use when.

## Decision

Adopt **Option A** (Path 1). Ship a programmatic equivalent of
`/check-plan` so skills with chain points can invoke the
deterministic check logic without the slash-command surface.

**Implementation shape** (final form decided in the implementing
issue):

1. **Programmatic surface:** likely `bin/check-plan` as an
   executable script that takes `--criteria-set <name>` and
   `--input <path-or-stdin>` arguments and emits structured output
   (pass / fail per criterion, machine-readable). Skills invoke it
   as a subprocess and parse the output.
2. **Slash-command surface unchanged:** `/check-plan` remains as
   the operator-facing entry point. Internally, the slash-command
   wraps the same criteria-evaluation logic that the programmatic
   surface exposes — both surfaces share one source of truth for
   the criteria list and the evaluation logic.
3. **Skill-spec migration:** the five skills with documented chain
   points (`/adr-writer`, `/prepare-issue`, `/changelog`,
   `/milestone-summary`, `/pr-review-packager`) update their specs
   to reference the programmatic surface and remove the
   slash-command-chain caveat language. The transparency note
   pattern that the v3.3.0 baseline surfaced is no longer needed
   because the spec now describes what the runtime actually does.
4. **Non-interactive variant:** any `/check-plan` step that today
   asks the operator for confirmation runs in non-interactive mode
   when invoked programmatically — failing closed if the input is
   ambiguous rather than blocking on operator input. Operators who
   want the interactive flow continue to invoke `/check-plan`
   directly.

**Permission contract (ADR-041) classification:** the programmatic
`bin/check-plan` is a category-1 (substitutable) operation —
read-only against the criteria list, no mutating side effects —
and may be invoked by skills under auto-mode without explicit
operator approval. Listed in the contract's category-1 examples.

## Consequences

- Easier: skills can deterministically run the kit's canonical
  check-plan logic without operator involvement; spec aligns with
  runtime, removing the cross-skill caveat language; the criteria
  list lives in one place rather than being duplicated inline
  across five skill specs; future skills with chain points have a
  clear, documented invocation surface from day 1; ADR-034's
  enforcement strengthens because more chain points actually run
  the gate.
- Harder: new code surface (`bin/check-plan` script + shared
  evaluation logic) to maintain; programmatic-vs-slash-command
  duality must stay consistent across criteria changes; the
  non-interactive variant adds code that the slash-command surface
  does not need; first kit script that skills invoke
  programmatically — establishes a precedent that future skills
  may follow, which is itself architectural surface area.
- Maintain: criteria list and evaluation logic live in one canonical
  module, consumed by both the slash-command surface and the
  programmatic surface; criteria changes update both surfaces in
  lockstep; the five affected skill specs reference the
  programmatic surface and stay in sync as criteria evolve;
  permission-contract classification (per ADR-041) needs review
  whenever the programmatic surface gains new operations.
- Deferred: extending the programmatic-surface pattern to other
  slash-command skills (e.g. a programmatic `/clarify` or
  `/audit-milestone`) is out of scope; revisit only if a similar
  chain-point friction surfaces. Migrating existing target
  projects' skill installations to the new surface is a kit-version
  bump concern handled by the existing release process; not in
  scope for this ADR's implementation. CI / lint enforcement that
  no skill spec contains the old `/check-plan` slash-command-chain
  language is also deferred; revisit if drift surfaces post-merge.
