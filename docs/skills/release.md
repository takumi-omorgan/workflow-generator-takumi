# release — operator reference

Rationale and background for the `release` skill. The agent operates from
`skills/release/SKILL.md` and its co-installed companions (`reference.md`,
`example.md`); it never reads this file. Anything needed to produce a correct
result stays in the body or those companions — this file is for the human
operator.

## Why this skill exists

It comes from [ADR-017](../../design/adr/adr-017-release-skill.md): `/release`
is the orchestration around `/changelog`, not a changelog generator itself.
It is the terminus of the delivery chain (issue → PR → merge → `/release`).
Project-shape detection is [ADR-042](../../design/adr/adr-042-project-shape-detection-in-release.md).

## What this skill does not do

- Does not generate changelog content itself — it invokes `/changelog` (and
  aborts, pointing at Issue #18, if `/changelog` is not installed).
- Does not modify existing tags, and never force-pushes tags.
- Does not create releases without explicit user approval.
- Does not merge branches, push commits, or alter `main` — it only tags.
- Does not decide semver unilaterally; it proposes and the user confirms.

## Why project-shape detection exists

The kit applies to any structured project — software or otherwise. On
non-product projects (research projects, books, curricula, content projects,
design-system docs, internal-policy documents), defaulting to product-shape
framing — "first tagged release of …", semver-shaped language,
software-flavoured copy — actively misleads users. The detection step is the
structural enforcement point that matches the release surface to the
project's actual shape. It classifies each release as *product-shape* (the
default) or *workflow-shape*, and the classification gates the framing of the
release-body content.

The detection signals, threshold rule, and outcome semantics are the single
source of truth in the co-installed
[`reference.md`](../../skills/release/reference.md); the cross-references in
`docs/workflow-guide.md` §2.i point back to it.

## Override flags — worked use cases

- `--force-product-shape` — forces `shape = product` regardless of signal
  count. Use on a project that trips the workflow-shape heuristic but is
  genuinely a software product (e.g. a software project whose PRD prose
  includes the word "workflow" enough times to score the PRD-language signal,
  plus a docs-only sub-project layout that scores the package-manifest
  signal).
- `--force-workflow-shape` — forces `shape = workflow` regardless of signal
  count. Use on a non-product project whose detection signals are too sparse
  to trigger but the operator wants the workflow-shape clarifier (e.g. a
  research-shaped project that carries a `requirements.txt` for analysis
  tooling, suppressing the package-manifest signal).

The two are mutually exclusive; passing both aborts with
"--force-product-shape and --force-workflow-shape are mutually exclusive."
An override takes effect immediately after detection and before the plan is
rendered, and the plan reports it prominently so the user sees auto-detection
was bypassed.

## Why the workflow tag summary is the banner's first line

For `shape = workflow`, the annotated tag's summary line is the opening line
of the clarifier banner. That is intentional: it labels the tag itself as a
workflow-shape release for anyone reading `git show vX.Y.Z` later.

## Reference and example

The edge-case behaviour table (no prior tag, dirty tree, `/changelog` empty,
`gh` failures, force-shape flag conflicts, PRD/build-out-plan missing), the
invariant list (never force-push, never mutate in dry-run), the pre-plan and
post-execution self-check checklists, and the signal-to-tier rules for the
version heuristic live in the co-installed
[`reference.md`](../../skills/release/reference.md). A worked walkthrough is
in [`example.md`](../../skills/release/example.md).
