# kb-lookup — worked example

A small CLI utility that looks up keyboard shortcuts for common apps from
the terminal. This example shows the full workflow kit output for a
real-but-tiny project, from PRD through a shipped PR.

## Why this example exists

`kb-lookup` is a one-command CLI with a tightly scoped domain (keyboard
shortcuts). It is small enough to read end-to-end in one sitting and
illustrates how the kit's artifacts fit together when the deliverable
is a single command-line tool rather than a web app or library.

## How to read this example

Start with the PRD, then walk the artifacts in the order the workflow
produces them:

1. [`Design/prd.md`](Design/prd.md) — the rough scope the user brought to the kit.
2. [`Design/mvp.md`](Design/mvp.md) — the in-scope cut produced by `prd-to-mvp`.
3. [`Design/adr/adr-001-shortcut-data-format.md`](Design/adr/adr-001-shortcut-data-format.md) — the one scoping decision that needed recording.
4. [`issues/`](issues/) — the two GitHub issues that make up the backlog.
5. [`prs/`](prs/) — the PR bodies that close those issues.
6. [`CLAUDE.md`](CLAUDE.md) — the rendered project rules Claude Code reads each session.

## What is deliberately missing

- No real installable package. A single 22-line sample script is shown
  in the PR body to make the example feel grounded, but this is not
  runnable software.
- No CI configuration, release tooling, or test framework setup beyond
  what the artifacts reference.
- Only one ADR. A real project would accumulate more over time; this
  example captures just the decision the planning step surfaced.
