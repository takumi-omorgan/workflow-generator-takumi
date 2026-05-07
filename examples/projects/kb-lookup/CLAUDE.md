# kb-lookup

## What this is

A single-command CLI that prints the keyboard shortcut for a named
action in a named app, offline. Bundled data covers three apps:
VS Code, Slack, and Chrome.

## Technology stack

- Runtime / language: Python 3.10+
- Framework: none (argparse, importlib.resources)
- Database / storage: bundled JSON in `kb_lookup/data/`
- Key libraries: standard library only

## Conventions

- Module system: Python package under `kb_lookup/`
- Code style: `ruff` + `black`; line length 100
- Dependency policy: stdlib only for runtime; dev deps pinned in `pyproject.toml`
- Secret management: N/A — no network calls
- Commit style: plain prose, reference ADR and issue numbers

## Project structure

```
kb-lookup/
  kb_lookup/            # package source
    cli.py              # argparse entry point
    loader.py           # reads JSON shortcut data
    platform.py         # renders modifier keys per OS
    data/               # bundled shortcut JSON, one file per app
  tests/                # pytest suite mirroring kb_lookup/
  design/               # PRD, MVP, ADRs
  pyproject.toml
```

See also: `design/` for ADRs, `notes/` for per-issue prompts.

## How to run

```bash
pip install -e .
kb slack "new message"
```

## Testing

- Framework: pytest
- Location: `tests/` mirroring `kb_lookup/`
- Run: `pytest`
- Coverage expectations: new modules ship with tests for happy path,
  error path, and any platform-specific branch.

## Review expectations

- Every change lands via PR linked to a GitHub issue.
- Plan-first execution: propose a plan, wait for approval, then implement.
- Commit messages reference the ADR and issue (e.g. `Add loader (ADR-001, #1)`).
- Existing tests must continue to pass on every PR.

## Current phase

M1 — core loader and CLI. Once the two M1 issues ship, the next
phase is "M2 — packaging" (PyPI publish workflow).
