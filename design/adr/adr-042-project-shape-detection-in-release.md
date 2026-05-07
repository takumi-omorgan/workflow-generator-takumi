# ADR-042: Project-shape detection in `/release` for non-product projects

**Status:** accepted
**Date:** 2026-05-06

## Context

[ADR-028](adr-028-workflow-agnostic-framing.md) reframed the kit as
workflow-agnostic — applicable to research projects, books,
curricula, content projects, design system docs, internal-policy
documents, and any structured project where decisions and incremental
work matter, not only software. The reframing was a stance change in
the README and supporting docs; it did not change skill behaviour.

The v3.3.0 baseline eval surfaced one place where the kit's
behaviour still leaks the software-only assumption: `/release`. F26
(silent v0.1.0 default with product-shaped release notes) reproduced
across all three fixtures. Severity calibrated as: medium on
md-notes (partial-scope honesty), low on podcast-pipeline (the
operator-authored Caveats section pattern mitigated the leak), and
**escalated again on research-tracker** because that fixture's PRD
explicitly disclaims being a product (PRD contains *"I'm not shipping
a product"* language; success criteria are user-outcomes not
test-pass; `design/build-out-plan.md` is markdown-only with no
compile / build / deploy step).

On a project that is not a product, `/release` should not pretend
one is shipping. It currently does — defaults to v0.1.0, generates
release notes claiming *"first tagged release of …"*, and includes
no acknowledgement of the workflow-not-product framing. This is the
**strongest ADR-028-leakage signal in the release surface** across
the v3.3.0 baseline. The kit's claim to be workflow-agnostic needs a
structural enforcement point in `/release`, not just author
discipline.

This ADR cross-references [ADR-028](adr-028-workflow-agnostic-framing.md)
(the framing this enforces), [ADR-017](adr-017-release-skill.md)
(the `/release` skill scope being amended), and the upcoming
permission contract from [ADR-041](adr-041-auto-mode-permission-contract.md)
(which governs `/release`'s approval gate as a category-3
non-substitutable operation).

## Options considered

### Option A: Auto-detect with `--force-product-shape` override flag

- Pros: common case (operator does not have to think about it) works
  correctly without flag; edge case (auto-detection misclassifies)
  has a clean escape hatch; aligns with the kit's prefer-defaults
  philosophy; the same detection-with-override pattern already works
  in `/check-plan` and other skills; structural enforcement of
  ADR-028 in the release surface.
- Cons: detection signals must be tuned conservatively to avoid
  false-positives on borderline projects (e.g. a Python project
  whose PRD happens to use the word "workflow"); detection signals
  are new surface area that evolves with the kit's PRD / build-out
  templates; signal drift would silently break the rule.

### Option B: Operator-set flag with no auto-detection

- Pros: simpler spec — `/release --workflow-project` opts into the
  non-product framing; no detection signals to maintain; no
  false-positive risk.
- Cons: relies on operator memory across every release; the v3.3.0
  baseline is the data point that operators forget the flag and
  ship product-shaped release notes on workflow projects; this is
  precisely the silent-failure mode auto-detection exists to
  prevent.

### Option C: No spec change — document the workflow-project caveat in the workflow guide

- Pros: lightest possible change; no detection signals to maintain.
- Cons: exactly the gap the ADR exists to close. Manual release-body
  editing is what operators do today, and the eval data shows it
  drifts away from the project's actual shape.

### Option D: Detection without release-body change — flag-and-confirm only

- Pros: low-risk middle ground — `/release` notices the project
  looks non-product and asks the operator to confirm before
  proceeding, but does not change the release-body shape.
- Cons: half-measure. The friction this ADR exists to close is the
  release-body framing leak; flagging without changing the body
  leaves the leak in place once the operator confirms.

## Decision

Adopt **Option A**. Add project-shape detection to `/release`'s
preflight, with operator override.

**Detection signals** (`/release` scans for non-product project
indicators in this order):

- `design/prd.md` or `design/prd-normalized.md` contains
  *"not [shipping|building] a product"* / *"workflow"* /
  *"folder of markdown"* / equivalent language in the project's
  problem statement or success criteria.
- `design/build-out-plan.md` Build strategy section says
  *"There is no compile / build / deploy step"* or equivalent.
- Success criteria are user-outcome strings (e.g. *"a researcher
  can …"*) rather than test-result strings (e.g. *"all tests
  pass"*).
- Repo root has no `package.json`, `pyproject.toml`, `go.mod`,
  `Cargo.toml`, `Gemfile`, `requirements.txt`, or equivalent
  package manifest.

**Threshold:** **two-or-more signals** trigger the non-product code
path. Single-signal cases stay on the product code path; the
threshold is conservative to avoid false-positives on borderline
projects.

**Non-product release body** — when the non-product path triggers,
release notes lead with a clarifier:

> This is a workflow tag for documentation drift-tracking; the
> project is not a software product (see PRD for project shape).
> The version number is for snapshot ordering, not semantic
> versioning of an API.

Below the clarifier, the standard Features / Chores / Other sections
still emit (they are useful regardless of project shape) but the
overall framing is workflow-shaped rather than product-shaped. The
"first tagged release of …" language is replaced with snapshot
language.

**Override flag:** `--force-product-shape` overrides the
auto-detection and forces the standard product-release framing.
Documented for operators whose project trips the heuristic but
genuinely is a product. The reverse flag (`--force-workflow-shape`)
is also provided, symmetrically, for projects whose detection
signals are too sparse to trigger but the operator wants the
workflow framing.

**Canonical signal list:** lives in `skills/release/SKILL.md` as the
single source of truth, cross-referenced from the workflow guide.
Signal list evolves as the kit's PRD and build-out templates evolve;
changes go through the normal ADR amendment path if material.

## Consequences

- Easier: non-product projects get release framing that matches
  their actual shape automatically; F26-class agnostic-framing leak
  is closed in the release surface; the kit's claim to be
  workflow-agnostic gains a structural enforcement point in the
  release surface, not just doc-level reframing.
- Harder: auto-detection has false-positive cases that the
  threshold must tune against; signal drift between the detection
  list and the kit's evolving PRD / build-out templates is a new
  failure mode; operators on borderline projects need to learn the
  override flag.
- Maintain: detection signals live in `/release`'s SKILL.md as the
  canonical list; signal list evolves with the kit's PRD and
  build-out templates; the non-product release-body template is
  new copy that needs to stay aligned with the product-shape body
  as `/release` evolves.
- Deferred: extending the detection pattern to other release-adjacent
  skills (`/changelog`, `/audit-milestone`) is out of scope —
  revisit if leakage surfaces there in future evals. Recommending
  date-based snapshot tags (e.g. `2026.05` instead of `0.1.0`) for
  non-product projects is also deferred; the version-number
  convention can stay semver-shaped with the clarifier banner doing
  the framing work. Reusing detection across skills via a shared
  helper is left to the implementing issue if the pattern repeats.
