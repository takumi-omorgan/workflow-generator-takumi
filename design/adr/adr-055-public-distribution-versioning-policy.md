# ADR-055: Public distribution versioning and changelog policy

**Status:** accepted
**Date:** 2026-06-10

## Context

The kit is preparing its first public distribution as a separate repo
(`olivermorgan2/claude-workflow-kit`), produced by a deterministic export from
this source repo. That model and its export mechanics are designed in
[`design/public-distribution-export-design-20260609.md`](../public-distribution-export-design-20260609.md);
the export tooling and the broader two-repo export-model ADR are tracked under
issue #16 and are **not** decided here.

Before any export tooling lands, the **version** and **changelog** policy must be
settled, because the export refuses to run on contradictory version state and the
first public release must not force an early corrective patch. The current state
is a three-way drift:

- `kit.json` `kitVersion` is `4.1.0` — the unreleased development head.
- The latest internal tag is `v4.0.0`.
- `README.md` and `docs/install.md` still pin `v3.3.0` in install commands.

Internal release history already spans `v1.0.0`…`v4.0.0`. This ADR extends the
kit's semver definition in [ADR-026](adr-026-kit-versioning-policy.md) to the
public-distribution dimension; it does not change what counts as a breaking
change.

## Options considered

### Initial public version

- **Option A — debut the public repo at a fresh `v1.0.0` (or `v0.1.0`).**
  - Pros: a clean "1.0" public story.
  - Cons: creates a second version namespace that collides with the existing
    `v1.0.0`…`v4.0.0` internal tag history, and reintroduces exactly the
    version-drift this policy exists to remove. Two sources of truth.
- **Option B — align the public version to `kit.json` `kitVersion`.**
  - Pros: one version line; the export's version-pin gate has an unambiguous
    canonical value to check; no second source of truth.
  - Cons: the public repo "starts" at `4.x` with no public `1.x`–`3.x` history,
    which needs a one-line explanation in public docs.

### Public changelog source

- **Option A — ship the existing internal `CHANGELOG.md` verbatim.**
  - Pros: zero work.
  - Cons: publishes ~20 KB of internal issue/ADR churn with no public meaning,
    and leaks internal references the export otherwise scrubs.
- **Option B — curated public changelog generated from tagged releases.**
  - Pros: public-meaningful entries only; absorbs the internal-ADR churn during
    generation; consistent with the export's name/version transforms.
  - Cons: one generation step at release time.

## Decision

1. **Initial public version — Option B (align to `kit.json`).** The single
   source of truth for the kit version is `kit.json` `kitVersion`. The published
   release tag must equal it (`vX.Y.Z` == `kitVersion`). The first public tag is
   the current `kitVersion` at export time (`v4.1.0` today), **not** a fresh
   `v1.0.0`.

2. **Source → public version mapping.** There is exactly one version line.
   Public releases carry the same semver as the source `kitVersion` at the moment
   of export. The kit does **not** maintain divergent public/private version
   numbers.

3. **Public changelog — Option B (curated, generated from releases).** The public
   changelog is generated from tagged releases with the export's name/version
   transforms applied; internal-only breadcrumbs (per-issue/ADR churn with no
   public meaning) are dropped. The raw internal `CHANGELOG.md` is not shipped
   verbatim. The public changelog begins at the first public release; private
   development history is not reproduced publicly.

4. **Public history model.** The public distribution ships `docs/architecture.md`
   as the single current architecture statement (per
   [ADR-053](adr-053-workflow-docs-architecture-document.md)). Detailed ADR
   decision history stays internal and is not shipped by default; public docs must
   not imply the full ADR set is published. The prose/link neutralization that
   makes shipping docs consistent with this is implemented under issue #16, not
   here.

5. **Tag flow.** The source repo is tagged first via the existing `/release`
   flow. The public repo's tag is produced from the **verified export** after
   `bin/export-public` passes its gates — it is not tagged independently. The
   export refuses to run when the requested tag ≠ `kit.json` `kitVersion`, making
   that equality a machine-enforced invariant. The enforcement is implemented
   under issue #16; this ADR sets the policy it enforces.

## Consequences

- One version source of truth (`kit.json` `kitVersion`); the export's version-pin
  gate has an unambiguous canonical value, and the first public release cannot
  silently debut at the wrong number.
- Every hardcoded version literal in shipping docs (`README.md`,
  `docs/install.md`, the `bootstrap` default) must track `kitVersion`. Correcting
  the current stale `v3.3.0` pins to the canonical version is tracked under issue
  #16 (the source-neutralization sweep), not this ADR.
- Maintainers bump `kit.json` `kitVersion` as the one place a version lives; the
  public changelog is generated, never hand-copied from the internal one.
- Out of scope / deferred: the export tooling (`bin/export-public`, leak/link
  gates) and the two-repo export-model ADR (issue #16); the publish runbook and
  the `gh`-identity switch (a later sequence). This ADR settles **policy** only.

**ADR-number note.** The export design draft reserved "ADR-053" for the export
model, but `053` was assigned to the architecture-document decision. This
versioning/changelog policy is **ADR-055**; the two-repo export-model decision
will be filed when issue #16 lands.
