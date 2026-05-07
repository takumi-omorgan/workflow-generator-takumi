# Standard-PRD example — Release Notes Generator

> **Use this example if** you already have a polished PRD in a
> conventional shape — sections like Problem, Goals, Functional
> requirements, Out of scope, Success criteria.
> **Not this one if** you have only a rough idea (use
> [`idea-only-example.md`](idea-only-example.md)) or your own custom
> planning notes (use [`custom-prd-example.md`](custom-prd-example.md)).

End-to-end walkthrough of the **standard-PRD** path defined in
[ADR-003](../design/adr/adr-003-prd-intake-model.md). The scenario —
*Release Notes Generator*, a small CLI that turns merged GitHub PRs
into a markdown changelog — is fresh to the kit (no prior skill
example covers it), so the artifacts are inlined here in abbreviated
form.

## Scenario

The user maintains a small open-source library and is tired of
hand-writing release notes. Before opening Claude Code, they wrote
themselves a polished PRD because they think better in writing. They
arrive at the kit with the PRD ready to go — no idea-capture step
needed.

## Step 1 — `prd-normalizer` (standard path)

The user passes their PRD to `prd-normalizer`. The skill recognises
the shape, maps the input sections onto the canonical 11 fields, asks
two batched questions (confirm product name; one-line description),
and writes `design/prd-normalized.md`.

The user's original PRD is preserved at its original path.

### Input — `design/release-notes-prd.md` (the user's PRD)

```markdown
# Release Notes Generator — PRD

## Overview
A small CLI that generates a markdown changelog from merged GitHub PRs
between two Git tags. Replaces the manual "scroll through merged PRs and
summarize" step at every release.

## Problem
At each release I hand-write release notes by scrolling through merged
PRs in the GitHub UI. It's slow, easy to miss a PR, and the output
varies in quality each time.

## Target users
- Primary: me, the maintainer producing release notes for the project's
  Git tags.
- Secondary: downstream consumers reading the produced changelog.

## Goals
- Generate a draft changelog from merged PRs in a tag range.
- Group PRs by their primary label (feature, fix, docs).
- Output is a markdown file ready to commit and push.

## Functional requirements
- Accept two Git tags as arguments, e.g. `v0.4.0..v0.5.0`.
- Use the `gh` CLI to fetch the PRs merged between the two tags.
- Group PRs by their primary label.
- Print a markdown section per group with PR title, number, and author.
- Write to stdout by default; `-o FILE` to write to a file.

## Non-functional requirements
- Single-file Bash or short Node script. No installer.

## Out of scope
- No GitHub release publishing — output is a markdown file, not an API
  call.
- No PR-description summarization or LLM rewriting.
- No CI/CD integration.

## Success criteria
- I can run `release-notes v0.4.0..v0.5.0 -o CHANGELOG.md` and the
  file is what I'd hand-write, give or take 10%.
- Less than 10 minutes per release vs. 30+ today.
```

### Output — `design/prd-normalized.md` (abbreviated)

After mapping to the canonical 11 fields:

- **Product name:** Release Notes Generator
- **One-line description:** A CLI that turns merged GitHub PRs in a tag
  range into a grouped markdown changelog.
- **Problem, Goal, Target users, Non-goals, Success signals** — passed
  through with the user's wording.
- **User stories** — the normalizer converts the PRD's "Functional
  requirements" into 3 stories ("As the maintainer, I run the CLI with
  a tag range so I get a draft changelog..." etc.).
- **Core capabilities** — the five functional-requirement bullets,
  un-prioritized.
- **Constraints and preferences:** single-file script (Bash or short
  Node), `gh` CLI dependency, no installer.
- **Open questions:** `[TBD]` — none surfaced in the input; user
  declined to add any.

→ For the full canonical shape: [`skills/prd-normalizer/SKILL.md`](../skills/prd-normalizer/SKILL.md).

## Step 2 — `prd-to-mvp`

The user runs `prd-to-mvp`. The skill reads the normalized PRD, asks
three batched questions (project size, capability cut, phase shape),
and writes both planning artifacts.

