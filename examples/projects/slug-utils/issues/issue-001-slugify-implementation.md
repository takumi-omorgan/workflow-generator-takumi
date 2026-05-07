# Issue #1 — Implement `slugify`

## Summary

Implement the `slugify` function and its transliteration table per
ADR-001 (API shape) and ADR-002 (Unicode handling). This issue
ships half the public API and all of the transliteration logic.

## ADR

Related ADRs:
- `design/adr/adr-001-public-api-surface.md`
- `design/adr/adr-002-unicode-handling.md`

## Goal

A working `slugify(input: string): string` that produces lowercase,
hyphen-separated ASCII slugs per the MVP's success criteria, with
predictable drop-on-miss behaviour for out-of-table Unicode.

## Why it matters

Every consumer of this library will call `slugify` first. Getting
its shape and Unicode behaviour right now is cheaper than changing
it after the first release.

## Tasks

- [ ] Implement the Latin-1 transliteration table in a separate
  module (`src/transliterate.ts`) so ADR-002's scope is easy to
  audit.
- [ ] Implement `slugify` in `src/index.ts` exporting the signature
  from ADR-001.
- [ ] Tests: ASCII happy path, accented input, mixed punctuation,
  empty string, all-non-Latin input.
- [ ] Document the "characters outside the table are dropped" rule
  in the README.

## Acceptance criteria

- `slugify("Hello, World!")` returns `"hello-world"`.
- `slugify("Café Déjà Vu")` returns `"cafe-deja-vu"`.
- `slugify("日本語")` returns `""`.
- `slugify("  --leading and trailing-- ")` returns
  `"leading-and-trailing"`.
- All tests pass under `vitest`.

## Notes

Labels: `feature`, `core-api`
Milestone: `M1 — public API`
