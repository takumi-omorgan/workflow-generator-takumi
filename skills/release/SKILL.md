---
name: release
description: Tag a semver release, generate release notes via /changelog, and publish a GitHub Release. Use when ready to cut, tag, and publish a release; for release notes alone use /changelog instead.
permission-category: 3  # non-substitutable — git tag, git push, gh release create — maximum public visibility, per workflow-guide §7
inputs:
  - name: "--version / --bump"
    required: false
    description: "Explicit X.Y.Z, or major | minor | patch"
  - name: "--draft / --prerelease"
    required: false
    description: "Release visibility flags"
  - name: "--dry-run"
    required: false
    description: "Preview without tagging or publishing"
outputs:
  - artefact: "(git tag + GitHub Release)"
    description: "Annotated tag pushed; Release published via gh"
next: []
---

# release

Orchestrate the release ceremony: pick the next semver, get notes from
`/changelog`, create and push an annotated git tag, and publish a GitHub
Release. Every mutating step is gated behind a **single explicit approval**
(ADR-017). It only tags — never merges, pushes commits, or alters `main`.

Operator reference (rationale, override use-cases):
[`docs/skills/release.md`](../../docs/skills/release.md). Co-installed
companions read as needed: [`reference.md`](reference.md) (shape
signals/threshold + banner, version tiers, edge cases, invariants,
self-checks), [`example.md`](example.md).

## When to use

When `main` is worth a release and the user wants a tagged, published Release
— the terminus of issue → PR → merge. For changelog content alone, use
`/changelog`.

## Invocation and flags

`/release` with any of these (all optional):

- `--version=X.Y.Z` — explicit target (semver, no `v`); overrides bump.
- `--bump=major|minor|patch` — on the last tag; a first release seeds `0.1.0`.
- `--branch=main` — release branch.
- `--draft` / `--prerelease` — passed to `gh release create`.
- `--dry-run` — preview to the gate; mutate nothing.
- `--force-product-shape` / `--force-workflow-shape` — override detected
  shape; mutually exclusive (both → error).
- `--milestone-phase=N` — after release, set phase N's
  `design/build-out-plan.md` row to `released <tag>`; absent → report,
  continue.

If neither `--version` nor `--bump` is given, compute a suggestion (below)
and present it for confirmation.

## Release boundary

Default unit = **one phase**. With multiple `### Phase N` blocks and no
`--milestone-phase`, infer it: one phase milestone closed since the last tag
→ use it; else group range PRs by milestone (all one phase → use it); else
prompt once (`none` = multi-phase bundle). Confirm it in the plan. Single- or
phase-less projects skip this (one release = whole project); a bundle updates
every bundled phase's row.

## Suggested version

With no version supplied, run `bin/release-suggest --since-last-release
--format json` (target: `.claude/bin/release-suggest`) — **advisory**,
tags/publishes nothing; its `outputs` carry `suggestedBump`, `confidence`,
`signals`, `warnings`. Present them; `--version`/`--bump` or confirmation
overrides. A `low`/`medium` confidence, any `warnings`, or an empty range
(`suggestedBump: null`) → look closer; never tag on it alone. Signal-to-tier:
`reference.md`.

## Prerequisites (stop on any failure)

- `gh` authenticated (`gh auth status`); `git` tree clean
  (`git status --porcelain` empty); current branch == `--branch`.
- Local branch in sync with `origin/<branch>` (`git fetch`, then refuse if
  ahead/behind/diverged).
- `/changelog` available (`.claude/skills/changelog/`, or `skills/changelog/`
  in the kit repo); else abort (install `/changelog` first — ADR-016/Issue #18).
- If `design/adr/` exists, `bin/sync-adr-index --check` must be clean; on
  drift (exit 1) the user runs `bin/sync-adr-index`, commits, retries.

## Project shape (ADR-042)

After prerequisites, score the detection signals (`reference.md`): `shape =
workflow` when ≥2 fire, else `product` (default). Apply any force-shape
override (recording it for the plan). Shape gates framing: `product`
renders the changelog verbatim; `workflow` prepends the clarifier banner
(exact text in `reference.md`) to the notes, into both the tag and Release
body.

## Preceding tag

`git describe --tags --abbrev=0`. On success → the `/changelog` `--since`
base and the `--bump` base. On failure ("No names found") → **first release**
(default `0.1.0`), passing the initial commit
(`git rev-list --max-parents=0 HEAD | tail -1`) as the range start.

## Release flow

One turn, one `yes`. Run, in order: **prerequisites** → **shape detection**
(+ overrides) → **last-tag detection** → **target version** (above) →
**refuse if `vX.Y.Z` exists** (`git tag -l` / `git ls-remote --tags
origin vX.Y.Z`; suggest the next patch and exit) → **notes**
(`/changelog --since-last-release --output=- --github-release=vX.Y.Z`; no
commits → stop) → **render the plan** (version/tag; shape + any override
note; last tag; bump rationale; the `/changelog` preview, banner-prefixed
when `workflow`; tag message; Release config; the commands) → **approval
gate**: "Type `yes` to create and
push the tag and publish the release. Any other response cancels." — only
literal `yes` (case-insensitive, trimmed); `y`/`ok`/`sure` cancel.

**On `yes`** (skipped in `--dry-run`): write notes to a temp file
(`/changelog --output=<tmp> --github-release=vX.Y.Z`, prepending the workflow
banner when `shape=workflow`); `git tag -a vX.Y.Z -m "Release X.Y.Z\n\n<first
notes line>"`; `git push origin vX.Y.Z` (tag only); `gh release create vX.Y.Z
--title "vX.Y.Z" --notes-file <tmp> [--draft] [--prerelease]`; if
`bin/bootstrap-workflow-kit` exists,
`gh release upload vX.Y.Z bin/bootstrap-workflow-kit` (ADR-029); if
`--milestone-phase=N`, update its phase row. Then report the release URL
(`gh release view vX.Y.Z --json url -q .url`), clean up; `main` stays
untouched. Anything but `yes` cancels ("Release cancelled.").

`--dry-run` runs the plan steps (shape detection included, so the preview
shows if the banner fires), prints "Dry-run. Would execute:" with the
resolved commands, and mutates nothing.

## Receipts

Cat-3 mutating skill: idempotency receipt keyed by the **release tag**
([`docs/receipts.md`](../../docs/receipts.md)). **Before** tagging, check for
one (`bin/write-receipt --find --skill release --key <tag>`); a `completed`
receipt → the tag was already cut, so stop rather than duplicate. **On
completion**, write a `completed` receipt with the tag and URL in `outputs`.
Best-effort, gitignored, never blocks handoff.

## Handoff

`/release` is the terminus — no downstream skill. The user's next action is
external: share the URL and start the next issue.
