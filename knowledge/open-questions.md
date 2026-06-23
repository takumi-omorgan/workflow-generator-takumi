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

Related (now largely settled in source): the active install/bootstrap
commands in `README.md` and `docs/install.md` already use the canonical
name and version (`olivermorgan2/claude-workflow-kit` @ `v5.0.0`), so the
naming/version reconciliation the first pass flagged here is done for the
user-facing surface. The only remaining `olivermorgan2/workflow-generator`
/ `v3.3.0` strings are in historical `CHANGELOG.md` entries, internal
`design/`/`notes/`/`prompts/` material (stripped from the public export),
the `bin/export-eval-fixtures/stale-version/` test fixture (intentionally
stale), and skill `example.md` illustrations — all left as-is by design.
What remains under this question is the *protocol* for keeping that
identity consistent across exports, not a concrete outstanding defect.

## Resolved

### Q2 — How does the source repo relate to the public v5.0.0 release?

**Resolved (2026-06-23, second pass): no divergence.** The first pass
assumed source was at `v4.0.0` with the v5 command model/docs/validation
scripts absent. That read was stale — current source is at `kit.json`
`kitVersion 5.0.0`, the `start` router skill exists, and the docs and
validation scripts the question listed all exist in source. There is no
"forward-port vs. re-export" decision to make; the Codex findings are
ordinary source-content/doc items, 4 of which were fixed this pass (the
rest false positives). See [risks.md](risks.md) (R2, retired) and the
corrected dispositions in
[reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
