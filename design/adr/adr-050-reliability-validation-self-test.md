# ADR-050: Reliability layer — canonical schemas, carry-forward and consistency validation, idempotency receipts, and a workflow self-test

**Status:** accepted
**Date:** 2026-06-05

## Context

Milestones M2 ([ADR-047](adr-047-machine-readable-agent-contract.md)) and
M3 ([ADR-048](adr-048-unified-workflow-control.md),
[ADR-049](adr-049-follow-up-prd-workflow.md)) gave the kit a
machine-readable contract and a unified control model. Both noted that
their load-bearing conventions were protected by **PR review only**:
ADR-047 deferred "field-by-field consistency checks ... (M4, Issue 20)"
and "CI wiring of `bin/validate-kit-json` (M4)"; ADR-040's carry-forward
schema lives as prose in `docs/workflow-guide.md` §6 with "spec drift
between §6 and any one SKILL.md silently breaks the carry-forward loop";
and the M3 eval recorded "no machine enforcement of the new contracts" as
carried-forward friction.

Milestone M4 in the roadmap
(`design/workflow-generator-roadmap-and-issues-20260605.md`) closes that
gap. It is five issues that form one coherent decision — make the kit
robust enough for repeated human and agent use by validating schemas,
recording receipts, and testing core flows: a canonical carry-forward
schema (Issue 16), a validator for it (Issue 17), idempotency receipts for
mutating skills (Issue 18), a workflow self-test (Issue 19), and
consistency checks plus their CI wiring (Issue 20).

The kit's standing constraints shape the solution: "no premature
automation, no speculative abstractions" (`CLAUDE.md`), the
standard `bin/*` JSON envelope and exit-code convention (ADR-047), and
backwards compatibility for existing target-project installs (ADR-002
scopes the kit to new projects, but a metadata change must not break a
project already on a prior version).

## Options considered

### Option A: One coherent reliability layer — canonical schema files, dependency-free validators on the standard envelope, file-based receipts, and a non-mutating self-test, wired into CI

- Pros: the five issues reinforce each other — the schema file is the
  single source the carry-forward validator enforces, the consistency
  checker guards that the file stays referenced, the self-test runs both
  validators (and the receipt logic) on a stub as its regression test, and
  CI runs the whole surface on every push. New scripts reuse the existing
  envelope/exit-code convention rather than inventing surfaces. Receipts
  are a documented JSON *file* convention the agent can write directly, so
  they work in any target project with no installer change and no new
  dependency. Schemas are plain YAML read by the `python3` already used in
  `bin/`. Closes the M2/M3 "enforced by PR review only" gap with machine
  checks.
- Cons: adds four `bin/*` scripts and a `schemas/` directory — more kit
  surface to maintain; the carry-forward schema now has two homes (prose
  §6 and the file) that must agree, mitigated by `check-consistency` and
  the validator reading the file rather than a second copy of the rules.

### Option B: Encode the schemas and checks as a JSON-Schema toolchain with a real validator library

- Pros: standards-based; richer constraint vocabulary; less bespoke
  parsing code.
- Cons: pulls a JSON-Schema library into a kit that has deliberately
  avoided runtime dependencies; the carry-forward producer data is YAML
  embedded in markdown, which a JSON-Schema validator does not read
  without more glue than the constraint set (three fields, one pattern,
  no-extra-fields) warrants. Contradicts "no speculative abstractions."
  Rejected: the explicit, dependency-free checker is simpler to review and
  runs anywhere `python3` does.

### Option C: Document the conventions and keep PR review as the enforcement point (no new scripts)

- Pros: zero new surface; nothing to keep in sync.
- Cons: this is the status quo M4 exists to change. The M3 eval already
  recorded that review-only enforcement lets contracts drift silently; a
  documented-only carry-forward schema and consistency rule give no
  machine signal and no CI gate. Rejected: it does not satisfy any of the
  five issues' "validation catches it before release" acceptance criteria.

## Decision

Adopt **Option A**. M4 adds one reliability layer with five parts:

