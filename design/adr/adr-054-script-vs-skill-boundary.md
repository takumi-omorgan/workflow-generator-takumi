# ADR-054: Deterministic script vs. Claude-skill boundary

**Status:** proposed
**Date:** 2026-06-09

## Context

The kit is mid-migration from a skill-only architecture to a script-backed
one. It already has the load-bearing pieces: a JSON-envelope contract with
standard exit codes (ADR-047, `bin/lib/json-envelope.sh`), a deterministic
criteria engine extracted out of a skill (ADR-043, `bin/check-plan`), an
idempotency-receipt layer (`bin/write-receipt`), a self-test/consistency
harness (ADR-050), and a fully-scripted AI PR review runtime where the LLM is
isolated to one validated call.

Several skills the team itself labels "mechanical" still ask the LLM to *be a
parser* inline in the prompt: `changelog` parses `git log` delimiters and
applies a fuzzy dedupe; `adr-writer` derives the next ADR number by counting
files; `pr-review-packager` extracts issue numbers, ADR tokens, and
carry-forward context with regex described in prose; and `pause`, `resume`,
`prepare-issue`, `claude-issue-executor`, and `workflow-docs` each describe
marker-fence editing in natural language — five copies of a parser the LLM
re-derives every run. The `schemas/*.yaml` files exist but are not enforced as
a runtime contract.

This is the exact failure mode ADR-043 documents: the spec drifts from what is
actually executed, every skill author has to re-know the pattern, and an LLM
approximating a parser is the least reliable thing it can do. Before the kit is
published, this residual parse/count/splice work should be hardened.

## Options considered

### Option A: Leave the mechanics inline in the skills

- Pros: no new scripts; nothing to install or register.
- Cons: ships the drift ADR-043 already diagnosed; public users inherit
  LLM-as-parser brittleness; marker-fence prose risks silent corruption of
  user-authored text.

### Option B: Extract the deterministic primitives into small, tested `bin/` helpers that skills call

- Pros: finishes ADR-043's direction; byte-stable, fixture-tested behavior;
  skills shrink to interviewing, scoping, prose, routing, and approval; reuses
  the existing envelope/exit-code contract and the AI-review eval harness as a
  model.
- Cons: more `bin/` scripts to register, install, and keep green; each skill
  must be rewired to call its helper.

### Option C: Build a generalized skill-execution framework

- Pros: one abstraction for all skill mechanics.
- Cons: the speculative abstraction the kit's own CLAUDE.md forbids; large
  surface; over-engineered for a handful of concrete primitives.

## Decision

Adopt Option B under one decision rule: **if two competent runs must produce
byte-identical output, it is a deterministic script; if two competent runs may
legitimately differ, it stays a Claude skill.** Parsing a diff, counting ADRs,
and splicing a marker fence are the former; reviewing a diff, scoping an MVP,
and authoring decision prose are the latter. A skill *calls* the helper for the
deterministic spine and keeps the judgment, prose, and approval gate.

The hardening scope for this round is a marker-fence read/write helper
(`bin/lib/fences.py` + a `bin/fence` CLI, since skills are markdown and can
only shell out), `bin/changelog-collect`, `bin/adr-alloc`, a runtime schema
validator (`bin/validate-schema`), `bin/pr-context`, and the `workflow-docs`
splice mechanics (`bin/docs-render`). `bin/milestone-collect` and
`bin/release-suggest` are deferred — they add a live-`gh`/heuristic surface and
are not needed before export. The AI PR review runtime is the reference
architecture and is **not** rewritten; `bin/review-eval` stays green.

Judgment-dominant skills (`idea-to-prd`, `feature-prd`, `prd-normalizer`,
`prd-to-mvp`, `planning`, `clarify`, `issue-planner`, the review judgment
itself) stay skills and are explicitly out of scope for scripting.

## Consequences

- New deterministic helpers each emit the standard JSON envelope, are
  registered in `kit.json`, and are covered by offline golden/fixture tests on
  the AI-review eval model.
- Helpers consumed by default-installed skills must travel with the installer,
  so `bin/lib/json-envelope.sh` becomes a default-installed library rather than
  AI-review-only.
- A skill→script flag contract check guards against the spec/runtime
  divergence ADR-043 named.
- The dependency-light posture is preserved: stdlib Python only, no PyYAML or
  templating engine; YAML stays line-based.
- This ADR implements ADR-043's stated direction across more surfaces; it does
  not reverse any accepted decision and leaves existing ADRs immutable.
