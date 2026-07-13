# Knowledge Log

Append-only, dated log of knowledge-layer updates. Newest entries at the
top. One line per update; link to the file or section that changed.

## 2026-07-13

- **Closed out v5.0.x: the kit is published.** `design/state.md` had been stale
  since 2026-06-21, still describing v5.0.0 as frozen and "awaiting
  identity-gated publish". Verified against `gh`: the public repo
  `olivermorgan2/claude-workflow-kit` exists (created 2026-06-12, public), and
  releases `v5.0.0` (tag `a38a142`, 2026-06-12) and `v5.0.1` (tag `1c0eba3`,
  2026-06-29, latest) are both published; source `kit.json` kitVersion is
  `5.0.1`. Rewrote the in-flight, blockers, recent-work, continue-here, and
  next-action sections accordingly — the publish blocker is cleared, and the
  next step is proposing the M6–M9 prerequisite ADRs (which currently exist
  only as untracked local drafts), not opening M6 issues.
- Recorded the durable lesson behind PR #40: the `guard` placeholder check
  grepped whole changed files, so a knowledge/design file that *describes* a
  placeholder token false-positived. Process checks over an append-only
  knowledge layer must scan **added lines**, not file contents — otherwise the
  layer's own history makes the gate unusable. Added
  [open-questions.md](open-questions.md) Q3 (Hermes Kanban, deferred).

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
