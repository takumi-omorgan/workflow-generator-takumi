
# ADR-007: Provide a CLAUDE.md starter template with placeholders

**Status:** accepted
**Date:** 2026-04-17

## Context

New projects need a `CLAUDE.md` file to give Claude Code the context it needs to work effectively. Currently users hand-write this file from scratch, which is slow and inconsistent. `docs/install.md:102` notes that a proper template will be added in Issue #4. The template should include placeholders for project name, stack, workflow rules, and GitHub conventions so that setup becomes a fill-in-the-blanks exercise rather than a blank-page problem.

## Options considered

### Option A: Static template with {{placeholders}}

- Pros: simple to ship, consistent with the existing template pattern in `templates/`, easy to render with sed or envsubst.
- Cons: no interactivity; the user must find and replace every placeholder manually.

### Option B: Interactive skill that prompts the user

- Pros: guided experience, fewer missed fields.
- Cons: adds complexity, requires a new skill before the rest of the kit is stable.

### Option C: Adopt a community CLAUDE.md template

- Pros: benefits from wider community iteration.
- Cons: may not align with the kit's opinionated workflow structure or ADR conventions.

## Decision

Ship a **static template** at `templates/CLAUDE.md` with `{{placeholder}}` tokens. This is the simplest option and aligns with the existing template pattern used elsewhere in the kit (see ADR-005). The installer script (ADR-009, when built) will render the template automatically; until then, users copy and fill it in by hand.

## Consequences

- Users get a consistent starting point for every new project.
- The template becomes the single source of truth for what belongs in `CLAUDE.md`.
- An interactive skill can be layered on later without changing the underlying template.
- References: ADR-005 (generate docs into target repo).
