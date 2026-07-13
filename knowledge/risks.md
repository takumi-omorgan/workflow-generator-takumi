# Risks

Active risks worth tracking. Each entry: a short title, the risk, its
current status, and where it's being worked. Retire an entry (move it to a
brief "Resolved" note) once it no longer applies.

## Open

### R1 — Public release protocol needs tightening

- **Risk.** The protocol for promoting curated work from the private/source
  repo (`takumi-omorgan/workflow-generator-takumi`) to the public repo
  (`olivermorgan2/claude-workflow-kit`) has one unenforced leg: nothing
  verifies, *after* a publish, that the live public remote actually matches the
  artifact `bin/export-public` built and `bin/check-public-export` verified.
  `bin/export-public` never pushes (ADR-056 Decision 1), so the publish itself
  is a manual human step; a stale, partial, hand-made, or directly-committed
  publish would pass every gate the kit has today.
- **Scope corrected (2026-07-13).** This risk was originally written as a broad
  fear of *leaking* internal ADRs/evals/notes or publishing inconsistent
  artifacts. An audit of the live public repo at its published HEAD
  (`1c0eba3`) shows that is **not happening**: the published tree is exactly
  the 258 files the export produces, with no excluded paths and correct
  identity strings. The ADR-056 export contract is being honoured. The residual
  risk is **latent** — an unverified seam, not an active leak.
- **Status.** Open — **mitigation decided, not yet built.**
  [ADR-057](../design/adr/adr-057-public-export-integrity-gate.md) (accepted
  2026-07-13) decides a `bin/verify-published` post-publish gate: fetch the
  remote at the published tag, assert file-set and content equality against a
  freshly built artifact, and re-run the ADR-056 checks against the *fetched*
  tree. The risk does not close until that script ships and the release flow
  gates on it. Question [Q1](open-questions.md) is resolved; this risk is what
  remains of it.
- **Owner / next step.** Implement `bin/verify-published` per ADR-057 and wire
  it into the `/release` public shape as the final, blocking step.

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
