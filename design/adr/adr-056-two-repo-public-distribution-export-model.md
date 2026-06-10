# ADR-056: Two-repo public distribution export model

**Status:** accepted
**Date:** 2026-06-10

## Context

The kit is preparing its first public release. The public repository
(`olivermorgan2/claude-workflow-kit`) must be a **generated, verifiable
subset** of this private source repo — not a renamed remote, a force-push, or
a hand-maintained parallel tree. The source repo holds material that must
never ship publicly: the kit's own accepted ADRs (its private decision
history), evaluation reports, roadmaps, per-issue execution prompts, working
notes, and the archive. A first public export must also not carry stale
owner/repo URLs, stale version pins, personal absolute paths, or links that
dangle into excluded internal files.

The distribution **policy** is already settled: the two-repo split and the
export contract are designed in
[`design/public-distribution-export-design-20260609.md`](../public-distribution-export-design-20260609.md),
and the versioning/changelog policy is fixed in
[ADR-055](adr-055-public-distribution-versioning-policy.md) — one version
line, `tag == kitVersion`, a curated public changelog, and
[`docs/architecture.md`](../../docs/architecture.md) (per
[ADR-053](adr-053-workflow-docs-architecture-document.md)) as the single
public architecture statement in place of the internal ADR set. What ADR-055
explicitly deferred to issue #16, and what this ADR records, is the
**export-model decision and its enforcement mechanics**: how the public
artifact is produced and proven clean before any publish.

This decision does not cover creating or pushing the public repo, switching
`gh` identity to `olivermorgan2`, or cutting a release — those are a separate,
identity-gated step and remain out of scope here.

## Options considered

### Option A: Rename / mirror the source remote, prune history later

- Pros: no tooling to build.
- Cons: internal commits and files reach the public history irreversibly;
  pruning after the fact is error-prone and cannot un-publish. No
  reproducibility, no pre-publish proof.

### Option B: Hand-maintain a separate public repo

- Pros: full control over public content.
- Cons: two trees drift; every kit change must be mirrored by hand; the most
  likely failure mode is exactly the leak/stale-reference churn this work
  exists to prevent.

### Option C: Deterministic export tool + a separate verifier, dry-runnable, no push

- Pros: the public tree is a reproducible function of tracked files at `HEAD`;
  untracked material (e.g. `.hermes/`) can never be included; the artifact is
  proven clean by a leak/link verifier and the repo validation suite *before*
  any publish; the build needs no GitHub access, so it runs in CI and locally;
  the identity-sensitive publish stays a separate, gated step.
- Cons: more `bin/` surface to register, test, and keep green.

## Decision

Adopt **Option C**. The public distribution is produced by a deterministic
export, verified by a standalone checker, and never pushed by this tooling.

1. **`bin/export-public`** builds the artifact: `git archive HEAD` (tracked
   files only) → root-anchored EXCLUDE prune → reduce `prompts/` to
   `_template.md` → apply TRANSFORM rules (repo-name rewrite, version-pin
   rewrite to the export version, personal-path scrub, and de-linking of
   markdown links that resolve into excluded private paths) → run the verifier
   → run the repo validation suite *from inside the exported tree*. It refuses
   to run when the requested version ≠ `kit.json` `kitVersion` (the ADR-055
   invariant, machine-enforced). It performs **no** `git push`, repo creation,
   release, or auth switch, and a dry run needs no GitHub access.

2. **`bin/check-public-export`** is the deterministic, side-effect-free
   verifier. Given a staging tree it asserts the public contract: a top-level
   allowlist; excluded private/source paths absent (root `design/adr/**`,
   root `design/*.md`, `design/prd-addenda/**`, `notes/**`, `archive/**`,
   `.hermes/**`, `ai-review/config.json`, `ai-review/artifacts/**`, and any
   `prompts/*` other than `_template.md`); required artifacts present
   (`docs/architecture.md`, `prompts/_template.md`); no markdown link pointing
   into an excluded path; no old owner/repo URL strings; no personal absolute
   or temp/audit paths; and no stale version pin in install-surface files.
   Each violation names the offending file, path, or reference.

3. **Root-anchoring is load-bearing, and the link rule is resolution-based.**
   Exclusions and the link check operate on a path *relative to the export
   root*, not on substrings. This is why nested example-project content
   (`examples/projects/*/design/**`, including those projects' own
   `design/adr/**`) is preserved and its internal ADR links pass, while the
   kit's own root `design/adr/**` is excluded and any link into it is flagged.
   A single shared classifier (`bin/lib/export_paths.py`) backs both the
   verifier and the transformer so the boundary cannot drift between them.

4. **The kit's own ADRs do not ship** (confirming ADR-055 §4). Orphaned links
   into them from shipping docs/skills/templates are neutralized at export
   time by de-linking to plain anchor text. Source-level neutralization
   remains a valid future option, but the implemented default is an
   export-time transform so the source repo keeps its internally-resolving ADR
   links.

5. **The verifier is part of normal validation.** `bin/export-eval` drives
   `bin/check-public-export` over golden staging fixtures (clean and one per
   failure mode) and is wired into `bin/self-test`, so the leak/link contract
   is exercised on every change, fully offline.

6. **The export tooling is source-repo only and does not ship.** The export
   builds and verifies the public artifact; it is not part of it (the build
   script for a release is not shipped inside the release). Shipping it would
   also be self-referential: the verifier would flag its own leak-pattern
   literals, and the transform would scrub its own source-owner constants,
   breaking its fixtures. So the export prunes `bin/export-public`,
   `bin/check-public-export`, `bin/export-eval`, their `bin/lib/` helpers and
   fixtures, and `docs/publishing.md`, and reconciles the public `kit.json`
   (drops their `bin[]` entries), `bin/self-test` (drops the `export-eval`
   step), and `docs/README.md` (drops the runbook row) so nothing dangles and
   the in-export gates stay green. In the SOURCE repo the tooling is fully
   registered and validated like any other kit surface.

## Consequences

- The public artifact is reproducible and reviewable; internal material cannot
  reach it, and a dry run proves cleanliness with no GitHub access.
- Three new envelope-speaking scripts (`check-public-export`,
  `export-public`, `export-eval`) are registered in `kit.json` and covered by
  offline fixtures, consistent with [ADR-054](adr-054-script-vs-skill-boundary.md):
  the deterministic build/verify spine is scripted; judgment (what to publish,
  when, and the changelog prose) stays human/skill work. These scripts are
  source-only and are pruned from the public artifact (Decision 6).
- The generated tree lives under `dist/` (gitignored) — a build artifact,
  never committed.
- Out of scope / deferred: creating and pushing
  `olivermorgan2/claude-workflow-kit`, the `gh`-identity switch, the publish
  runbook, and cutting the first public release. This ADR settles the
  **export model and its verification**; publishing is a later, identity-gated
  sequence.
