# `schemas/` — canonical machine-readable schemas

This directory holds the kit's **canonical, machine-readable schemas**:
one structured file per shared data shape that more than one skill,
script, or document depends on. Each file is the single source of truth
for the *fields and constraints* of its shape; the prose that explains
*when and why* to use the shape lives in a doc that the schema file
cross-references (and vice versa).

The split mirrors the rest of the agent contract
([`docs/agent-contract.md`](../docs/agent-contract.md)): structured data
for machines, prose for humans, and a checker that fails when the two
drift.

## Schemas

| File | Shape | Prose home | Validated by |
|---|---|---|---|
| [`design-questions.v1.yaml`](design-questions.v1.yaml) | Cross-skill design-question carry-forward entry (ADR-040) | [`docs/workflow-guide.md` §6](../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040) | [`bin/validate-carry-forward`](../bin/validate-carry-forward) |
| [`receipt.v1.yaml`](receipt.v1.yaml) | Idempotency receipt for a mutating skill (ADR-050) | [`docs/receipts.md`](../docs/receipts.md) | [`bin/write-receipt`](../bin/write-receipt) |
| [`ai-review-config.v1.yaml`](ai-review-config.v1.yaml) | Provider configuration for AI PR review (ADR-051) | [`docs/ai-review.md`](../docs/ai-review.md) | [`bin/review-pr`](../bin/review-pr) |
| [`ai-review-artifact.v1.yaml`](ai-review-artifact.v1.yaml) | AI PR review artifact / finding shape (ADR-051) | [`docs/ai-review.md`](../docs/ai-review.md) | [`bin/review-pr`](../bin/review-pr), [`bin/publish-review`](../bin/publish-review) |

## Conventions

- **Versioned filenames.** `<name>.v<N>.yaml`. A breaking change to a
  shape adds a `.v2.yaml` beside the v1 file rather than editing v1 in
  place, the same way the kit supersedes ADRs rather than rewriting them.
  The `version:` field inside the file matches the filename.
- **Self-describing.** Each file declares `schema`, `version`, the
  `unit` (whether the data is a single object or a list of items), and an
  `item:` block listing `required` fields, per-field `type`/`pattern`/
  `enum`, and whether extra fields are allowed (`additionalFields`).
- **Read by the validators.** The validators load these constraints from
  the schema file rather than hard-coding them, so changing a schema
  changes what is enforced — there is no second copy of the rules in a
  script.
- **No new runtime dependency.** Files are plain YAML read with the
  `python3` already used across `bin/`; the kit does not pull in a
  JSON-Schema library (consistent with the "no speculative abstractions"
  rule in [`CLAUDE.md`](../CLAUDE.md)).

These files are kit-level. They are not copied into target projects by
the installer in this iteration (the same posture as `kit.json`); a
target-project agent follows the per-skill cross-references instead.
