# Knowledge Layer — Schema & Conventions

This directory is the **internal project knowledge layer** for the
private/source workflow-kit repository
(`takumi-omorgan/workflow-generator-takumi`). It is a lightweight,
git-reviewable record of stable project knowledge — decisions, risks,
open questions, and distilled review findings — that accumulates as we
build the kit.

> **Scope.** This layer is *internal tooling for developing the kit*. It is
> **not** a public kit feature, **not** a runtime feature wired into the
> skills/installer, and **not** copied into target projects. It never ships.
> See [project-brief.md](project-brief.md) for the public/private split.

## What lives here

| File | Purpose |
|---|---|
| `SCHEMA.md` | This file — conventions and curation rules |
| `index.md` | Hand-maintained map of the knowledge layer |
| `log.md` | Append-only, dated log of knowledge updates |
| `project-brief.md` | What the kit is, the lifecycle, the public/private split, the collaboration protocol |
| `risks.md` | Active risks worth tracking |
| `open-questions.md` | Unresolved questions awaiting input or a decision |
| `reviews/` | Distilled findings from adversarial reviews (one note per review-worthy event) |

## File conventions

- **Markdown only.** Every entry should read cleanly in a diff and a PR.
- **Stable knowledge, not state.** Capture things that remain true across
  sessions, not the moment-to-moment status of a task.
- **Date entries** in `log.md` and review notes using `YYYY-MM-DD`.
- **Link, don't duplicate.** Cross-reference ADRs in `design/adr/`, issue
  numbers, and `notes/` rather than copying their content here.
- **Keep it short.** A risk or open question is a few sentences plus
  enough context to act on it later.

## Curation rules

**Persist** (this is what the layer is for):

- Decisions and the reasoning behind them (or links to the governing ADR).
- Risks — anything that could derail the project or the public release.
- Open questions awaiting an answer, a decision, or external input.
- Distilled review findings — the durable lesson from a Codex review,
  not the line-by-line comments.
- Glossary / domain facts — terms, roles, conventions that recur.

**Do not persist** (these belong elsewhere or nowhere):

- Raw chat transcripts or conversation dumps.
- Temporary task state ("currently editing X", "next I'll run Y").
- Stale PR mechanics — branch names, CI run IDs, merge order once merged.
- Minor or one-off suggestions that don't change how we work.

When in doubt: if it would still be useful to a teammate joining in three
months, persist it. If it only matters for the next ten minutes, leave it out.

## How to update

1. Add or edit the relevant file (`risks.md`, `open-questions.md`, a new
   note under `reviews/`, etc.).
2. Add a dated one-line entry to [log.md](log.md).
3. Update [index.md](index.md) if you added or removed a file.
4. Commit on a docs branch and open a PR — the layer is reviewed like any
   other change.
