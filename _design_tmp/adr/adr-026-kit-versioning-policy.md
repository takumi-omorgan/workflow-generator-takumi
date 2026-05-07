# ADR-026: Versioning policy for the kit

**Status:** accepted
**Date:** 2026-04-26

## Context

The kit follows semantic versioning (`vMAJOR.MINOR.PATCH`) for its
GitHub Releases — `v1.0.0`, `v2.0.0`, and an in-flight `v3.0.0`
covering the recent ADR batch. But the kit's "API" is not an
imported library: it is a collection of templates, skills,
placeholder names, marker fences, installer flags, and shell
scripts. The standard semver intuition ("a breaking change is a
breaking change to the public API") does not map cleanly without
an explicit definition.

This came up in practice during the v3 cut: ADR-024 renamed the
heading `In v1` to `In scope` and the placeholder
`{{IN_V1_BULLETS}}` to `{{IN_SCOPE_BULLETS}}`. Whether that
counted as breaking depended on whether downstream parsers and
local template overrides count as part of the "API." There was
no written rule, so the call was made by judgment. Future releases
should not have to relitigate that question.

This ADR records the rule. It sits alongside ADR-016
(changelog/release-notes skill) and ADR-017 (release skill), which
define how releases are produced; this ADR defines what counts as
which kind of release.

## Options considered

### Option A: Don't write a policy; decide case-by-case

- Pros: lowest overhead; no ADR to maintain.
- Cons: identical changes can be classified differently across
  releases; the question is relitigated every time; downstream
  users have no contract to rely on.

### Option B: Write an explicit policy ADR

- Pros: a single source of truth; release classifications become
  mechanical; downstream users know what to expect; the changelog
  skill can apply the rules directly.
- Cons: a small ongoing maintenance cost — the policy may need
  revisions as the kit's surface evolves (e.g., when new artifact
  types are added).

### Option C: Adopt an external policy by reference (e.g. SemVer.org plus a "tooling adaptation")

- Pros: short ADR.
- Cons: standard SemVer assumes an imported API; the adaptation is
  the part that matters here, and it would still need to be
  written.

## Decision

Adopt **Option B**. Define the kit's semver surface explicitly. The
kit's "public API" is everything an installed target project
relies on, even though the kit is not imported as code. The
following table classifies common change types:

### MAJOR (breaking)

A bump to MAJOR signals that target projects scaffolded from a
prior version may need user-visible work to upgrade. Triggered by:

- **Renaming a placeholder** in any `templates/*.md` (e.g.,
  `{{IN_V1_BULLETS}}` → `{{IN_SCOPE_BULLETS}}`).
- **Renaming a heading parsed by a skill.** `workflow-docs` parses
  `Design/mvp.md` headings; `issue-planner` parses MVP scope
  sections; `prd-normalizer` reads PRD sections. Renaming any of
  those headings breaks parsers operating on existing files.
- **Renaming or removing a marker fence** (e.g.,
  `<!-- workflow-docs:start:scope -->`,
  `<!-- adr-index:start -->`). Marker fences are load-bearing — any
  change to their format must be major.
- **Removing a skill, template, or installer flag** that previously
  shipped as `accepted`-status.
- **Changing the installer's default behaviour** in a way that
  alters which files appear in a target project, or that changes
  the meaning of a flag.
- **Changing the canonical layout** documented in
  `docs/repo-structure.md` (e.g., moving `Design/adr/` to a
  different path).

### MINOR (additive)

A bump to MINOR signals new capabilities that existing target
projects can adopt without modifying anything they already have.
Triggered by:

- **Adding a new skill** under `skills/`.
- **Adding a new template** under `templates/`.
- **Adding a new installer flag** (with a backwards-compatible
  default).
- **Adding a new optional placeholder** to an existing template.
- **Adding a new ADR-status value** (e.g., `experimental`) that
  existing parsers tolerate.
- **Adding a new section** to a generated doc, behind a marker
  fence, that target projects pick up on next regeneration.

### PATCH

A bump to PATCH signals fixes and refinements that do not change
behaviour for any user. Triggered by:

- **Documentation fixes** — typos, prose rewrites, clarifications.
- **Internal refactors** that do not change any user-visible file
  shape.
- **ADR additions or status flips** (e.g., `proposed` → `accepted`,
  or a supersession that does not change behaviour).
- **Bug fixes** to skills or scripts where the previous behaviour
  was unambiguously wrong (e.g., a parser that crashed on valid
  input).
- **Updates to `examples/projects/`** that do not change template
  or skill behaviour.

### Edge cases and judgment calls

- **Heading rename in a template that no skill parses.** Treat as
  MINOR if the rename is additive (new heading replaces an old one
  that was decorative); MAJOR if downstream tooling outside the
  kit (CI scripts, docs sites) is known to depend on the old name.
  When in doubt, MAJOR.
- **Bug fix that changes output for some inputs.** If the fix
  alters output for inputs that were previously documented as
  working, MINOR or MAJOR; if the fix only affects undocumented
  edge cases or crashes, PATCH.
- **Status flip on an `accepted` ADR to `superseded`.** PATCH —
  the supersession ADR itself should describe behavioural changes,
  if any, and those changes are classified separately.
- **Removing a deprecated feature.** MAJOR. Deprecation should be
  introduced in a MINOR release with a removal target documented
  in the CHANGELOG; the removal itself is the MAJOR bump.

### Pre-1.0 exception

The kit is past `v1.0`, so the standard pre-1.0 semver permission
to make breaking changes in MINOR releases does **not** apply. All
breaking changes are MAJOR.

## Consequences

- The CHANGELOG generator (`/changelog`) and release skill
  (`/release`) can use this policy to classify the bump from a
  list of changes; the human author still confirms.
- Downstream users get an explicit contract: an upgrade from
  `vN.X.Y` to `vN.X.Z` requires no work; from `vN.X.Y` to
  `vN.M.0` (where M > X) is additive only; from `vN.0.0` to
  `vM.0.0` (where M > N) may require migration work documented
  in the CHANGELOG.
- The v3 release is correctly classified as MAJOR: ADR-024
  renamed placeholders and parser-relevant headings, which the
  policy classifies as MAJOR-triggering.
- This ADR will need revision when the kit grows new artifact
  types (e.g., starter CI workflows, plugin manifests). Treat
  those revisions as PATCH-level updates to the policy unless
  they reclassify existing change types.
- The policy is intentionally pragmatic, not legalistic. Where a
  call is genuinely close, document the reasoning in the
  CHANGELOG entry rather than forcing a binary classification.
