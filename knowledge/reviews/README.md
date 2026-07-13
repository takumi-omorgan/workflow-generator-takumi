# Reviews — Distilled Findings

This folder holds **distilled findings** from adversarial reviews (scored
reviews at the PRD, milestone/ADR, and PR quality gates). Capture the
durable lesson, not the raw comment thread.

Reviews are model-neutral: the reviewer is whichever independent model ran
the gate. Record the **model ID actually used** in each note rather than
assuming a default — defaults drift, so a note that names no model cannot be
audited later.

## What to record

One note per review-worthy event, named `YYYY-MM-DD-<short-slug>.md`. A
note should capture:

- **What was reviewed** — the PRD, ADR, milestone, or PR (link the issue/PR).
- **Reviewer** — the model ID that ran the review (e.g. `qwen/qwen3.7-plus`).
- **Score & verdict** — the score out of 5, blocker count, validation status.
- **Distilled findings** — the substantive issues that changed the work or
  how we work, phrased so they're useful later.
- **Resolution** — what we changed, or why we deliberately didn't.

## What not to record

- Line-by-line review comments or full transcripts.
- Minor or one-off suggestions that don't change the work or the process.
- Stale PR mechanics (branch names, CI run IDs) once the PR is merged.

See [../SCHEMA.md](../SCHEMA.md) for the full curation rules.

## Index

- [2026-06-23 — Codex review of public release (v5.0.0)](2026-06-23-public-release-codex-findings.md)