1. **Canonical schema files under `schemas/`.** `schemas/design-questions.v1.yaml`
   is the machine-readable mirror of `docs/workflow-guide.md` §6 (the
   ADR-040 carry-forward unit); `schemas/receipt.v1.yaml` is the receipt
   shape. Each file is self-describing (`schema`, `version`, `unit`,
   `item.required`, per-field `type`/`pattern`/`enum`,
   `additionalFields`). Versioned filenames; a breaking change adds
   `.v2.yaml` rather than editing v1 in place. The prose home and the file
   must agree, and §6 remains the human spec.

2. **`bin/validate-carry-forward`** (standard envelope; exit 0/1/2). It
   reads the required fields, the `target-issue` pattern, and the
   extra-field policy *from* `schemas/design-questions.v1.yaml` — there is
   no second copy of the rules — and validates `### design-questions`
   blocks in eval notes. `--against` traces a producer file's
   target-issues into a PR body or prompt, failing when carry-forward is
   not preserved.

3. **Idempotency receipts** for mutating skills, specified in
   `docs/receipts.md` and `schemas/receipt.v1.yaml`. A receipt is a JSON
   file under `.claude/receipts/<skill>__<key>.json` capturing skill,
   key, status, timestamp, inputs, outputs, and next-action. The
   convention is the **file**; `bin/write-receipt` is the deterministic
   reference writer/reader (`--find`), not a dependency — a target project
   without the helper writes the same file directly. The cat-2/cat-3
   mutating skills (`claude-issue-executor`, `pr-review-packager`,
   `issue-planner`, `complete-milestone`, `release`) cross-reference the
   convention; cat-1 file-writing skills do not (their outputs are already
   idempotent).

4. **`bin/check-consistency`** (standard envelope; exit 0/1/2) — the
   doc↔metadata umbrella checker complementing `validate-kit-json`. It
   verifies `docs/skills.md` ↔ `kit.json`, the verb layer ↔ the index, the
   `bin` registry (registered paths exist and are executable; every
   standard-envelope script is registered), schema-file references, and
   the permission-category legend.

5. **`bin/self-test`** (standard envelope; exit 0/1/2) plus
   `docs/self-test.md` and `notes/self-test-log.md`. The script runs the
   non-mutating validation surface against the kit and a throwaway stub
   (which also regression-tests the carry-forward validator and receipt
   logic), timing it and listing friction. The manual protocol measures
   the full idea→first-PR time; recent results are summarised in release
   notes.

The standard-envelope validators and the self-test are wired into CI at
`.github/workflows/kit-checks.yml`, satisfying ADR-047's deferred CI
wiring. All new scripts use the ADR-047 envelope and exit codes; none add
a runtime dependency or change the installer.

## Consequences

- Easier: carry-forward, doc/metadata, and schema drift are now caught by
  machine checks and a CI gate rather than PR review alone; a resuming
  agent can read receipts to avoid duplicating a hard-to-reverse mutation;
  the kit can show, release over release, that its time-to-first-PR
  friction is tracked.
- Harder: four new `bin/*` scripts and a `schemas/` directory are new
  surface to maintain; the carry-forward schema lives in prose (§6) and a
  file that must agree — `check-consistency` makes that drift loud, and the
  validator reads the file so there is no third copy.
- Maintain: a schema change updates §6 first, then its `.yaml` mirror, then
  the three SKILL.md cross-references, in lockstep; new standard-envelope
  `bin/*` scripts must be registered in `kit.json` (or `check-consistency`
  fails); `docs/receipts.md` is the canonical receipt convention any new
  mutating skill follows.
- Deferred (recorded, not opened): shipping `write-receipt` and the
  validators into target projects via the installer (this iteration keeps
  them kit-level, as ADR-047 did for `kit.json`, to avoid an
  installer-behaviour change); extending receipts to cat-1 skills;
  re-aligning the legacy `bin/check-plan` envelope; and growing the
  carry-forward validator into a structural plan-checker rule
  ([ADR-034](adr-034-plan-checker.md)). These are non-blocking follow-ups.
