# Custom-PRD example — Stand-up Notes Bot

> **Use this example if** you have planning notes in your own format —
> mixed prose, bullets, brain-dump, a product brief, a spec — that does
> not look like a conventional PRD.
> **Not this one if** you have only a rough idea (use
> [`idea-only-example.md`](idea-only-example.md)) or a polished
> conventional PRD (use [`standard-prd-example.md`](standard-prd-example.md)).

End-to-end walkthrough of the **custom-PRD** path defined in
[ADR-003](../design/adr/adr-003-prd-intake-model.md). The scenario —
*Stand-up Notes Bot*, a Slack bot that collects daily stand-up posts
into a single tidy summary — is the running custom-input example used
in the kit's skill files. Step 1 links to the canonical detail; the
downstream steps are sketched in abbreviated form here.

## Scenario

The user is building a small internal tool for their team. They wrote
a "what I'm thinking" brain-dump in their own structure — mixed prose,
"Things I care about" bullets, "Not doing" list, "Stuff I haven't
figured out" musings — and saved it as `design/brief.md`. They have no
PRD in any conventional shape.

## Step 1 — `prd-normalizer` (custom path)

The user runs `prd-normalizer`. The skill detects the input is not a
conventional PRD and uses its custom path: read the whole document,
identify sections by **semantic meaning** rather than heading name,
map onto the canonical 11 fields, batch-ask 5 questions for the gaps,
write `design/prd-normalized.md`. The user's `design/brief.md` is
preserved at its original path.

→ Full input/output trace, including the brain-dump input, the
elicitation questions, and the rendered normalized PRD:
[`skills/prd-normalizer/examples.md`](../skills/prd-normalizer/examples.md) (Example 2).

## Step 2 — `prd-to-mvp`

The user runs `prd-to-mvp`. The normalized PRD has clear product-level
non-goals from the user's "Not doing" list (no standalone app, no
analytics, no DM reminders, no AI rewriting) and clear constraints
from the user's "Things I care about" list (Slack-native, AWS Lambda,
verbatim posts, single-team only).

### `design/mvp.md` (abbreviated)

- **Principles:** Slack-only. Verbatim, never paraphrased. Single
  team. Cron-shaped, not interactive.
- **In scope:** listen to #team-eng for stand-up posts up to a cutoff;
  group by author; post a single summary to #team-leads at 10:00.
- **Out of scope:**
  - Product-level: standalone app; analytics or trends; DM reminders;
    AI rewriting.
  - Deferred-by-MVP-scoping: multi-team support; threaded-reply
    handling; per-recipient time-zone delivery.
- **Success criteria:** end-to-end "Priya stops manually scrolling
  to assemble her morning report"; the 10:00 summary arrives on time
  every working day.

### `design/build-out-plan.md` (abbreviated)

- **Phase 1 — Listen and collect**: Slack event subscription, post
  storage in memory, cutoff handling. Exit when posts are collected
  for one working day.
- **Phase 2 — Format and post**: render summary, post to #team-leads
  on schedule. Exit when the summary lands daily for a week without
  intervention.

Initial backlog: ~5 issues across two milestones (M1 / M2).

### Decisions needing ADRs

1. **Storage for collected posts before the 10:00 post.** In-memory
   only (lost on Lambda cold start) vs. lightweight persistence (S3 or
   DynamoDB).
2. **Time zone for the 10:00 cutoff.** UTC vs. London (where the
   manager is) vs. configurable.

## Step 3 — `adr-writer` (batch)

The user passes the two-item decisions list to `adr-writer`. Both
ADRs drafted in one run, both `proposed`.

### `design/adr/adr-001-post-storage.md` (abbreviated)

- **Context:** Lambda runtime; need to retain posts from ~09:00 until
  the 10:00 summary; Lambda cold-starts may evict in-memory state.
- **Options:** (A) in-memory only and accept rare misses; (B) DynamoDB
  table keyed by date and author.
- **Decision:** DynamoDB. Cost is negligible at this scale; rare
  misses on a daily report are user-visible bugs the manager will
  notice.
- **Consequences:** Easier — predictable behaviour across cold
  starts. Harder — one more AWS resource to provision. Maintain — TTL
  the table to drop posts after 24 hours. Deferred — multi-team needs
  a second key dimension.

### `design/adr/adr-002-cutoff-time-zone.md` (abbreviated)

The simpler sibling — pick London time (the manager's), because the
9:55 cutoff is meaningful relative to *her* day, not engineering
geographies. Two-option ADR, terse Consequences.

→ For the full drafting protocol:
[`skills/adr-writer/SKILL.md`](../skills/adr-writer/SKILL.md) and
[`skills/adr-writer/example.md`](../skills/adr-writer/example.md).

## Step 4 — First execution session

User accepts both ADRs and picks the first M1 issue
(*"Slack event subscription"*). Starts a Claude Code session with a
filled [`notes/issue-prompt.md`](../notes/issue-prompt.md) referencing
the Slack-API constraints and `design/adr/adr-001-post-storage.md`.

→ Template and guide:
[`notes/issue-prompt.md`](../notes/issue-prompt.md),
[`docs/issue-prompt-guide.md`](../docs/issue-prompt-guide.md).

## Final state of `design/`

```text
standup-notes-bot/
  design/
    brief.md                                 ← user's original (preserved)
    prd-normalized.md                        ← Step 1 (prd-normalizer)
    mvp.md                                   ← Step 2 (prd-to-mvp)
    build-out-plan.md                        ← Step 2 (prd-to-mvp)
    adr/
      adr-001-post-storage.md                ← Step 3 (adr-writer)
      adr-002-cutoff-time-zone.md            ← Step 3 (adr-writer)
```

The original `brief.md` is preserved; the normalized version is the
one downstream skills consume.

## What happens next

The user works through the M1 backlog issue by issue, one Claude Code
session per issue, then moves to M2.

`issue-planner`, `claude-issue-executor`, `workflow-docs`, and
`pr-review-packager` are on the kit's roadmap (see
[`skills/README.md`](../skills/README.md)) but not yet shipped. Until
they are, opening issues and running sessions is manual — which is
what the example above already shows.
