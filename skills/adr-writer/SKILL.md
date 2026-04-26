---
name: adr-writer
description: Draft one or more ADRs from architectural decision topics, using the repo's ADR template
---

# adr-writer

Draft ADRs from a list of architectural decision topics — typically
the "Decisions needing ADRs" list surfaced by `prd-to-mvp`, but also
usable for any decision that comes up later. Output: one file per
decision in `Design/adr/`, each rendered from
[`templates/adr-template.md`](../../templates/adr-template.md), with
status `proposed`. Acceptance is a human act and is not done by this
skill.

## When to use this skill

- After `prd-to-mvp` has produced its "Decisions needing ADRs" list,
  to draft them in one batch.
- During implementation, when a new architectural decision needs to
  be recorded.

If the decision has already been made informally and you only need
the ADR to document it, this skill still works — the options analysis
just summarises the alternatives that were considered.

## What this skill does not do

- Does not perform MVP scoping — that is `prd-to-mvp`.
- Does not accept the ADR on the user's behalf. Status starts as
  `proposed`. Promotion to `accepted` is a human review act.
- Does not rewrite or supersede existing ADRs in place. To change
  an accepted decision, draft a new ADR and mark the old one
  superseded.
- Does not invent constraints. Constraints in the Context section
  come from `Design/prd-normalized.md`, `Design/mvp.md`, or the user.

## Inputs

- **Required:** one or more decision topics. Each topic is a short
  problem statement (e.g. *"GPX parsing: browser-side vs.
  server-side"*).
- **Recommended:** `Design/prd-normalized.md` for the constraints
  context.
- **Recommended:** `Design/mvp.md` for product principles and MVP
  scope context — useful when an option's pros/cons depend on what
  the MVP includes.

## Output

- **Files:** `Design/adr/adr-NNN-short-title.md`, one per decision
  topic, rendered from `templates/adr-template.md`.
- **Numbering:** sequential, never reused. The skill scans
  `Design/adr/` for the highest existing `adr-NNN-*.md` and starts
  numbering from the next integer. Within a batch, numbers increment
  in the order topics were given.
- **Status:** `proposed` for every ADR this skill produces.
- **Date:** today's date in `YYYY-MM-DD`.

## Alignment with existing ADRs

The skill follows the conventions of the kit's own ADR-001 through
ADR-006:

- Top-level heading `# ADR-NNN: Title`.
- `**Status:**` and `**Date:**` lines immediately after the heading.
- Four top-level sections: `## Context`, `## Options considered`,
  `## Decision`, `## Consequences`.
- Options as `### Option A: Name` etc., each with `- Pros:` and
  `- Cons:` bullets.
- `## Decision` is one short paragraph naming the chosen option and
  why.
- `## Consequences` is a bulleted list — what becomes easier, what
  becomes harder, what the team has to maintain, what is deferred.

If a future ADR amends the template, this skill follows the template.

## Drafting protocol — single decision

Repeat for every topic in the input batch:

1. Restate the decision topic as a one-line problem statement.
2. Pull relevant constraints from `Design/prd-normalized.md`'s
   "Constraints and preferences" field. Pull product principles from
   `Design/mvp.md` if it exists. These populate `## Context`.
3. Propose 2 or 3 options with Pros/Cons. Use 3 only when there is a
   genuine third alternative; otherwise 2.
4. Write `## Decision` naming the chosen option. If the choice is
   non-obvious, ask the user once.
5. Draft `## Consequences` as four bullets covering what becomes
   easier / harder / has to be maintained / is deferred. If a bullet
   has nothing to add, write "None new" rather than removing it.

## Drafting protocol — batch

When the input is multiple topics:

1. Confirm the list with the user in one batched turn — show the
   numbered topics and ask for any to be removed, reframed, or added.
2. For each topic in confirmed order, run the single-decision
   protocol.
3. For trivial decisions (the "obvious answer" case), keep the ADR
   short — two options, one-paragraph Decision, terse Consequences.
   Trivial does not mean skip the ADR; it means write it briefly.
4. Render every file. Report back the list of numbers and titles
   created.
5. After all files are rendered, run `bin/sync-adr-index` to refresh
   the index in `Design/adr/README.md`. This keeps the index table
   aligned with what is on disk (ADR-023). If the script reports
   changes, include `Design/adr/README.md` in the next commit
   alongside the new ADRs.

## How `[TBD]` fields are handled

If `Design/prd-normalized.md` contains `[TBD]` on the "Constraints and
preferences" field, ask the user once whether any constraints apply to
the current decision; do not block on it.

## Self-check before finishing each ADR

Per file:

- [ ] `NNN` is the next unused number in `Design/adr/`.
- [ ] Status is `proposed`.
- [ ] At least 2 options are listed, each with both Pros and Cons.
- [ ] Decision names one of the listed options (no hybrid unless the
  user explicitly asked for one).
- [ ] Consequences covers all four bullets ("None new" is allowed).
- [ ] Date is today's date in `YYYY-MM-DD`.
- [ ] No `{{...}}` template placeholders remain.

After the batch:

- [ ] `bin/sync-adr-index` ran cleanly. `Design/adr/README.md` is
  staged alongside the new ADRs.

## Handoff

The user reviews each `proposed` ADR and changes status to `accepted`
when ready. This skill does not auto-accept. Accepted ADRs become
inputs to the executor skill (later issue) when implementing the
related issues.

See [`example.md`](example.md) for a worked batch — one contentious
decision and one near-trivial decision drafted in a single run.
