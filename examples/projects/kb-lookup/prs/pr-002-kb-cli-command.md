# PR #2 — `kb` CLI command

## Summary

Wires up the `kb` command on top of the loader from #1. Supports the
two MVP shapes — `kb <app>` for all shortcuts and `kb <app> <action>`
for one — and renders modifier keys per platform.

## Closes

Closes #2

## ADR

Related ADR: `design/adr/adr-001-shortcut-data-format.md`

## Changes

- New `kb_lookup/cli.py` exposing `main()`.
- `kb` entry point declared in `pyproject.toml`.
- Platform detection in `kb_lookup/platform.py` — one function,
  `render(shortcut, platform)`, kept separate from the CLI so it is
  unit-testable without subprocess.
- Error messages for unknown action mirror the unknown-app style
  introduced in #1: they list valid actions.

## Test results

```
pytest: 14 passed, 0 failed, 0 skipped
```

## Manual verification

```bash
kb slack
# → prints every Slack shortcut, one per line, ⌘ on macOS.
kb slack "new message"
# → prints one line: ⌘N   (macOS) or Ctrl+N (Linux).
kb slack frobnicate
# → exits 1, prints: unknown action 'frobnicate'; known: ...
```
