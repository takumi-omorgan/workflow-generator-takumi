---
name: prd-to-mvp
description: Scope a normalized PRD into an MVP statement and a build-out plan
---

# prd-to-mvp

Take `Design/prd-normalized.md` and produce two artifacts: a scoped
**MVP statement** at `Design/mvp.md` and a sequenced **build-out plan**
at `Design/build-out-plan.md`. Both are rendered from existing
templates in this kit.

## When to use this skill

Use after `prd-normalizer` (Issue #6) has produced
`Design/prd-normalized.md`. If that file does not exist, run
`prd-normalizer` first.

This skill is the entry point from product planning into implementation
planning. Its outputs feed `adr-writer` (this issue) for architectural
decisions and `issue-planner` (later issue) for the GitHub backlog.

## What this skill does not do

- Does not draft ADRs — that is `adr-writer`. This skill surfaces a
  list of decisions that need ADRs, but does not write them.
- Does not execute the build-out plan — that is the executor skill.
- Does not revise the PRD in place. If the PRD is wrong, re-run
  `prd-normalizer`.
- Does not invent capabilities not present in the normalized PRD. If
  scope feels thin, that is information about the PRD, not licence to
  pad.

## Inputs

- **Required:** `Design/prd-normalized.md`.
- **Optional:** user preference on project size — weekend project,
  one-month, multi-month — to guide how aggressive the scope cut is.

## Outputs

- **`Design/mvp.md`** — rendered from
  [`templates/mvp-template.md`](../../templates/mvp-template.md).
- **`Design/build-out-plan.md`** — rendered from
  [`templates/build-out-plan-template.md`](../../templates/build-out-plan-template.md).

Both files are produced from a single scoping conversation. The two
artifacts are tightly coupled: phase 1 of the build-out plan must
cover every in-scope capability of the MVP.

## Scoping protocol

1. Read `Design/prd-normalized.md` end to end.
2. Propose an in-scope / out-of-scope split for every core capability
   and user story. Default to aggressive cuts; over-scoping is the
   more common failure.
3. Ask the user to confirm or adjust the split — one batched turn
   (≤ 5 questions). Include the project-size question if the user
   has not stated a preference.
4. Render `Design/mvp.md` from `templates/mvp-template.md`. Derive
   3–5 product principles from the normalized PRD's constraints,
   non-goals, and goal — principles that will resolve future scope
   arguments.
5. Draft `Design/build-out-plan.md` from
   `templates/build-out-plan-template.md`. Sequence into 2–4 phases.
   Each phase has a goal, deliverables, exit criteria. Ask the user
   once whether the phase count and shape feel right.
6. Surface a **"Decisions needing ADRs"** list as the final section
   of `build-out-plan.md` (or a short separate note). Each item is one
   architectural question with a one-line context pointer. This list
   is the input to `adr-writer`.

## How `[TBD]` fields are handled

The normalized PRD may contain `[TBD]` markers (see `prd-normalizer`).

- If a hard-required field is `[TBD]` (product name, problem, primary
  user, ≥1 capability, ≥1 story), stop and send the user back to
  `prd-normalizer`. MVP scoping cannot proceed without these.
- If a soft field is `[TBD]` (e.g. constraints and preferences), note
  it as an open item in `mvp.md`'s acceptance section and continue.

## Self-check before finishing

Do not write either file until all five hold:

- [ ] Every core capability from the normalized PRD is classified
  (in scope or out of scope). None left ambiguous.
- [ ] The MVP success criteria are end-to-end user outcomes, not
  implementation tasks.
- [ ] The "Out of scope" list combines (a) product-level non-goals from
  the normalized PRD and (b) capabilities this skill deferred. The two
  sources are not conflated — readers can see why each item is out.
- [ ] Build-out-plan phase 1's exit criteria collectively cover every
  in-scope capability.
- [ ] No `{{...}}` template placeholders remain in either rendered
  file.

## Handoff to `adr-writer`

The "Decisions needing ADRs" list at the end of the build-out plan is
the direct input to `adr-writer`. Each item should be a single
architectural question (e.g. *"GPX parsing: browser-side vs.
server-side"*), not a feature description. `adr-writer` accepts a
batch of these in one run.

See [`example.md`](example.md) for a worked PRD → MVP + build-out plan
walkthrough.
