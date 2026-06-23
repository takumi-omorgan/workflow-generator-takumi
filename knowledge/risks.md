# Risks

Active risks worth tracking. Each entry: a short title, the risk, its
current status, and where it's being worked. Retire an entry (move it to a
brief "Resolved" note) once it no longer applies.

## Open

### R1 — Public release protocol needs tightening

- **Risk.** The protocol for promoting curated work from the private/source
  repo (`takumi-omorgan/workflow-generator-takumi`) to the public repo
  (`olivermorgan2/claude-workflow-kit`) still has issues and needs
  tightening. Without a tight protocol there's a risk of leaking internal
  ADRs, evals, roadmaps, or source notes — or of publishing inconsistent
  or unreviewed artifacts.
- **Status.** Open. Specific details to be supplied by the user. Until
  then this is represented as an open risk, not a set of concrete defects —
  see [open-questions.md](open-questions.md) (Q1).
- **Owner / next step.** Await the user's details on what specifically is
  weak in the release protocol, then turn the specifics into concrete
  mitigations (and likely an ADR).

## Resolved

### R2 — "Source repo has diverged from the reviewed public release" (retired)

- **Original risk (now disproven).** The first pass claimed the public v5.0.0
  release was not a clean export of source (assumed latest tag `v4.0.0`), with
  the v5 command model, several docs, and validation scripts "absent from
  source history" — and concluded 6 of 7 Codex findings had no source
  counterpart.
- **Resolution.** That premise was a stale read of the tree. Current source is
  at `kit.json` `kitVersion 5.0.0`; the `start` router skill exists under
  `skills/start/`; `docs/architecture.md`, `docs/workflow-control.md`,
  `docs/workflow-guide.md`, `docs/claude-code-guide.md` and `bin/self-test`,
  `bin/validate-kit-json`, `bin/validate-carry-forward`, `bin/check-consistency`
  all exist. There is no v5 vs. source divergence to reconcile. 4 of 7 findings
  were source-actionable doc/content fixes (now shipped); 3 are false positives.
  See the corrected dispositions in
  [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