### `design/mvp.md` (abbreviated)

- **Principles:** Stdin/stdout-friendly. No installer. No LLM. One
  command, one purpose.
- **In scope:** all five functional capabilities — tag-range argument,
  `gh` PR fetch, label grouping, markdown output, `-o FILE` flag.
- **Out of scope:**
  - Product-level: GitHub release publishing; LLM rewriting; CI/CD
    integration.
  - Deferred-by-MVP-scoping: cross-repo aggregation; per-author
    sections; HTML output.
- **Success criteria:** end-to-end "run it on the next release and the
  output needs ≤ 10% editing"; runtime under 10 seconds for a typical
  release.

### `design/build-out-plan.md` (abbreviated)

- **Phase 1 — Core**: tag resolution, `gh` PR fetch, label grouping.
  Exit when running on a real tag range produces correctly grouped
  PR titles in stdout.
- **Phase 2 — Output**: markdown formatting and `-o FILE`. Exit when
  the output file is committable as-is.
- **Phase 3 — Polish**: error messages, README, dry-run on the next
  real release.

Initial backlog: ~7 issues across three milestones (M1 / M2 / M3).

### Decisions needing ADRs

1. **Implementation language: Bash vs. Node.** Affects portability,
   parser ergonomics, and dependency footprint.
2. **Test framework.** A defaults question; recorded for completeness.

## Step 3 — `adr-writer` (batch)

The user passes the two-item decisions list to `adr-writer`. One ADR
per item, drafted in one run, both with status `proposed`.

### `design/adr/adr-001-implementation-language.md` (abbreviated)

- **Context:** PRD constrains to "single-file Bash or short Node
  script — no installer." Need to pick one.
- **Options:** (A) Bash + `jq`; (B) Node single-file script.
- **Decision:** Node. The PR-list parsing logic is enough JSON
  handling that `jq` chains become hard to read; Node + native JSON
  keeps it under 200 lines and is testable.
- **Consequences:** Easier — testable with Vitest. Harder — Node
  must be installed (acceptable: maintainers already have it).
  Maintain — keep to a single file. Deferred — Bash port if a
  no-Node user appears.

### `design/adr/adr-002-test-framework.md` (abbreviated)

The trivial sibling — Vitest, two-option ADR, terse Consequences.
Same shape as the contentious one because the kit's convention is
*"decisions are recorded, not assumed."*

→ For the drafting protocol and full ADR shape:
[`skills/adr-writer/SKILL.md`](../skills/adr-writer/SKILL.md) and
[`skills/adr-writer/example.md`](../skills/adr-writer/example.md).

## Step 4 — First execution session

User reviews both ADRs and accepts them. Picks the first M1 issue
(*"Tag-range resolution and PR fetch"*) and starts a Claude Code
session with a filled [`notes/issue-prompt.md`](../notes/issue-prompt.md)
referencing `design/adr/adr-001-implementation-language.md`.

→ Template and guide:
[`notes/issue-prompt.md`](../notes/issue-prompt.md),
[`docs/issue-prompt-guide.md`](../docs/issue-prompt-guide.md).

## Final state of `design/`

```text
release-notes-generator/
  design/
    release-notes-prd.md                     ← user's original (preserved)
    prd-normalized.md                        ← Step 1 (prd-normalizer)
    mvp.md                                   ← Step 2 (prd-to-mvp)
    build-out-plan.md                        ← Step 2 (prd-to-mvp)
    adr/
      adr-001-implementation-language.md     ← Step 3 (adr-writer)
      adr-002-test-framework.md              ← Step 3 (adr-writer)
```

The original PRD lives at its original path; the normalized version is
the one downstream skills consume.

## What happens next

The user works through the M1 backlog issue by issue, one Claude Code
session per issue. After M1 they move to M2 and M3.

`issue-planner`, `claude-issue-executor`, `workflow-docs`, and
`pr-review-packager` are on the kit's roadmap (see
[`skills/README.md`](../skills/README.md)) but not yet shipped. Until
they are, opening issues and running sessions is manual — which is
what the example above already shows.
