# slug-utils — worked example

A tiny TypeScript library for generating and parsing URL slugs. This
example shows the full workflow kit output for a project whose
deliverable is a **library API** rather than a user-facing app —
which changes the shape of the ADRs and issues compared to
`kb-lookup`.

## Why this example exists

Library projects have to make up-front API decisions that are
expensive to change later, so they tend to produce more ADRs per
line of code than CLIs or apps. `slug-utils` illustrates that: two
of the three recorded artifacts are ADRs, and both are about API
shape, not implementation.

## How to read this example

1. [`Design/prd.md`](Design/prd.md) — the problem statement.
2. [`Design/mvp.md`](Design/mvp.md) — in-scope capabilities and non-goals.
3. [`Design/adr/adr-001-public-api-surface.md`](Design/adr/adr-001-public-api-surface.md) — decides the shape of the exported API.
4. [`Design/adr/adr-002-unicode-handling.md`](Design/adr/adr-002-unicode-handling.md) — decides how non-ASCII input is treated.
5. [`issues/`](issues/) — two issues that together ship the MVP.
6. [`prs/`](prs/) — PR bodies closing those issues.
7. [`CLAUDE.md`](CLAUDE.md) — project rules for Claude Code.

## What is deliberately missing

- No published package — this is artifact-only.
- No real benchmarking. The MVP does not commit to performance targets.
- No `CHANGELOG.md` — one ships when the first release is cut.
