
# ADR-021: Example / starter projects gallery

**Status:** accepted
**Date:** 2026-04-17

## Context

The `examples/` directory covers three PRD intake paths but contains no full worked projects. New users lack end-to-end references showing the kit from install to shipped PR — they can read about the workflow but cannot see a concrete example of every artifact the kit produces.

## Options considered

### Option A: In-repo under examples/

- Pros: ships with the kit, always in sync with the current version, discoverable.
- Cons: adds weight to the repo, must be kept small.

### Option B: Separate companion repo

- Pros: keeps the kit repo lean.
- Cons: version drift, extra clone step, easy to forget to update.

### Option C: Curated list of external projects

- Pros: zero maintenance of example code.
- Cons: external projects may diverge from kit conventions, links rot.

## Decision

Ship 2–3 small complete projects in-repo under `examples/` (e.g., a CLI utility, a web app). Each project includes the full artifact set: PRD, MVP spec, ADRs, issues, branches, and PRs. Projects are kept intentionally small to manage repo size — the goal is to demonstrate the workflow, not to build production software.

## Consequences

- New users can study a real, complete workflow end-to-end.
- The examples must be updated when the kit's conventions change, adding a small maintenance burden.
- Aligns with documentation architecture (ADR-005) and the workflow guide (ADR-020).
