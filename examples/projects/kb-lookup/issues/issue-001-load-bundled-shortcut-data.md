# Issue #1 — Load bundled shortcut data at runtime

## Summary

Add the data-loading layer for `kb-lookup`: read per-app JSON files
bundled in the package and return them as a typed lookup structure
the CLI can query. This is the foundation issue — no CLI yet, just
the loader and its tests.

## ADR

Related ADR: `design/adr/adr-001-shortcut-data-format.md`

## Goal

Produce a `load_app(name)` function that returns the shortcut table
for a named app, or raises a clear `UnknownAppError` if the app is
not bundled.

## Why it matters

Every other feature depends on this. Until we can load data, there
is no CLI to build. ADR-001 picked JSON + `importlib.resources` so
this issue is a small, self-contained implementation of that choice.

## Tasks

- [ ] Create the `kb_lookup/data/` package directory with three
  starter JSON files: `vscode.json`, `slack.json`, `chrome.json`.
- [ ] Populate each file with 5–10 of the most common shortcuts,
  using the per-action format `{ "mac": "...", "other": "..." }`.
- [ ] Implement `kb_lookup.loader.load_app(name: str)` using
  `importlib.resources`.
- [ ] Add `UnknownAppError` with a message that lists the bundled
  apps.
- [ ] Unit tests for the happy path and the unknown-app error.

## Acceptance criteria

- `load_app("vscode")` returns a dict keyed by action name.
- `load_app("notion")` raises `UnknownAppError` and the error message
  names the three bundled apps.
- Tests pass on macOS and Linux (CI not in scope for this issue).

## Notes

Labels: `feature`, `foundation`
Milestone: `M1 — core loader`
