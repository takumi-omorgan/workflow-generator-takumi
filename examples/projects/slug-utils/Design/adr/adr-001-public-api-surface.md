# ADR-001: Public API surface

**Status:** accepted
**Date:** 2026-03-12

## Context

The MVP (`Design/mvp.md`) commits to "two functions, two signatures
— nothing else exported". We still need to decide what those two
signatures look like, because the choice is expensive to reverse
once consumers start importing the library. The PRD
(`Design/prd.md`) rules out an options object, which narrows the
design space but still leaves two reasonable shapes.

## Options considered

### Option A: Pure string-in, string-out

```ts
export function slugify(input: string): string;
export function unslugify(slug: string): string;
```

- Pros: simplest possible signatures; no decisions to make at call
  sites; consistent with MVP principle #1.
- Cons: zero room to grow — adding any behaviour later means
  breaking the signature.

### Option B: String input, optional options object

```ts
export function slugify(input: string, options?: SlugifyOptions): string;
```

- Pros: leaves a growth path for features we might want later
  (separators, casing).
- Cons: directly contradicts MVP scope ("No configuration object
  'just in case'"). Invites future scope creep into the initial release.

## Decision

Go with **Option A**. The MVP explicitly forbids an options object
and commits to predictable behaviour. If a real user later needs
configuration, we add it behind a new exported function
(`slugifyWith(options)`) rather than mutating the existing
signature. That keeps the "two functions" guarantee of the initial
release intact for anyone who imported it early.

## Consequences

- The library has a bright line between the initial release (string
  in, string out) and any future extension (separate function).
- Readers of the source can trace the entire control flow from two
  fixed entry points.
- Changing the separator or casing later requires a new exported
  function, not a patched signature — slightly more work, but
  non-breaking.
