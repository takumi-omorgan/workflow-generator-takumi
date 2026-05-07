# ADR-041: Auto-mode permission contract for strict-mode skill operations

**Status:** accepted
**Date:** 2026-05-06

## Context

[ADR-039](adr-039-plan-mode-for-significant-tasks.md) shipped
harness-level plan mode for significant tasks in
`claude-issue-executor`. The v3.3.0 baseline eval calibrated F24 (the
executor's plan-mode bypass under "auto mode") across three fixtures:
HIGH severity on md-notes (silent bypass), MEDIUM on podcast-pipeline
(session-context-dependent), LOW on research-tracker (bypass but
self-reported in alignment check). The trajectory is positive — the
ADR-039 fix moved the bypass from "silent" toward "self-reported" —
but the underlying principle stands: even at LOW severity, the kit
should not allow auto-mode to silently substitute for an explicit
operator gate on significant tasks.

The same shape appears beyond `claude-issue-executor`. F23
(`/pr-review-packager`'s strict-mode-vs-runtime mismatch) is the same
class of bug: a skill operation that should require explicit operator
approval being substituted by auto-mode classifier inference. Any
future skill with strict-mode contracts will reproduce it.

ADR-039 scoped its fix narrowly to executor plan mode. The kit needs
a generalised rule: an explicit **permission contract** that names
what auto-mode is allowed to substitute for, what it is not allowed
to substitute for, and how operators authorize substitutions when
the contract permits them. Without this, every new strict-mode gate
becomes a re-litigation of the same question, and silent-substitution
regressions remain possible whenever a skill author misses the
implicit rule.

This ADR generalises ADR-039 from a per-skill rule into a kit-wide
contract. It does not supersede ADR-039 — the executor-specific
significant-task checklist remains in force; this ADR adds the
operations-shape framing that the checklist instances.

## Options considered

### Option A: Full kit-wide permission contract spec

- Pros: strongest enforcement; single source of truth that names
  every skill operation as substitutable or not; clearest spec for
  skill authors to consult when adding new operations; closes
  F24-class regressions structurally rather than per-skill;
  predictable behaviour for operators regardless of which skill
  they invoke.
- Cons: biggest documentation surface; new shared spec touching
  every skill with strict-mode gates; auto-mode loses some
  convenience (one extra operator interaction per significant-task
  session) — judged worth it for spec-grade enforcement.

### Option B: Skill-by-skill fix without a unifying spec

- Pros: cheaper to land — patch `/claude-issue-executor` and
  `/pr-review-packager` independently; no kit-wide doc churn.
- Cons: drift risk grows linearly as new strict-mode skills ship;
  the unifying principle stays implicit; every new skill author has
  to discover the rule rather than consulting it.

### Option C: Documentation-only change in the workflow guide

- Pros: lightest possible change; no spec coupling; preserves
  author judgment.
- Cons: this is exactly the gap the ADR exists to close. The eval
  data shows authors comply with the principle organically — but
  the kit needs spec-grade enforcement, not author convention,
  precisely because organic compliance is what F24 demonstrated
  cannot be relied on across versions and authors.

### Option D: Reject auto-mode entirely on strict-mode skill operations

- Pros: most secure; auto-mode classifier fails closed on any
  operation marked non-substitutable; no possibility of silent
  bypass.
- Cons: over-restrictive for genuinely-trivial cases that the
  contract should permit (e.g. ADR status flips, single-line typo
  fixes); rejected as too blunt.

## Decision

Adopt **Option A**. Define a kit-wide auto-mode permission contract
that classifies skill operations into three categories. Codify it as
a new section of the workflow guide (single source of truth) and
cross-reference from every affected skill spec.

**Three operation categories:**

1. **Substitutable** — auto-mode may proceed without explicit operator
   approval. Examples: file reads, repo scans, lint checks, format
   passes, ADR / feature-ideas status flips, single-typo fixes,
   generation of artefacts that are reviewed before they are written
   to disk by another step.

2. **Operator-acknowledged-bypass** — auto-mode may proceed but must
   explicitly state in the skill's chat output that the bypass is
   happening, citing the contract section that permits it. Examples:
   significant-task plan mode (ADR-039) when the operator has
   pre-authorized auto-mode for the session via an explicit toggle.
   The bypass is operator-acknowledged, never silent.

3. **Non-substitutable** — auto-mode never substitutes for explicit
   operator approval on these operations regardless of mode. Examples:
   `git push`, `gh pr create`, `gh release create`, `git tag`,
   creating GitHub issues or comments, running migrations,
   modifying `.claude/settings*.json`, modifying `bin/*` scripts,
   any operation with public visibility or hard-to-reverse blast
   radius.

**Two skill-spec changes that instance the contract:**

1. **`claude-issue-executor`** — significant-task gate (ADR-039) is
   triggered by an explicit operator-set toggle, not by auto-mode
   classifier inference. If auto-mode is active, the skill asks the
   operator at session start ("Enter plan mode for this task? yes /
   no / decide-from-scope") rather than auto-entering or
   auto-skipping. The "yes / decide-from-scope" branches use
   ADR-039's existing checklist; "no" requires the operator to
   acknowledge the bypass in writing in the skill's chat output.

2. **`pr-review-packager`** — extends the same principle to the
   PR-creation gate. The skill's existing behaviour (asking for
   explicit yes regardless of auto-mode, confirmed by research-tracker
   across 5 PRs) becomes the canonical pattern for any skill with
   public / hard-to-reverse actions: auto-mode does NOT substitute
   for explicit approval on category-3 operations.

**Documentation change:**

3. **Workflow guide gains an "Auto-mode permission contract" section**
   that lists the three categories with examples, names which skill
   operations fall into which category, and is the single source of
   truth that skill authors consult when adding new strict-mode
   gates. The list is exhaustive for shipped skills as of this ADR
   and grows as new skills ship; the contract requires every new
   strict-mode operation to be classified before merge.

`--no-prompt` mode (ADR-038) interaction: `--no-prompt` is itself a
category-1 operator-pre-authorization for the trivial-issue path;
it does not bypass category-3 operations (the executor still cannot
push or create PRs under `--no-prompt` without explicit approval).

## Consequences

- Easier: operators get predictable, spec-grade enforcement on
  hard-to-reverse skill operations regardless of which skill they
  invoke or which auto-mode classifier version is in effect; bypass
  becomes operator-acknowledged rather than silent; F24-class
  regressions become structurally impossible rather than
  author-convention-dependent; new skill authors have one document
  to consult rather than reverse-engineering the rule from existing
  ADRs.
- Harder: auto-mode loses one round-trip of convenience per
  significant-task session; skill authors classifying new operations
  must consult the contract rather than judging case-by-case; spec
  drift between contract and skill specs is a new failure mode that
  PR review must catch.
- Maintain: the contract is new shared surface area with one
  canonical home in the workflow guide; every new strict-mode skill
  operation needs explicit classification at merge time; the three
  category lists evolve as the kit grows; ADR-039's executor-specific
  significant-task checklist remains the per-skill instance of the
  category-2 rule and stays in sync with the contract.
- Deferred: applying the contract retroactively to skills whose
  current strict-mode behaviour is already category-correct
  (e.g. `pr-review-packager`'s confirmed-yes pattern) is doc-only —
  no behavioural change required. Migration ordering is left to the
  implementing issue. CI / lint enforcement of the contract (e.g.
  static check that no skill spec authorizes a category-3 operation
  under auto-mode) is out of scope; revisit if drift surfaces in
  future evals.
