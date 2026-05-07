# slug-utils — PRD

**Last updated:** 2026-03-10

## Problem

Every TypeScript project I start needs the same two slug helpers:
"turn a title into a URL slug" and "turn a slug back into a readable
string for breadcrumbs". The existing npm packages either bundle
dozens of helpers I don't need, pull in Unicode tables that balloon
bundle size, or handle non-ASCII poorly. I want a tiny library that
does exactly two things well.

## Goals

- Two exported functions: `slugify(input)` and `unslugify(slug)`.
- Round-trip stability: `unslugify(slugify(x))` gives a readable
  string, not necessarily `x` byte-for-byte.
- Strict ASCII output by default. Non-ASCII characters are
  transliterated where a single obvious mapping exists and dropped
  otherwise.
- Zero runtime dependencies.
- Ships as ESM with a `.d.ts` file.

## Non-goals

- No i18n-specific slug strategies (e.g. pinyin for Chinese). That's
  a whole different library.
- No framework-specific wrappers (React hooks, etc.).
- No configuration object "just in case". One function, one
  signature, one behaviour.
- No performance commitments.

## Target user

A TypeScript or JavaScript developer building a small web app who
needs slugs for routing and wants to add a dependency they can read
in one sitting.

## Success criteria

- `npm install slug-utils` and import works in a fresh Vite project
  with no additional config.
- The full library is under 200 lines of source (excluding tests).
- A developer can read the source and understand every line in under
  10 minutes.

## Constraints and preferences

- TypeScript 5+ target, ESM-only.
- No runtime deps. Dev deps only for tests and build.
- Published to npm under an unscoped name if available.
