
# ADR-002: Limit v1 to new-project setup only

**Status:** superseded by [ADR-022](adr-022-drop-version-qualifiers-from-kit-scope.md)
**Date:** 2026-04-12

> **Note (2026-04-26):** Superseded by ADR-022 to drop the "v1"
> qualifier from kit-scope language. The substantive decision is
> unchanged: the kit is scoped to new projects only. Per project rule,
> the original text below is preserved as the historical record.

## Context

The workflow kit is intended to create a disciplined software-delivery workflow at project bootstrap. Existing repositories often have inconsistent documentation, unclear conventions, partial GitHub workflow setup, and no decision history. Supporting migration of those repos in v1 would introduce major ambiguity about what the kit should preserve, replace, infer, or ignore.

## Options considered

### Option A: Support both new and existing projects in v1

- Pros: broader applicability, more users could adopt it immediately.
- Cons: much higher complexity, ambiguous migration behavior, harder documentation, and less predictable outputs.

### Option B: Support new projects only in v1

- Pros: clear scope, easier documentation, fewer edge cases, and stronger workflow consistency from the start.
- Cons: excludes teams that want to retrofit an existing codebase.

## Decision

Scope v1 to **new projects only**. The kit will be designed to establish the workflow before or at the very start of implementation.

## Consequences

- The docs can be written clearly and decisively.
- Skills do not need migration logic.
- The workflow can assume clean setup, fresh docs, and consistent conventions.
- Existing-project adaptation may be revisited in a later phase.
