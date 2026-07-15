---
name: issue-planner
description: Turn design/mvp.md and design/build-out-plan.md into a reviewed batch of GitHub issues, plus a Project board. Use when filing the issue backlog after the MVP and build-out plan have been finalized.
permission-category: 3  # non-substitutable — gh issue create is public-visibility; existing approval gate is correct, per workflow-guide §7
inputs:
  - name: "--dry-run"
    required: false
    description: "Draft the issue batch without creating it"
  - name: "--no-project"
    required: false
    description: "Skip GitHub Project board creation"
  - name: "--force"
    required: false
    description: "Recreate issues even if a backlog exists"
outputs:
  - artefact: "(GitHub issues)"
    description: "Batch of issues created via gh issue create"
  - artefact: "(GitHub Project board)"
    description: "Project board for the issues"
next:
  - skill: prepare-issue
    when: "the backlog is created"
  - skill: workflow-docs
    when: "documenting the project"
---

# issue-planner

Read `design/mvp.md` and `design/build-out-plan.md`, draft a batch of GitHub
issues, show the full batch for **human approval**, then create the approved
issues via `gh issue create`; on success create a Project board and add every
issue.

Operator reference (rationale, parsing detail, edge cases, example):
[`docs/skills/issue-planner.md`](../../docs/skills/issue-planner.md) — not
needed at runtime.

## When to use

After `prd-to-mvp` produced `design/mvp.md` and `design/build-out-plan.md`,
and `adr-writer` drafted the ADRs it surfaced. If either plan file is missing,
stop and name the prerequisite (`prd-to-mvp`). Does **not** write ADRs, open
PRs, run the executor, or modify plan/ADR files.

## Inputs and outputs

**Inputs** — required: `design/mvp.md`, `design/build-out-plan.md`, and an
authenticated `gh` (`gh auth status`; boards also need the `project` scope —
see OAuth below). Optional: `design/adr/` (ADR refs); `design/planning.md`
(sequencing; `R1`… IDs in bodies).

**Outputs** — GitHub issues (one per `## Initial issue backlog` item); one
board `<repo> — <milestone>` (columns Todo/In Progress/Review/Done), every
issue added; a summary (numbers, titles, milestones, Project URL). No local
files are written.

## Invocation

- `/issue-planner` — full flow: parse, draft, approval, create issues +
  board, report.
- `--dry-run` — draft and show the batch; **zero** mutating `gh` calls
  (read-only queries still allowed).
- `--force` — skip the idempotency check; creates duplicates.
- `--no-project` — create issues but skip the board.

Flags compose.

## Parsing

Parse by **heading hierarchy**, not regex/YAML. In
`design/build-out-plan.md`, locate `## Initial issue backlog`; each
`### {{Milestone}}` subheading groups issues and every bullet is one issue
title. With `### Phase N` blocks, create **one milestone per phase** and
assign each issue to its phase; a single- or zero-phase plan uses one
project-wide milestone. Attach an ADR link when a draft matches an ADR's
number/topic/title, else `none`. Drift-tolerance, phase-assignment, and
legacy fallbacks: reference. Skip any malformed/empty heading and collect a
parsing warning for approval.

## Issue draft format

Each issue follows `templates/issue-template.md`: a concise **Title** (append
the ADR ref in parens when one applies; no `[type]` prefix); **Body** sections
in order — Summary; ADR (link to `design/adr/adr-NNN-*.md` or `none` +
reason); Goal; Why it matters; Tasks (2–6 checkboxes); Acceptance criteria
(observable, not a restatement of tasks); Notes (add a `Prompt:` line only if
`prompts/issue-NNN-*.md` already exists — never invent one); **Labels** =
`feature` + a kind (`design`/`docs`/`infra`/`chore`/`test`), existing only;
**Milestone** = the exact GitHub name.

## Label and milestone handling

- **Labels:** query `gh label list --json name`; attach only existing ones.
  For a missing label, list it at approval and ask to create
  (`gh label create <name>`), drop, or abort — never silently create.
- **Milestones:** query
  `gh api repos/:owner/:repo/milestones?state=all --jq '.[].title'`; use
  existing titles verbatim; for missing ones, list at approval and, on
  approval, create each via
  `gh api repos/:owner/:repo/milestones -f title=... -f description=...`
  (description from the plan's recommendation table). If none, prompt for one
  default and reuse it.

## Idempotency

Issue creation is irreversible. Before approval, run
`gh issue list --state all --limit 500 --json number,title,milestone`; mark a
draft **already exists** if an issue shares its title (or differs only in
punctuation/case). Such drafts show their number and are **excluded by
default**; `--force` skips this check. After a run, record an
idempotency **receipt** keyed by the plan/milestone id
([`docs/receipts.md`](../../docs/receipts.md)) — best-effort, never blocks.

## Approval flow (mandatory gate)

Present the full batch **before any mutating `gh` call**, in three parts: (1)
**preflight summary** — draft count, per-milestone breakdown, missing
milestones/labels, already-exists collisions, parsing warnings; (2) **full
drafts** — each issue's title, labels, milestone, ADR ref, body, numbered;
(3) **prompt** — "Reply `yes` to create these N issues + missing
milestone(s) + board; else `no`/edits." Only a literal `yes` (case-
insensitive, no leading punctuation) is approval; else revise. On
`--dry-run`: "Dry-run: no changes made."

## Creation flow

On approval, in order: (1) create approved missing labels; (2) create
approved missing milestones; (3) create each issue via
`gh issue create --title "<t>" --body-file <tmp> --label "<l1>,<l2>" --milestone "<m>"`
(temp file preserves newlines; capture URLs); (4) unless
`--no-project`, `gh project create --owner "@me" --title "<repo> — <milestone>"`
(first issue's milestone; multi-milestone → `<product-name> — backlog`); (5)
`gh project item-add <project-number> --owner "@me" --url <url>` per issue;
(6) report numbers/titles, Project URL, and skipped drafts. On failure, stop
and report what succeeded, what failed, and the `gh` error — **no rollback**.

## OAuth scope for Projects

`gh project create`/`item-add` need the `project` scope; if `gh auth status`
lacks it, warn at preflight and offer
`gh auth refresh -s project,read:project`, else suggest `--no-project` —
never silently downgrade.

## Self-check before any mutating `gh` call

Confirm: the user typed literal `yes` (unless `--dry-run`); every draft has a
non-empty title, body, and milestone; every attached label and referenced
milestone exists (or the user approved creating it); no `{{...}}`
placeholders remain. If any fail, stop and report.

## Handoff

The backlog feeds `prepare-issue` (→ per-issue prompts
`prompts/issue-NNN-*.md`) and `workflow-docs`.
