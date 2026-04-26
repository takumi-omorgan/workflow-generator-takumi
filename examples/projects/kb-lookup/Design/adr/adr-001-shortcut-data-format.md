# ADR-001: Shortcut data format and location

**Status:** accepted
**Date:** 2026-02-06

## Context

The MVP (`Design/mvp.md`) requires bundled shortcut data for three
apps, with platform-aware rendering. We need a format that is easy
to author by hand, easy to parse at runtime, and easy to extend when
a fourth app is added. The PRD (`Design/prd.md`) also constrains us
to offline operation, so remote lookups are off the table.

## Options considered

### Option A: One JSON file per app, bundled as package data

- Pros: trivial to parse with the standard library; diff-friendly;
  one file per app keeps PRs small when adding an app.
- Cons: JSON has no comments, so we lose the ability to annotate why
  a shortcut differs across platforms.

### Option B: One YAML file per app

- Pros: supports comments; nicer for hand-authoring.
- Cons: adds a runtime dependency (`PyYAML`) for a tool whose only
  other dependency is the standard library. Violates the "small
  install footprint" spirit of the MVP.

### Option C: Inline Python dicts in a `data.py` module

- Pros: zero parsing cost; IDE completion when editing.
- Cons: mixing data and code discourages community contributions later
  and makes automated validation harder.

## Decision

Go with **Option A**: one JSON file per app, stored under
`kb_lookup/data/<app>.json` and loaded via `importlib.resources`.
Comments-in-data are a "nice to have" not worth a runtime dependency
in scope. The per-app file layout also keeps future app-additions to
small, reviewable PRs — consistent with the MVP's "bundled data beats
user-supplied data" principle.

## Consequences

- The loader is trivial: one stdlib import, no third-party parser.
- Platform-specific overrides are expressed as fields inside each
  action entry (e.g. `{"mac": "Cmd+K", "other": "Ctrl+K"}`), not as
  separate files.
- Adding a fourth app is a one-file PR — good for contribution flow
  if we ever open this up.
- Validation of the bundled data is now a worthwhile thing to add
  later; a malformed JSON file would crash the CLI at lookup time.
