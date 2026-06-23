# Open Questions

Unresolved questions awaiting an answer, a decision, or external input.
Resolve a question by recording the decision (here or in an ADR) and
linking it, then moving the entry to "Resolved".

## Open

### Q1 — What specifically needs tightening in the public release protocol?

The protocol for promoting work from the private/source repo to the public
repo needs tightening, but the specific weaknesses are not yet enumerated.
**The user will supply the details next.** Capture them here when provided,
then convert into concrete mitigations under [risks.md](risks.md) (R1) and,
if warranted, a governing ADR.

Related: the public-repo naming discrepancy noted in
[project-brief.md](project-brief.md) (README links reference
`olivermorgan2/workflow-generator`; the recorded operating name is
`olivermorgan2/claude-workflow-kit`) should be reconciled as part of
firming up the release protocol. The bootstrap URLs in `README.md` and
`docs/install.md` are also stale on version (`releases/download/v3.3.0/...`
while source is at v4.0.0); reconcile name and pinned version together.

### Q2 — How does the source repo relate to the public v5.0.0 release?

The reviewed public repo is at v5.0.0 with a command model, docs, and
validation scripts absent from source (latest tag v4.0.0) — see
[risks.md](risks.md) (R2). Decide the canonical direction before treating any
of Codex's public findings as source work: is public ahead (forward-port v5
into source) or a separate line (re-export from source)? This gates Codex
findings 1–6.

## Resolved

_None yet._
