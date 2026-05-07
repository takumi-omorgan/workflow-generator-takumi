# Idea-only example — Pace Drift

> **Use this example if** you are starting from a rough idea — a paragraph,
> some bullets, scratch notes — and have no PRD yet.
> **Not this one if** you already have a polished PRD (use
> [`standard-prd-example.md`](standard-prd-example.md)) or your own
> custom planning notes (use [`custom-prd-example.md`](custom-prd-example.md)).

End-to-end walkthrough of the **no-PRD** path defined in
[ADR-003](../design/adr/adr-003-prd-intake-model.md). The scenario —
*Pace Drift*, a small web app for analyzing race-pace drift from a GPX
file — is the running example used across the kit's skill files, so
each step links to the canonical detail rather than duplicating it.

## Scenario

The user is a solo runner who wants a weekend project: a small web app
that loads one race GPX file and shows where pace drifted from a target
pace. They have one paragraph of intent and nothing more — no PRD, no
spec, no design doc.

## Step 1 — `idea-to-prd`

The user runs `idea-to-prd`. The skill reads the rough paragraph,
asks four batched elicitation questions (target user, platform, success
shape, explicit non-goals), and writes `design/prd.md` — a lightweight
8-section PRD draft.

→ Full input/output trace: [`skills/idea-to-prd/example.md`](../skills/idea-to-prd/example.md).

## Step 2 — `prd-normalizer` (standard path)

The user runs `prd-normalizer`. The PRD draft from Step 1 already has
the standard 8-section shape, so the normalizer's standard path
applies. It asks two identity-field questions (product name, one-line
description) and writes `design/prd-normalized.md` — the canonical
11-field shape that downstream skills consume.

A small relocation happens: the draft's *"No mobile-optimized view in
the first release"* item moves out of non-goals and into "Constraints
and preferences" because it is an MVP-scope decision, not a
product-level non-goal. That distinction matters for the next step.

→ Full input/output trace: [`skills/prd-normalizer/examples.md`](../skills/prd-normalizer/examples.md) (Example 1).

## Step 3 — `prd-to-mvp`

The user runs `prd-to-mvp`. The skill reads `design/prd-normalized.md`,
proposes an in-scope / out-of-scope split, asks four batched questions
(project size, capability cut, target-input format, phase shape), and
writes two files in one run:

- `design/mvp.md` — five in-scope capabilities, eight out-of-scope
  items separated by source (product-level non-goals vs.
  deferred-by-MVP scoping), four product principles, three end-to-end
  success criteria.
- `design/build-out-plan.md` — three phases (Foundation → UI →
  Validation), three milestones, twelve initial backlog issues, and a
  closing **"Decisions needing ADRs"** list with two items.

→ Full input/output trace: [`skills/prd-to-mvp/example.md`](../skills/prd-to-mvp/example.md).

## Step 4 — `adr-writer` (batch)

The user passes the two-item "Decisions needing ADRs" list to
`adr-writer`. The skill drafts both in one run:

- `design/adr/adr-001-gpx-parsing-location.md` — a contentious choice
  (browser-side vs. server-side), with two options weighed against
  the MVP's local-session and no-backend constraints.
- `design/adr/adr-002-test-framework.md` — a near-trivial choice
  (Vitest), drafted briefly to honour the kit's "decisions are
  recorded, not assumed" convention.

Both ship with status `proposed`. The user reviews and changes status
to `accepted` before execution begins — that is a human act, not an
auto-step.

→ Full input/output trace: [`skills/adr-writer/example.md`](../skills/adr-writer/example.md).

## Step 5 — First execution session

The user picks the first issue from M1 of the build-out plan
(*"Implement GPX parser"*), opens it on GitHub using the
[`feature-request`](../.github/ISSUE_TEMPLATE/feature-request.md)
template, and starts a Claude Code session with a filled
[`notes/issue-prompt.md`](../notes/issue-prompt.md). The filled prompt
references `design/adr/adr-001-gpx-parsing-location.md` and the M1
context.

→ Sample filled prompt: [`notes/issue-prompt-sample.md`](../notes/issue-prompt-sample.md).
→ How to fill it and what the closing evaluation summary must contain:
[`docs/issue-prompt-guide.md`](../docs/issue-prompt-guide.md).

## Final state of `design/`

After Step 4 (planning complete) and before Step 5 (execution begins),
the target project's `design/` tree looks like this:

```text
pace-drift/
  design/
    prd.md                                  ← Step 1 (idea-to-prd)
    prd-normalized.md                       ← Step 2 (prd-normalizer)
    mvp.md                                  ← Step 3 (prd-to-mvp)
    build-out-plan.md                       ← Step 3 (prd-to-mvp)
    adr/
      adr-001-gpx-parsing-location.md       ← Step 4 (adr-writer)
      adr-002-test-framework.md             ← Step 4 (adr-writer)
```

`prd.md` is preserved alongside `prd-normalized.md` — the original draft
is never overwritten.

## What happens next

The user works through the M1 backlog issue by issue, one Claude Code
session per issue, using `notes/issue-prompt.md` for each. After M1,
they move to M2 (UI) and M3 (Validation) per the build-out plan.

`issue-planner`, `claude-issue-executor`, `workflow-docs`, and
`pr-review-packager` are on the kit's roadmap (see
[`skills/README.md`](../skills/README.md)) but not yet shipped. Until
they are, the user opens issues and runs sessions manually — which is
what the example above already shows.
