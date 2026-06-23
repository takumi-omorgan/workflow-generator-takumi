# Knowledge Log

Append-only, dated log of knowledge-layer updates. Newest entries at the
top. One line per update; link to the file or section that changed.

## 2026-06-23

- **Corrected the Codex-findings diagnosis (second pass).** The first-pass
  read assumed source was at `v4.0.0` with the v5 command model/docs/validation
  scripts absent; current source is `kit.json` `kitVersion 5.0.0` with all of
  it present. Re-verified: 4 of 7 findings are source-actionable doc/content
  fixes (now shipped), 3 are false positives, none transform-created. Shipped
  source fixes: `jq` prerequisite added to `README.md` + `docs/install.md`
  (Finding 1 — standalone `jq` is used in six target-installed helpers and
  `bin/self-test`'s tool gate); de-staled `docs/github-setup.md` "What's next"
  and fixed its stale repo name (Finding 7); clarified the verb layer vs. the
  installed `/start` router in `README.md` + `docs/architecture.md` (Findings
  2/3). Retired risk R2 and resolved question Q2 (no source↔public divergence).
  Updated [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
- Verified Codex's 7 public-release (v5.0.0) findings against the source repo:
  1 valid (Finding 7, `docs/github-setup.md`), 3 invalid, 1 invalid-as-stated,
  2 not-applicable. Recorded the source↔public divergence as risk R2 /
  question Q2 and added
  [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
  No public-release fixes implemented.
- Initialized the knowledge layer: added `SCHEMA.md`, `index.md`,
  `project-brief.md`, `risks.md`, `open-questions.md`, `log.md`, and
  `reviews/README.md`. Seeded the project brief with the kit overview, the
  Scope → Decide → Backlog → Implement → Ship lifecycle, the public/private
  split, and the Claude/Codex/Hermes collaboration protocol. Recorded the
  public-release-protocol risk as an open risk/question pending details.
