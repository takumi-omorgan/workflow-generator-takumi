# Issue #2 — `kb` CLI command

## Summary

Wire up the `kb` command that the end user actually runs. It takes
an app name and an optional action, looks up the shortcut via the
loader from #1, and prints a platform-correct result to stdout.

## ADR

Related ADR: `design/adr/adr-001-shortcut-data-format.md`
<!-- ADR-001 governs the data shape this command reads. No new ADR is needed for the CLI surface. -->

## Goal

Ship the first end-user-visible feature: `kb <app> [<action>]` that
prints one or more shortcuts, with modifier keys rendered per the
host platform.

## Why it matters

This is the MVP's headline capability (see `design/mvp.md` → "MVP
scope → In scope"). Without it, the loader from #1 has no user.

## Tasks

- [ ] Add a `kb` entry point in `pyproject.toml`.
- [ ] Implement `kb_lookup.cli:main` using `argparse`:
  - `kb <app>` prints all shortcuts for that app.
  - `kb <app> <action>` prints the one shortcut (or a clear error).
- [ ] Detect platform (`sys.platform`) and pick the `mac` vs.
  `other` field from each action.
- [ ] Error messages for unknown app and unknown action follow the
  pattern set in #1.
- [ ] End-to-end test using `subprocess` for one happy path and one
  error path.

## Acceptance criteria

- `kb slack` prints every Slack shortcut, one per line.
- `kb slack "new message"` prints a single shortcut line.
- `kb slack frobnicate` exits non-zero and prints an error that
  names valid actions.
- Output on macOS uses ⌘/⌥/⇧; on Linux it uses Ctrl/Alt/Shift.

## Notes

Labels: `feature`, `cli`
Milestone: `M1 — core loader`
Depends on: #1
