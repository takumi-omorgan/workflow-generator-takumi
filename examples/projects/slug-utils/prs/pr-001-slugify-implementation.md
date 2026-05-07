# PR #1 — Implement `slugify`

## Summary

Implements the first half of the public API. `slugify` lowercases
input, transliterates Latin-1 accented characters using the hand-
maintained table from ADR-002, drops everything else, and
hyphen-joins the remaining tokens.

## Closes

Closes #1

## ADR

Related ADRs:
- `design/adr/adr-001-public-api-surface.md`
- `design/adr/adr-002-unicode-handling.md`

## Changes

- New `src/transliterate.ts` — one `Map<string, string>` covering
  Latin-1 accented characters and a handful of ligatures (æ, œ, ß).
- New `src/index.ts` — the `slugify` function, 18 lines including
  the export.
- Test suite `tests/slugify.test.ts` with the five cases listed in
  the issue plus two regressions.
- README updated with the "characters outside the table are dropped
  silently" note — a consequence recorded in ADR-002.

Reference sketch of `slugify` (23 lines):

```ts
import { TRANSLITERATE } from "./transliterate.js";

const NON_ASCII = /[^\x00-\x7F]/g;
const NON_WORD = /[^a-z0-9]+/g;

export function slugify(input: string): string {
  const transliterated = input
    .toLowerCase()
    .replace(NON_ASCII, (ch) => TRANSLITERATE.get(ch) ?? "");
  return transliterated
    .replace(NON_WORD, "-")
    .replace(/^-+|-+$/g, "");
}
```

## Test results

```
vitest: 12 passed, 0 failed
```

## Manual verification

None needed — the behaviour is fully covered by the test suite.
