
# ADR-045: Rename `Design/` → `design/` for root-directory casing consistency

**Status:** accepted
**Date:** 2026-05-07

## Context

`Design/` is the only TitleCase top-level directory in a kit where every other root directory is lowercase: `docs/`, `notes/`, `skills/`, `templates/`, `bin/`, `prompts/`, `examples/`, `archive/`. The capitalised root *files* (`README.md`, `LICENSE`, `CHANGELOG.md`, `CLAUDE.md`) follow well-known external conventions; `Design/` has no analogous external anchor — its TitleCase is a project-internal choice that diverges from its peers without a load-bearing reason.

ADR-005 (accepted 2026-04-12) established `Design/adr/` and `Design/ai-summary.md` as the locations for core docs generated into target projects. ADR-005's substantive decision is *generate core docs into the target repo* — the directory casing was incidental at the time. Since then, 15 other accepted ADRs have come to cite `Design/`, for ~58 occurrences across ADR bodies and ~176 files / ~500+ occurrences kit-wide (skills, templates, docs, examples, `bin/lib/check-plan-eval.sh`, `CLAUDE.md`, `README.md`).

A pre-ADR `/clarify` pass (recorded in this conversation, no `design/decisions.md` artefact since the kit has shipped past entry-flow inputs) settled four open questions that would otherwise muddy this ADR:

1. **Ship the rename?** Yes — consistency is worth the one-time cost.
2. **What does it rename to?** `design/` — pure case fix, preserving the directory's current breadth (ADRs + state + summaries + optional MVP/decisions/planning). Alternatives `decisions/` and `planning/` were rejected because both would force splitting `state.md` and `ai-summary.md` out into a new home, doubling the blast radius and turning a case fix into a structural restructure.
3. **How to handle accepted-ADR rewrites?** Authorise mechanical path-string rewrite via ADR-044 (drafted alongside this one, sequenced first). ADR-044 is the precondition for touching the 16 affected ADR bodies without supersession cascade.
4. **Migration story?** Document a manual two-step rename + bulk `sed` snippet in CHANGELOG / release notes:

   ```bash
   git mv Design _design_tmp
   git mv _design_tmp design
   grep -rl 'Design/' . | xargs sed -i '' 's|Design/|design/|g'
   ```

   The two-step pattern is required on case-insensitive filesystems (macOS APFS by default), where the naïve `git mv Design design` fails with `Invalid argument`. No new tooling. Per ADR-002 the kit explicitly scopes to new projects, so the snippet is a courtesy for users who installed prior versions, not a contract.

## Options considered

### Option A: Rename `Design/` → `design/` (pure case fix)

- Pros: resolves the inconsistency directly; smallest semantic change; preserves the directory's current breadth so `state.md`, `ai-summary.md`, `mvp.md`, `decisions.md`, `planning.md` keep their existing home; migration for prior-version installs is a one-line `git mv` plus a `sed` snippet; rewriting the 16 affected ADR bodies is authorised by ADR-044 and requires no further supersession.
- Cons: breaking change for every existing target-project install; touches ~176 files / ~500+ occurrences kit-wide; depends on ADR-044 being accepted first.

### Option B: Rename `Design/` → `decisions/` (semantic narrow)

- Pros: tighter semantic fit for ADR-shaped content; clarifies intent.
- Cons: forces splitting `state.md`, `ai-summary.md`, `mvp.md` out into a new home (root-level or a new `planning/`); doubles the blast radius; turns a case fix into a structural restructure; addresses a problem entry #7 did not flag (case inconsistency, not semantic ambiguity).

### Option C: Leave `Design/` as-is

- Pros: zero change; zero break; zero migration cost.
- Cons: TitleCase inconsistency stays indefinitely; every new target-project install inherits the inconsistency; the paper-cut compounds as the kit accrues users; the case-mismatch keeps showing up as an onboarding observation.

## Decision

Adopt **Option A**. Rename `Design/` → `design/` across the kit, the convention it teaches target projects, and inside the 16 affected accepted ADR bodies — using the mechanical-rewrite exception established by ADR-044 as the authority for those ADR-body edits.

This supersedes ADR-005 on the directory-casing question only. ADR-005's substantive decision (*generate core docs into the target repo, including ADRs and the AI summary*) stands; only the path strings change. ADR-005's status flips to `superseded by ADR-045` when the rename PR lands. No other ADR is superseded — they are mechanically rewritten under ADR-044.

## Consequences

- Root-directory casing becomes uniformly lowercase across the kit and the convention it teaches target projects; the onboarding paper-cut is gone.
- Breaking change for every existing target-project install. Release notes for the rename version carry a two-step `git mv` + `sed` snippet (see Context §4 above) — the two-step variant is required on case-insensitive filesystems (macOS APFS) where `git mv Design design` fails. Per ADR-002 the kit scopes to new projects, so the snippet is a courtesy, not a contract — users who pin to a prior kit version stay on that version's directory layout.
- Touches ~176 files / ~500+ occurrences across `CLAUDE.md`, `README.md`, `docs/`, `templates/`, all 19 `skills/*/SKILL.md`, `bin/lib/check-plan-eval.sh`, `examples/projects/*/`, and 16 accepted ADR bodies. The 16 ADR rewrites are authorised by ADR-044 and require no further supersession; ADR-005 alone is superseded (casing question only).
- ADR-044 must be accepted before the rename PR can merge. Issue sequencing: ADR-044's issue ships first; ADR-045's issue ships second and references both ADRs.
