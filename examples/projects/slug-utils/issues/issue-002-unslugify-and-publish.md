# Issue #2 — Implement `unslugify` and prepare for publish

## Summary

Implement the second half of the public API — `unslugify` — and set
up the build/publish pipeline so the package is ready to ship to
npm. No actual release in this issue; the release tag is a separate
manual step.

## ADR

Related ADR: `Design/adr/adr-001-public-api-surface.md`

## Goal

Finish the in-scope API surface and make `npm publish --dry-run` succeed
with correct `files`, `exports`, and types declarations.

## Why it matters

This closes out M1. After this issue, the library meets every MVP
success criterion and we can cut a 0.1.0 release.

## Tasks

- [ ] Implement `unslugify(slug: string): string` — replace hyphens
  with spaces, uppercase the first letter.
- [ ] Tests for `unslugify`: happy path, empty string, multi-word.
- [ ] Round-trip test: `unslugify(slugify(x))` yields a readable
  string for each of the MVP success-criteria examples.
- [ ] Configure `tsup` (or equivalent) to emit ESM + `.d.ts` from
  `src/index.ts`.
- [ ] `package.json`: set `type: "module"`, `exports`, `files`,
  `types`.
- [ ] Verify `npm publish --dry-run` succeeds.

## Acceptance criteria

- `unslugify("hello-world")` returns `"Hello world"`.
- Round-trip test passes for every MVP success-criteria example.
- `npm publish --dry-run` reports exactly the built files, the
  README, and LICENSE — nothing else.
- The built package is under 4kB unpacked.

## Notes

Labels: `feature`, `packaging`
Milestone: `M1 — public API`
Depends on: #1
