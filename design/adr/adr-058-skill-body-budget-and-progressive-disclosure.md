# ADR-058: SKILL.md body budget and progressive disclosure

**Status:** accepted
**Date:** 2026-07-14

## Context

The 22 shipped skills total **33,444 words** of SKILL.md body, measured
with `wc -w` over each body with YAML frontmatter excluded. The five
heaviest run 2,384–2,706 words each:

| Skill | Body words |
|---|---|
| `workflow-docs` | 2,706 |
| `claude-issue-executor` | 2,615 |
| `issue-planner` | 2,478 |
| `pr-review-packager` | 2,387 |
| `release` | 2,384 |

The body is loaded into the agent's context on every invocation, where it
competes with the actual project material the skill is supposed to operate
on. Long bodies also mix two audiences: operating instructions for the
agent, and rationale/reference for the human operator — the latter belongs
in `docs/`, which already exists and is linkable.

The kit has already moved deterministic mechanics out of skill prose and
into tested `bin/` helpers: [ADR-043](adr-043-programmatic-check-plan.md)
extracted the criteria engine behind `bin/check-plan`, and
[ADR-050](adr-050-reliability-validation-self-test.md) added the
schema/consistency/self-test layer. The script-vs-skill boundary rule that
generalises this is [ADR-054](adr-054-script-vs-skill-boundary.md), whose
helpers shipped under issue #13 but which is **still marked `proposed`** —
this ADR does not depend on that decision and does not resolve its status.

What remains after the mechanics move is prose. The bodies are still
dominated by background, edge-case narration, and ADR-history the agent
does not need at run time, and the kit has no stated budget, so bodies grow
monotonically — every fix adds a paragraph and nothing removes one.

We are optimising for: reliable instruction-following (shorter operating
instructions are followed more consistently), context headroom for the
user's project, and a forcing function against prose accretion.

## Options considered

### Option A: No budget; rely on review taste

- Pros: zero tooling.
- Cons: is the status quo that produced 2,700-word skills; taste does
  not survive dogfooding pressure.

### Option B: Budget with a soft ratchet — advisory checker, grace list that "shrinks each release"

Set an 800-word budget, add `bin/check-skill-budget` as an *advisory*
check, grandfather the 18 over-budget skills onto a grace list, and flip
the checker to blocking once that list empties.

- Pros: no migration required up front; nothing breaks on day one.
- Cons: **the ratchet has no binding force.** Nothing performs the
  advisory→blocking flip, the grace list has no owner or expiry, and an
  advisory check does not stop a body from growing. This is the status
  quo with a warning printed over it — the same "every fix adds a
  paragraph and nothing removes one" dynamic that produced the problem.

### Option C: Hard 800-word budget, blocking in CI from day one, no grace list

- Pros: maximally strict; unambiguous.
- Cons: **18 of the 22 skills fail it immediately** and the median skill
  (1,397 words) is 75% over. This blocks all unrelated work behind a
  22-skill rewrite, which is how migrations get abandoned half-done —
  leaving split docs with no owner and skills in an inconsistent state.

### Option D: Per-skill high-water-mark baseline, blocking from day one; 800-word budget for new skills

Add `bin/check-skill-budget` to the CI check set (the ADR-050 pattern),
**blocking from its first commit**, enforcing two rules:

1. **New skills** must be ≤ **800 words** of SKILL.md body (frontmatter
   excluded).
2. **Existing skills** are enumerated in a generated baseline file, each
   pinned to *its own current word count as a ceiling*. A skill may
   shrink freely; any commit that makes a baselined body **larger** fails
   CI. Lowering a ceiling is done by the same PR that migrates the skill;
   when a ceiling reaches ≤ 800 the entry is deleted from the baseline.
3. **Ceilings are monotonically non-increasing.** The checker compares the
   baseline against its own state in the previous commit and fails if any
   ceiling rises or if a new entry is added. Without this, a single PR
   could grow a body *and* raise its ceiling together and still pass —
   which would reduce the whole scheme to a suggestion. The only legal
   edits to the baseline are lowering a ceiling and deleting an entry.

The baseline empties through ordinary review, so there is no "flip" event
for anyone to forget. Growth is halted on day one even though the
migration has not happened yet.

Establish the split convention: SKILL.md keeps *what to do* — inputs,
steps, gates, outputs, handoffs, hard rules; rationale, ADR history,
worked examples and edge-case essays move to `docs/skills/<name>.md`.
**The body must remain self-sufficient at run time**: the agent loads only
SKILL.md and never follows the docs link, so anything it needs to produce
a correct result stays in the body. The docs link is for the human
operator. The `description` frontmatter field is unaffected.

- Pros: mechanically enforced from day one with no willpower dependency;
  stops accretion immediately; sequences the migration instead of
  demanding it all at once; matches the kit's existing validator/CI idiom.
- Cons: the baseline file is a new artefact to keep in sync (mitigated by
  generating it); a skill can still sit at 2,706 words indefinitely if
  nobody migrates it — the gate stops growth, it does not by itself
  compel shrinkage.

### Option E: Runtime summarisation (agent reads full body, self-condenses)

- Pros: no migration.
- Cons: spends the context anyway; non-deterministic; exactly the
  LLM-as-parser anti-pattern [ADR-043](adr-043-programmatic-check-plan.md)
  exists to eliminate.

## Decision

**Option D.** SKILL.md bodies are operating instructions under a
CI-enforced budget: 800 words for new skills, and a per-skill
high-water-mark ceiling for the 18 existing skills that exceed it, blocking
from the checker's first commit. Reference material moves to
`docs/skills/<name>.md`, and the body stays self-sufficient at run time.

## Consequences

- Skill invocations get cheaper and more reliably followed; the user's
  project gets the context headroom back.
- **Accretion stops immediately**, before any skill is split: a commit
  that grows a baselined body fails CI. This is the property Option B
  lacked.
- The migration is sequenced, not forced: the five heaviest skills
  (2,384–2,706 words) go first, each lowering its own ceiling; the
  baseline entry is deleted once a skill reaches ≤ 800. The baseline file
  empties through ordinary review, with no advisory→blocking flip to
  perform.
- The gate stops growth but does not compel shrinkage. A skill may sit at
  its ceiling indefinitely; driving the baseline to empty stays a planning
  decision, not something CI can force.
- The baseline is only a ratchet if its ceilings can never rise, so the
  checker must diff the baseline against the previous commit rather than
  merely reading it. A checker that trusts the committed baseline can be
  defeated by one PR that grows a body and raises its ceiling together.
- Authors must now decide where a sentence lives. The existing flat
  `docs/skills.md` gains the "what goes where" section that makes the call
  mechanical, and it is the file that documents the convention; the
  per-skill prose it points to lives in the new `docs/skills/<name>.md`
  files. These are two different surfaces and the ADR keeps them distinct.
- The split is only safe for rationale, history, worked examples and
  background. Runtime-necessary rules must not move: the agent never reads
  `docs/`, so a rule relocated there is a silently-dropped rule.
- The baseline lives in its own generated file, **not** in `kit.json`.
  `kit.json` and `validate-kit-json` stay untouched — that contract lives
  in frontmatter, which this ADR does not budget.
- `bin/check-skill-budget`, the baseline file, and the skill migrations are
  **new implementation work**, out of scope for this ADR and tracked as
  follow-up issues. This ADR decides only the rule.
- Deferred: token-based (rather than word-based) budgeting; revisit if
  word counts prove a poor proxy.
