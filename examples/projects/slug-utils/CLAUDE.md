# slug-utils

## What this is

A zero-dependency TypeScript library that exports two functions:
`slugify` (string → URL slug) and `unslugify` (slug → readable
string). Published as ESM with bundled type declarations.

## Technology stack

- Runtime / language: TypeScript 5+, ESM
- Framework: none
- Database / storage: none
- Key libraries: none at runtime; `vitest` and `tsup` as dev deps

## Conventions

- Module system: ESM only
- Code style: `prettier` default + `eslint:recommended`
- Dependency policy: zero runtime deps. Dev deps pinned in
  `package.json` and reviewed on every PR.
- Secret management: N/A
- Commit style: plain prose, reference ADR and issue numbers

## Project structure

```
slug-utils/
  src/
    index.ts              # slugify + unslugify exports
    transliterate.ts      # Latin-1 → ASCII map
  tests/                  # vitest suite mirroring src/
  design/                 # PRD, MVP, ADRs
  package.json
  tsup.config.ts
```

See also: `design/` for ADRs, `notes/` for per-issue prompts.

## How to run

```bash
npm install
npm test
npm run build
```

## Testing

- Framework: vitest
- Location: `tests/` mirroring `src/`
- Run: `npm test`
- Coverage expectations: any exported function must have tests for
  happy path, empty input, and the behaviour called out in its ADR.

## Review expectations

- Every change lands via PR linked to a GitHub issue.
- Plan-first execution: propose a plan, wait for approval, then implement.
- Commit messages reference the ADR and issue.
- Existing tests must continue to pass on every PR.
- Any change to `src/transliterate.ts` counts as an API-visible change
  and needs reviewer sign-off.

## Current phase

M1 — public API. After the two M1 issues ship, the next milestone
is "M2 — release" (cut 0.1.0 and publish).
