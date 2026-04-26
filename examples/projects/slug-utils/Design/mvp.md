# slug-utils — MVP

**Last updated:** 2026-03-11

## Product name

slug-utils

## One-line description

A zero-dependency TypeScript library that converts strings to URL
slugs and back, with predictable handling of non-ASCII input.

## Product goal

Ship a library with exactly two exported functions, `slugify` and
`unslugify`, that a reader can fully understand in ten minutes and
that a consumer can install without adding bundle weight.

## Target users

### Primary user

A TypeScript developer building a small web app who needs slugs for
routing and has no patience for large utility libraries.

## Core problem

Every alternative either (a) ships a lot of unused helpers, (b)
pulls in heavy Unicode tables, or (c) handles non-ASCII poorly with
no clear rule. Developers end up writing their own 30-line slugifier
and re-writing it every project.

## Product principles

1. Two functions, two signatures — nothing else exported.
2. Predictable non-ASCII behaviour beats clever non-ASCII behaviour.
3. Zero runtime dependencies. Ever.
4. Small enough to read end-to-end in one sitting.

## MVP scope

### In scope

- `slugify(input: string): string` — produces lowercase ASCII slugs
  with hyphen separators.
- `unslugify(slug: string): string` — produces a readable string with
  spaces and title-case first letter.
- A small built-in transliteration table covering common Latin-1
  accented characters (é → e, ü → u, …).
- Characters with no obvious ASCII mapping are dropped silently.
- A comprehensive test suite that covers the documented behaviour.

### Out of scope

- A configuration / options object on either function.
- Non-Latin transliteration strategies (pinyin, Cyrillic, Greek).
- Streaming API, async API, or any non-string input.
- A CLI wrapper.
- Performance targets or benchmarks.

## Primary outputs

One npm package, ESM + `.d.ts`, published with a single version tag.

## Success criteria

The MVP succeeds if a user can:

1. Install the package and import `slugify`/`unslugify` with no config.
2. Call `slugify("Hello, World!")` and get `"hello-world"`.
3. Call `unslugify("hello-world")` and get `"Hello world"`.
4. Call `slugify("Café Déjà Vu")` and get `"cafe-deja-vu"`.

## Deferred to later

- Configurable separators — every real consumer we've seen uses `-`.
- A `transliterate` function exported standalone — wait for a real
  use case.
- Locale-aware casing (Turkish dotted I, etc.) — material enough to
  justify its own library.

## Acceptance criteria for this document

This MVP statement is acceptable when it:

- names a clear product and user,
- lists what is in and out of scope without ambiguity,
- and can drive the build-out plan, ADRs, and issue backlog without
  further interpretation.
