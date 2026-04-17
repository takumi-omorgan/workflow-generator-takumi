
# ADR-008: Dedicated prompts/ folder for issue session briefs

**Status:** accepted
**Date:** 2026-04-17

## Context

Filled issue prompts (`issue-N-prompt.md`) currently live in `notes/` alongside freeform working notes. These prompts are structured session briefs — they follow a consistent format and serve a different purpose from ad-hoc notes. Mixing the two makes it harder to find the right prompt when starting an issue session and harder to enforce naming conventions. This change affects the target project layout defined in ADR-001 and ADR-005.

## Options considered

### Option A: prompts/ at project root

- Pros: top-level visibility, easy to reference from CLAUDE.md and issue branches, clear separation from notes.
- Cons: adds another root directory.

### Option B: Design/prompts/

- Pros: groups all design-time artifacts together.
- Cons: prompts are operational, not design artifacts; nesting adds friction.

### Option C: notes/prompts/ subfolder

- Pros: minimal change, keeps everything under notes/.
- Cons: still mixed with freeform files at the parent level, easy to overlook.

## Decision

Use **`prompts/` at the project root** with the naming convention `issue-NNN-short-title.md`. A blank template lives at `prompts/_template.md` so new prompts stay consistent. The `notes/` directory remains available for freeform working notes that are not tied to a specific issue session.

## Consequences

- Issue session briefs have a predictable, discoverable location.
- Naming convention makes it trivial to match a prompt to its GitHub issue.
- The template enforces structure without requiring a skill to generate it.
- `notes/` is simplified to truly freeform content.
- References: ADR-001 (project-local model), ADR-005 (target repo structure).
