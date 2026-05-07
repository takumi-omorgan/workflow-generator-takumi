# Examples

Reference material for users of the kit. There are two distinct
kinds of content here — pick the one that matches what you want
to learn.

Examples live in the kit repo only — they are reference material
for users, not something copied into a target project.

## Planning-path walkthroughs

Short scenarios that show how the kit's **intake phase** works for
each of the three PRD starting points defined in
[ADR-003](../design/adr/adr-003-prd-intake-model.md). Use these to
choose which skill to run first.

| File | Scenario |
|---|---|
| [`idea-only-example.md`](idea-only-example.md) | Start from a one-paragraph idea (Pace Drift) |
| [`standard-prd-example.md`](standard-prd-example.md) | Start from a conventional PRD (Release Notes Generator) |
| [`custom-prd-example.md`](custom-prd-example.md) | Start from mixed / custom notes (Stand-up Notes Bot) |

Each file is a six-section walkthrough with the same structure —
pick the one that matches your starting point. The header of each
example points you back here if you chose the wrong one.

## Worked project gallery

Complete artifact sets for small, realistic projects that have
already been scoped and part-way executed. Use these when you
want to see what the **full output of the kit** looks like after
the first milestone has shipped — PRD, MVP, ADRs, issues, PRs,
and a rendered `CLAUDE.md` — all in one place.

See [ADR-021](../design/adr/adr-021-example-projects.md) for why
these exist and [`projects/README.md`](projects/README.md) for the
gallery index.

| Project | Flavour |
|---|---|
| [`projects/kb-lookup/`](projects/kb-lookup/README.md) | 1-command Python CLI |
| [`projects/slug-utils/`](projects/slug-utils/README.md) | Zero-dependency TypeScript library |

The two kinds of content complement each other: walkthroughs teach
the *intake* flow, while the gallery shows what the *output* of
that flow plus one execution milestone looks like. Start with a
walkthrough if you are deciding how to begin; start with a gallery
project if you are trying to picture the finished artifacts.
