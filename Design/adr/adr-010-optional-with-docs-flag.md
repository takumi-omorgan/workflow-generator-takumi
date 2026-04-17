
# ADR-010: Optional --with-docs flag on install

**Status:** proposed
**Date:** 2026-04-17

## Context

The workflow kit ships reference documentation in `docs/` that explains the workflow model, skills, and conventions. Some users want these docs available locally in their target project for quick reference; others prefer to keep the target repo lean and read docs in the kit repository. This is an extension of the installer script defined in ADR-009.

## Options considered

### Option A: Opt-in flag, default off

- Pros: keeps the default install minimal, gives users a clear choice.
- Cons: users who would benefit from local docs may not discover the flag.

### Option B: Always copy docs

- Pros: every project is self-contained.
- Cons: adds files most users won't read locally, clutters the repo.

### Option C: Never copy docs (current behavior)

- Pros: simplest.
- Cons: no path to local docs without manual copying.

## Decision

Add an **opt-in `--with-docs` flag** to `bin/install-workflow-kit`. When passed, the script copies the kit's reference docs into `docs/workflow-kit/` in the target project. The `workflow-kit/` namespace avoids collisions with any project-specific docs the user creates in `docs/`.

## Consequences

- The default install stays lightweight.
- Users who want local docs get them in a predictable, namespaced location.
- The installer script gains one additional flag but no change to its default behavior.
- References: ADR-009 (installer script).
