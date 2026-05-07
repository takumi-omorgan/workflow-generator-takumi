# PR #1 — Load bundled shortcut data

## Summary

Adds the data-loading layer for `kb-lookup`. Bundles three starter
JSON files (VS Code, Slack, Chrome) and a small `load_app()` helper
that reads them via `importlib.resources`, following the format
agreed in ADR-001.

## Closes

Closes #1

## ADR

Related ADR: `design/adr/adr-001-shortcut-data-format.md`

## Changes

- New package `kb_lookup/` with `loader.py` and `data/*.json`.
- `UnknownAppError` exposed from `kb_lookup.errors`; its message
  lists bundled apps so callers can surface it verbatim.
- Unit tests covering the happy path and the unknown-app error.

Reference sketch of the loader (20 lines — not the full file):

```python
from importlib.resources import files
import json

class UnknownAppError(KeyError):
    def __init__(self, name, known):
        self._name, self._known = name, sorted(known)
        super().__init__(name)
    def __str__(self):
        return f"unknown app {self._name!r}; known: {', '.join(self._known)}"

_BUNDLED = {"vscode", "slack", "chrome"}

def load_app(name: str) -> dict:
    if name not in _BUNDLED:
        raise UnknownAppError(name, _BUNDLED)
    path = files("kb_lookup.data").joinpath(f"{name}.json")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)
```

## Test results

```
pytest: 6 passed, 0 failed, 0 skipped
```

## Manual verification

```bash
python -c "from kb_lookup.loader import load_app; print(load_app('slack'))"
# → prints the Slack shortcut table as a dict
python -c "from kb_lookup.loader import load_app; load_app('notion')"
# → raises UnknownAppError with the three bundled app names listed
```
