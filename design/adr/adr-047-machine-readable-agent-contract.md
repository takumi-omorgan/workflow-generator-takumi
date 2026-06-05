# ADR-047: Machine-readable agent contract (kit.json, skill frontmatter, bin envelope)

**Status:** accepted
**Date:** 2026-06-05

## Context

The kit is GitHub-first (ADR-004) and plan-first, issue-by-issue
(ADR-006). Its skills, permission categories, inputs, outputs, and
handoff order are all documented in prose — `skills/*/SKILL.md`,
`docs/skills.md`, and `docs/workflow-guide.md`. That is good for
humans and was confirmed self-consistent by the M0 drift audit
(`notes/skill-metadata-handoff-audit.md`: no blocking drift).

It is poor for agents. An AI agent that wants to discover what skills
exist, which are safe to run unattended, what each consumes and
produces, and what runs next must read nineteen `SKILL.md` bodies and
infer a graph from prose. The roadmap's Milestone M2
(`design/workflow-generator-roadmap-and-issues-20260605.md`) calls for
a machine-readable contract layer so that an agent can answer those
questions from structured data instead.

This ADR records the shape of that layer. It covers five roadmap
issues that form one coherent decision: a machine-readable index
(Issue 6), structured skill frontmatter (Issue 7), a shared `bin/*`
JSON envelope and exit-code convention (Issue 8), a programmatic
`prepare-issue` surface (Issue 9), and a single agent-facing entry
doc plus a validation path that keeps the layer honest (Issues 6, 10).
It deliberately changes no slash-command UX and adds no runtime
dependency — it is additive metadata plus two read-only scripts.

The kit already has one programmatic surface, `bin/check-plan`
(ADR-043), with its own JSON shape predating this ADR. That prior
shape is grandfathered rather than rewritten (see Decision).

## Options considered

### Option A: One hand-maintained `kit.json` index, frontmatter as per-skill source, a sync check

- Pros: explicit and reviewable — a reader sees the whole kit in one
  JSON file; no build step or generator to run or trust; per-skill
  detail still lives next to each skill in frontmatter, so a single
  skill copied into a target project carries its own contract;
  drift between the two is caught by a small validator
  (`bin/validate-kit-json`) rather than prevented by machinery.
- Cons: the skill set, names, and permission categories are stated
  in two places (index and frontmatter) and can drift between edits;
  mitigated by the validator, which fails when they disagree.

### Option B: Generate `kit.json` from frontmatter at build time

- Pros: single source of truth; no possibility of index/frontmatter
  drift.
- Cons: introduces a generator and a "is the committed index stale?"
  check anyway; YAML-frontmatter parsing across nineteen files in a
  portable build step is more machinery than the problem warrants;
  contradicts the kit's "no premature automation, no speculative
  abstractions" rule (CLAUDE.md). Rejected: the explicit-plus-check
  path is simpler to review and maintain.

### Option C: Frontmatter only, no aggregate index

- Pros: zero duplication; nothing to keep in sync.
- Cons: fails Issue 6's core requirement — an agent should list all
  skills and the workflow graph *without* reading nineteen `SKILL.md`
  bodies. An aggregate index is the point. Rejected.

## Decision

Adopt **Option A**. The machine-readable agent contract has four
parts and one validator.

1. **`kit.json` at the repo root** — a single JSON document
   enumerating every skill with `name`, `slashCommand`,
   `permissionCategory`, a one-line `description`, structured
   `inputs`, `outputs`, and `next`; the happy-path `workflowOrder`;
   the `permissionCategories` legend; the `exitCodes` legend; and a
   `bin` list naming each script and which envelope it speaks. It is
   the aggregate index an agent reads first. It is a **kit-level
   artefact** — not copied into target projects in this iteration
   (see Consequences for the deferred follow-up).

2. **Structured skill frontmatter** — every `skills/*/SKILL.md`
   gains `inputs`, `outputs`, and `next` YAML fields alongside the
   existing `name`, `description`, and `permission-category`.
   `inputs` lists the skill's arguments and flags; `outputs` lists
   produced artefacts (file paths or external artefacts such as a
   GitHub PR); `next` lists handoff skills with a one-phrase
   condition. Because `skills/` is copied into a target project's
   `.claude/skills/` (ADR-001), each skill carries its own contract
   wherever it runs.

3. **A shared `bin/*` JSON envelope and exit-code convention** —
   new `bin/*` scripts that support `--format json` emit
   `{skill, version, status, outputs, next, errors}` and use a
   five-value exit-code convention: `0` success, `1` domain failure,
   `2` invocation error, `3` auth/service failure, `4` user
   cancellation. A script uses the subset of codes it needs.
   `bin/check-plan` keeps its prior `{criteria-set, result,
   criteria[]}` shape and `0/1/2` codes (ADR-043) — it is
   grandfathered and documented as the legacy surface, not rewritten,
   to avoid breaking its in-tree callers. Re-aligning it is a
   follow-up, not part of this ADR.

4. **A programmatic `prepare-issue` surface** — `bin/prepare-issue
   --issue N --format json` is a read-only analysis surface (distinct
   from the interactive `prepare-issue` skill). It reports the prompt
   path, whether the prompt exists, whether it is stale relative to
   the live issue, the ADR references found in the issue, detected
   gaps, and the recommended next action (`claude-issue-executor`),
   inside the standard envelope.

The **validation path** is `bin/validate-kit-json`: it confirms
`kit.json` is well-formed, that its skill set exactly matches the
`skills/` directories, that each skill's `name` and
`permissionCategory` agree with that skill's frontmatter, and that
every `next` target names a skill that exists in the index. This is
the documented synchronization check Issue 6 requires; deeper
field-by-field sync (inputs/outputs prose vs. structured) is left to
the M4 consistency-check issue (Issue 20). The single agent-facing
entry point is `docs/agent-contract.md`, which explains all four
parts so a future agent can use the contract without reading every
`SKILL.md`.

## Consequences

- Easier: an agent reads `kit.json` once to discover skills,
  permission categories, the workflow graph, and which scripts speak
  the standard envelope; a single installed skill still carries its
  own structured contract; new `bin/*` scripts have one envelope and
  exit-code convention to follow instead of inventing their own.
- Harder: the skill set, names, and permission categories now live in
  two representations (index + frontmatter) that must be kept in
  agreement — the cost of the explicit index. `bin/validate-kit-json`
  exists to make that drift loud rather than silent, and should be
  run when skills or frontmatter change.
- Maintain: `kit.json` must be updated when a skill is added,
  renamed, removed, or re-categorised, and `bin/validate-kit-json`
  re-run; `docs/agent-contract.md` is new shared surface that any
  future `bin/*` script or metadata change must respect;
  `bin/check-plan`'s legacy envelope is a documented exception that a
  future ADR may re-align.
- Deferred: shipping `kit.json` and the `bin/*` agent scripts into
  target projects via the installer (this iteration keeps them
  kit-level to avoid an installer-behaviour change); re-aligning
  `bin/check-plan` to the standard envelope; field-by-field
  consistency checks beyond name/category/next (M4, Issue 20); and a
  CI wiring of `bin/validate-kit-json` (M4). These are recorded as
  non-blocking follow-ups, not opened as work here.
