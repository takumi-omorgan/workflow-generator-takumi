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

### R2 — Source repo has diverged from the reviewed public release

- **Risk.** The public repo (`olivermorgan2/claude-workflow-kit`, v5.0.0) that
  Codex reviewed is not a clean export of this source repo (latest tag v4.0.0).
  The public command model (`/start`, `/next`, `/decide`, `/backlog`, `/work`,
  `/ship`), several docs (`architecture.md`, `agent-contract.md`,
  `workflow-control.md`), and validation scripts (`self-test`,
  `validate-kit-json`, `validate-carry-forward`, `check-consistency`) exist in
  public but nowhere in source history. As a result, 6 of 7 Codex findings have
  no source counterpart and cannot be "fixed in source then exported" as posed.
- **Status.** Open. Distilled in
  [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
- **Owner / next step.** Resolve the source↔public relationship (see
  [open-questions.md](open-questions.md) Q2): forward-port public v5 into source,
  or re-export from source. Until then, only Finding 7 is source-actionable.
