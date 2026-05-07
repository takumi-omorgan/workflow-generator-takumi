# ADR-002: Handling of non-ASCII input

**Status:** accepted
**Date:** 2026-03-12

## Context

The MVP (`design/mvp.md`) says non-ASCII characters are
transliterated where a single obvious mapping exists and dropped
otherwise. We need to decide *how* that transliteration is
implemented, because the choice drives bundle size and predictability
— both of which are explicit product principles.

## Options considered

### Option A: Built-in Latin-1 table only

A hand-maintained map from Latin-1 accented characters to ASCII
letters (é → e, ü → u, ñ → n, …). Anything outside Latin-1 is
dropped.

- Pros: tiny (≈120 entries); deterministic; zero dependencies; keeps
  the library under the 200-line goal from the PRD.
- Cons: users with, say, Cyrillic input get empty-ish slugs. Some
  will be surprised.

### Option B: Unicode normalization (NFD) + strip combining marks

Use the built-in `String.prototype.normalize("NFD")` to decompose
accented characters, then strip combining marks via regex.

- Pros: no table to maintain; handles a wider range of diacritics
  automatically.
- Cons: only works for characters that decompose into
  base + combining mark. "ß" → "ss" and "æ" → "ae" still need
  explicit mappings. Ends up being both the table *and* the
  normalization step.

### Option C: Pull in a transliteration library (`transliteration`, `unidecode`)

- Pros: handles Cyrillic, Greek, CJK, etc. out of the box.
- Cons: adds a runtime dependency — directly violates MVP principle
  #3 ("zero runtime dependencies, ever"). Adds 50–200kB of Unicode
  tables to consumer bundles.

## Decision

Go with **Option A**. The MVP explicitly lists "no non-Latin
transliteration strategies" as a non-goal, so choosing the approach
that scales to Cyrillic would pay a cost we don't want. The
hand-maintained Latin-1 table fits in roughly 40 lines, stays under
the 200-line total goal, and is easy to audit in review. Characters
outside the table are dropped silently — this is the "predictable
non-ASCII behaviour beats clever non-ASCII behaviour" principle.

## Consequences

- `slugify("Café")` → `"cafe"`, `slugify("日本語")` → `""`. The
  second result is surprising if you don't read the docs — we must
  document this clearly in the README.
- Adding Cyrillic or Greek support is a one-PR extension (append to
  the table) rather than a library swap.
- We own the table. Any bug in a mapping is a bug in our code, not
  an upstream dependency's.
