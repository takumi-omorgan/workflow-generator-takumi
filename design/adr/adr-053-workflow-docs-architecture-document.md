# ADR-053: Maintain a current architecture document via workflow-docs

**Status:** accepted
**Date:** 2026-06-09

## Context

The kit already records decision history through ADRs and generates a compact
AI-readable project summary through `/workflow-docs`. That leaves a gap: users
need one current, human-readable architecture reference that says how the
project is shaped today. ADRs explain why decisions were made, but they are not
a good current-state architecture document once a project has evolved through
several issues, pivots, and superseded choices.

The public distribution of the kit also needs a concise architecture document
for the kit itself without publishing the full internal ADR history.

## Options considered

### Option A: Keep using ADRs as the architecture reference

- Pros: no new artifact.
- Cons: mixes current state with history, exposes stale/superseded context, and
  makes target projects harder for new humans and agents to understand.

### Option B: Add a current architecture document maintained by `/workflow-docs`

- Pros: gives every target project a stable `design/architecture.md`; keeps ADRs
  as rationale; can be refreshed continuously after meaningful changes and
  before releases; aligns with the public kit architecture doc.
- Cons: one more generated artifact to keep in sync and one more template to
  ship.

## Decision

Adopt Option B. `/workflow-docs` generates and refreshes three marker-fenced
outputs: `README.md`, `design/architecture.md`, and `design/ai-summary.md`. The
new `design/architecture.md` is the current human-readable system/design
reference for a target project. `design/adr/` remains the decision-history and
rationale store. The kit repository maintains its own public architecture
reference at `docs/architecture.md`.

## Consequences

- The installer must ship `templates/architecture-template.md` as a runtime
  template.
- `kit.json`, `workflow-docs` frontmatter, docs, and examples must list the new
  output.
- Target-project `CLAUDE.md` should tell agents to refresh architecture docs
  after meaningful architecture changes.
- Existing ADRs remain immutable; this ADR extends ADR-018 rather than editing
  it in place.
