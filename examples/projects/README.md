# Worked project gallery

End-to-end reference projects that demonstrate the full kit workflow
for a small, realistic problem. Each project ships as a frozen
snapshot of artifacts — PRD, MVP, ADRs, GitHub issues, PRs, and a
rendered `CLAUDE.md`. They are **not** runnable software; the
artifacts *are* the example.

See [ADR-021](../../design/adr/adr-021-example-projects.md) for why
these exist.

## How these differ from the planning-path walkthroughs

- The walkthroughs in [`examples/`](../README.md) show the **intake
  phase** — how a user gets from idea / PRD to a scoped MVP.
- These project examples show what a **complete planning + execution
  artifact set** looks like after the first milestone has shipped.

## Projects

| Project | Flavour | Size |
|---|---|---|
| [`kb-lookup/`](kb-lookup/README.md) | 1-command Python CLI | 1 ADR, 2 issues, 2 PRs |
| [`slug-utils/`](slug-utils/README.md) | TypeScript library | 2 ADRs, 2 issues, 2 PRs |

## How to read one

Start with the project's own `README.md` — it lists the files in the
recommended reading order. Every example follows the same tree:

```
<project>/
  README.md           # 1-page tour
  design/
    prd.md
    mvp.md
    adr/
      adr-001-*.md
      [adr-002-*.md]
  issues/
    issue-001-*.md
    issue-002-*.md
  prs/
    pr-001-*.md
    pr-002-*.md
  CLAUDE.md
```

## Cross-references

Each example is internally consistent: its ADRs reference its PRD
and MVP; each issue references the ADR it implements; each PR
references its issue and ADR. Nothing in these examples points
outside its own folder (no links to real repos, live PRs, or
external state).
