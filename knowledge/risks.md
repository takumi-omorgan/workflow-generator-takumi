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
