# ADR-061: Declarative runtime-asset manifest with required/optional semantics

**Status:** accepted
**Date:** 2026-07-14
<!-- Bundles notes/feature-ideas.md entries #36 (declarative runtime-asset
     manifest) and #37 (required vs optional installer assets), per
     both entries' own alignment notes. Sequenced BEFORE the ADR-059
     lifecycle tooling and ADR-060 install profiles, which consume it. -->

## Context

The kit has no declarative statement of what it installs. There is
exactly **one** structured declaration — the inline `RUNTIME_TEMPLATES`
array in the installer — surrounded by prose docs that restate it and
skills that consume its outputs by textual path. (Skills and docs are
not rival *sources of truth* so much as uncontrolled *copies* of a fact
only the installer states; the failure is that nothing reconciles them.)
The inline `RUNTIME_TEMPLATES` allowlist in
`bin/install-workflow-kit` is the clearest case: introduced with 12
entries (PR #65, commit `d245674`), it carries 13 today — the drift is
already underway. Adding one runtime template is a multi-step ritual
across installer, docs, tests, and staging rules. Separately, the
installer treats every missing source asset as warn-and-continue
(`bin/install-workflow-kit`, the `RUNTIME_TEMPLATES` copy loop: a
missing source logs `kit template missing` and continues), so a missing
*required* asset can produce a partially broken target while reporting
success (PR #65 review finding).

Two companion ADRs drafted in this same phase — not yet accepted at the
time of writing — consume this manifest, which is why it is sequenced
first:

- **ADR-059 (lifecycle)** — the upgrade planner must classify every
  installed file as kit-owned vs. generated vs. user-owned. Receipts
  record what *was* written; the manifest declares what *should* be.
  Without it, the upgrade plan re-derives ownership heuristically.
- **ADR-060 (install profiles)** — a `ship-loop` profile is, precisely,
  a subset selection over the asset list. Without a manifest, the
  profile becomes a second hardcoded list that drifts against the
  first.

This is the same drift class ADR-040/041/043 closed elsewhere: many
consuming surfaces, one canonical truth, PR review as the only
enforcement.

## Options considered

### Option A: Keep hardcoded installer lists; add profile/upgrade lists alongside

- Pros: no new artefact.
- Cons: three lists (install, profile, upgrade-ownership) describing
  the same facts; guarantees the drift this ADR exists to end.

### Option B: Markdown-table manifest + thin parser (`bin/list-runtime-assets`)

A single `runtime-assets.md` at the kit root — a stable-ID markdown
table, the same *format* convention as `skills/check-plan/criteria.md`
— with one row per asset: id, source path, install destination,
**required|optional**, **profiles** (full, ship-loop, …), ownership
class (kit-owned | generated | user-seeded), since-version.

Note the precedent is honest about its limits: `criteria.md` is a
structured table that scripts *cite* but none actually parses
(`bin/lib/check-plan-eval.sh` reimplements the criteria as shell
functions, and `bin/check-plan-criteria-drift` guards it by mtime
alone). `bin/list-runtime-assets` would therefore be the kit's **first**
machine-parser of such a table. That is a real cost — a parser is new
surface to test and keep robust — and it is accepted deliberately: the
alternative is not "no parser" but "three hardcoded lists". The table
borrows `criteria.md`'s readability, not a proven parsing layer.

`bin/list-runtime-assets` parses it and
emits the standard JSON envelope; the installer, `check-install-render`,
the ADR-059 upgrade planner, and the ADR-060 profile logic all consume
that output. Installer behaviour on missing source: **required ⇒
fail-fast** (accumulate all missing, report once, leave target clean);
**optional ⇒ warn-and-continue**; a test-only `--allow-missing` escape
hatch for fixtures that deliberately omit assets.

- Pros: one-file change to add an asset; partial-install-reported-as-
  success becomes structurally impossible; ADR-059/060 get their
  ownership and profile columns for free; consistent with the kit's
  existing structured-markdown + envelope idioms; no YAML dependency
  in the install path.
- Cons: bootstrap subtlety (the manifest and parser are themselves
  assets — resolved: they ship in the kit tree the installer runs
  from, not as installed assets); a schema to version; migration of
  the current hardcoded lists plus fixture updates.

### Option C: Pure-YAML manifest

- Pros: richer typing.
- Cons: adds a YAML parser dependency to the install path for no
  capability the table lacks; breaks the criteria.md precedent.

## Decision

Option B. `runtime-assets.md` becomes the single source of truth for
**what the kit installs and who owns it afterwards**, with
required/optional and per-profile columns; the installer,
`bin/check-install-render`, the upgrade planner, and profile selection
derive from it via `bin/list-runtime-assets`.

The claim is scoped deliberately. The manifest is authoritative for
*installation and ownership decisions*. It does **not** yet govern how
skills reference templates in their prose — those stay textual (see
Consequences). Calling it the source of truth for the installer's
behaviour is exact; calling it the source of truth for every mention of
a template in the kit would be false.

### This ADR owns both vocabularies

The manifest's two enumerated columns are settled **here**, not by the
ADRs that consume them. The sequencing argument above only works if the
dependency runs one way; a column whose valid values are defined by a
downstream draft would invert it.

- **Ownership class** — the closed set is `kit-owned | generated |
  user-seeded`. ADR-059's upgrade planner **adopts** this taxonomy. If
  ADR-059's review concludes it needs a different one (say, splitting
  `generated`), that is a superseding ADR against this one, not a
  silent redefinition of the column.
- **Profiles** — the initial valid set is exactly `{ full }`. The
  manifest validator enforces a **closed** vocabulary, so an unknown
  profile value is an error on day one. `ship-loop` becomes a legal
  value only if and when ADR-060 is accepted, which extends the set by
  amending this column's vocabulary. The column therefore ships
  validated, not as free text, and ADR-060 needs no data migration —
  only new rows' values.

### Parser contract

`bin/list-runtime-assets` is the kit's first machine-parser of a
markdown table, so its failure modes are part of the decision rather
than an implementation detail:

- **Strict, not permissive.** A row that does not parse — missing
  column, stray pipe, unknown profile or ownership value — is a **hard
  error naming the row**. It is never skipped. A permissive parser that
  silently drops a malformed row would recreate, one layer up, exactly
  the warn-and-continue failure this ADR exists to end.
- **No fallback.** If the manifest is missing or unparseable, the
  install **aborts**. It does not fall back to a hardcoded list —
  a fallback would quietly restore Option A and make the manifest
  advisory.
- **Missing sources.** Required ⇒ fail-fast: accumulate every missing
  required asset, report once, leave the target clean. Optional ⇒
  warn-and-continue.
- **`--allow-missing` is test-only and loud.** It exists for fixtures
  that deliberately omit assets. It must be passed explicitly, prints a
  prominent banner naming every asset it skipped, and is never used by
  the shipped install path. It downgrades required-missing to a warning
  and nothing else.

## Consequences

- Adding a runtime asset is a one-row change; CI
  (`check-install-render` + a new manifest validator) catches a row
  whose source path does not exist and an installed file no manifest
  row claims.
- Missing required assets abort the install with a complete list and a
  clean target; the warn-then-"success" failure mode is gone.
- ADR-059's classification and ADR-060's profile manifests reduce to
  reading columns instead of inventing parallel structures —
  **this ADR must be accepted before ADR-059 and ADR-060.**
- The manifest carries a `schemaVersion`, but it is a **parser
  contract, not decoration**: it is bumped only when a column is added,
  removed, or has its meaning changed, and the parser **rejects a major
  version it does not know** rather than guessing. Unlike `kit.json`
  (machine-emitted), this file is hand-edited, so the version buys
  exactly one thing — a comprehensible failure when an older kit meets
  a newer manifest.
- The `since-version` column is **informational and explicitly not
  validated**. It documents when an asset appeared; nothing enforces it
  and nothing may branch on it. Stating this is the point: an
  unenforced column that pretends to be authoritative is the drift this
  ADR opposes.
- Skills continue referencing paths textually; migrating skill
  references to manifest IDs is deferred until a real need appears. The
  manifest is therefore not yet the single source of truth for *every*
  template mention in the kit — only for what gets installed and who
  owns it. This is a known, accepted gap, not an oversight.
- The manifest and its parser ship in the kit tree the installer runs
  *from*, never as installed assets — otherwise the manifest would need
  to describe itself.
- Terminal-status bookkeeping: `notes/feature-ideas.md` entries #36
  (declarative runtime-asset manifest) and #37 (required vs optional
  installer assets) move to `adr-drafted` referencing this ADR.
