# Working notes

Scratch, ideation, and triage files used while building the kit itself.
These are **kit-repo-only** — they are not copied into target projects.

Contents:

- `bug-fixes.md` — triage holding pen for bugs found during dev / eval /
  dogfooding. Entries graduate to GitHub issues.
- `feature-ideas.md` — backlog of feature ideas captured for later batching.
- `refactoring-ideas.md` — backlog of kit-internal refactoring ideas
  (naming conventions, file organisation, supersession follow-ups,
  technical debt). Distinct from `bug-fixes.md` (something is broken)
  and `feature-ideas.md` (new capability).
- `eval-issue-NNN.md` — per-issue dogfood/eval carry-forward notes.
- **M0 baseline audit (2026-06-05)** — milestone-M0 stabilising-gate
  deliverables produced before roadmap feature work:
  - `baseline-health.md` — pass/fail/not-run status of every check and
    smoke test (M0-1).
  - `skill-metadata-handoff-audit.md` — name/permission/handoff/output
    drift audit across all 19 skills (M0-2).
  - `installer-idempotency-audit.md` — fresh-install + rerun behaviour,
    placeholder classification, doc drift (M0-3).
  - `dogfood-baseline-report.md` — first dogfood run: path, metrics,
    classified friction, improvements to re-check after M1/M2 (M0-5).

Historical content lives at top-level [`archive/`](../archive/) — kit-level
methodology docs, phase-1 issue prompts, and the shipped/dropped
feature-ideas ledger. Not under `notes/` because those are kit-level
historical artefacts, not session notes.

The current per-issue prompt template lives at
[`prompts/_template.md`](../prompts/_template.md); filled prompts go to
`prompts/issue-NNN-*.md` (see ADR-008). Use `/prepare-issue` to auto-fill
from a GitHub issue + linked ADRs.
