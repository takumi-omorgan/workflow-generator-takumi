# ADR-022: Drop version qualifiers from kit-scope decisions

**Status:** accepted
**Date:** 2026-04-26

## Context

Several early ADRs (notably ADR-002) and kit-self docs phrase scope
decisions with the qualifier "in v1" — for example, "Limit v1 to
new-project setup only," "GitHub-first in v1," "in v1 the prepared
prompt alone guides the session." When the kit was pre-1.0, this
qualifier signalled "current scope, may expand later." After v2.0.0
shipped (2026-04-19), the qualifier became actively misleading: a
reader sees "v1" and asks whether the constraint still applies in v2,
even though no scope decision actually changed at the v1→v2 boundary.

The kit has no version-gated behaviour. Scope decisions live in ADRs
and are governed by supersession — when scope changes, a new ADR
supersedes the old one. Tying scope language to release numbers
duplicates that mechanism and creates drift the moment a release
ships.

A "single source of truth + automated check" alternative was
considered (a `VERSION` file plus a release-time grep that fails the
build if docs disagree). It was rejected as machinery without a
matching problem: the kit does not have version-gated behaviour to
enforce, and the wording "v1" in ADRs was never meant to be
auto-updated to "v2", "v3" etc. — the right state is to not version
the decision at all.

## Options considered

### Option A: Keep version qualifiers and update them at each release

- Pros: literal accuracy at the moment a release ships.
- Cons: requires every release to sweep multiple files; "v1 → v2 →
  v3" wording grows stale fast and adds no information; suggests
  version-gated behaviour that does not exist.

### Option B: Single source of truth + automated check

- Pros: enforces consistency.
- Cons: solves the wrong problem — the qualifier itself is the
  defect, not the inconsistency between copies of it.

### Option C: Drop version qualifiers from kit-scope decisions

- Pros: scope language stays valid across releases; supersession
  remains the single mechanism for scope changes; no per-release
  doc sweep.
- Cons: loses the historical signal that a decision was made
  pre-1.0; readers who want that context look at ADR dates and
  status.

## Decision

Adopt Option C. Kit-self ADRs and kit-self docs (`CLAUDE.md`,
`docs/install.md`, `docs/github-setup.md`, etc.) phrase scope
decisions without version qualifiers. When a scope decision changes,
the right move is a new ADR superseding the old one — not editing
qualifiers in place.

This decision **supersedes ADR-002** specifically, because ADR-002's
title and decision text are version-qualified ("Limit v1 to
new-project setup only"). The substantive decision is unchanged: the
kit is scoped to new projects only. ADR-002's status is updated to
"superseded by ADR-022" but its content remains as the historical
record (per the project rule against in-place ADR edits).

This decision **does not supersede** ADR-001, ADR-003, ADR-004,
ADR-006, ADR-014, or ADR-016, which mention "v1" in passing but whose
decisions remain valid. The "v1" wording in those ADRs should be read
as "the kit," and will drop out naturally if those ADRs are later
superseded for unrelated reasons.

This convention applies to **kit-self** language only. The
target-project MVP vocabulary "In v1 / Not in v1" — used in
`templates/mvp-template.md`, the MVP-related skills, and example
projects — is unaffected. That phrasing is a deliberate scoping
device for downstream projects' first releases and is part of the
kit's product surface.

## Consequences

- ADR-002 is marked superseded by ADR-022; the index in
  `Design/adr/README.md` reflects this.
- Kit-self docs (`CLAUDE.md`, `docs/install.md`, `docs/github-setup.md`)
  no longer version-qualify scope statements. (Already applied in the
  same change as this ADR.)
- Future scope changes go through new ADRs, not in-place edits to
  qualifiers.
- Historical planning artifacts (`Claude Code Workflow Kit MVP Spec.md`,
  `Claude Code Workflow Kit — Build-Out Plan.md`, `notes/`) keep their
  original "v1" wording — they are snapshots of the original plan, not
  living docs.
- Target-project MVP vocabulary ("In v1 / Not in v1") is out of scope
  for this ADR and continues unchanged.
