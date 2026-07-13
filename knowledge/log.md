# Knowledge Log

Append-only, dated log of knowledge-layer updates. Newest entries at the
top. One line per update; link to the file or section that changed.

## 2026-07-13

- **Accepted ADR-057 (public export integrity gate) — after falsifying two of
  its three motivating premises.** The first draft claimed the published repo
  had an identity mismatch and shipped internal exhaust (`archive/`, `notes/`,
  the `CLAUDE.md` contributor section). An audit of the live public repo at its
  then-HEAD (`1c0eba3`) found **both claims false**: the published tree is
  exactly the 258 files `bin/export-public` produces, with correct identity
  strings and no excluded paths. The **ADR-056 export contract is being
  honoured**. Only the third claim held — there is no post-publish verification
  — and it is *latent*, not an active defect. ADR-057 was **rewritten** around
  that one real gap (the verified `dist/` tree and the live remote are
  separately derived; nothing asserts they match) and re-reviewed to `READY`
  (`qwen/qwen3.7-plus`, 4/5, 0 blockers, 4 minor findings all applied). The
  identity-rewrite work the false premise had commissioned was **dropped**.
  Resolved [open-questions.md](open-questions.md) Q1 and re-scoped
  [risks.md](risks.md) R1 (mitigation decided; `bin/verify-published` not yet
  built). Receipt:
  [reviews/2026-07-13-adr-057-review.md](reviews/2026-07-13-adr-057-review.md).
  **Durable lesson (second occurrence): when a review asserts an observable
  defect, observe it before designing against it.** A `READY` score from a
  reviewer without repo access is conditional on its own premise findings —
  read the findings, not just the verdict.
- **Switched the default adversarial reviewer from Codex to Qwen 3.7 Plus.**
  The hardened-workflow gate in [`CLAUDE.md`](../CLAUDE.md) and the roles/gates
  in [project-brief.md](project-brief.md) named Codex as the reviewer. The
  operating default is now **Qwen 3.7 Plus** (`qwen/qwen3.7-plus`) via
  OpenRouter/Hermes. **The gate itself is unchanged** — `READY` is still
  required, and reviewer-unavailable still means HALT, now explicitly with no
  silent fallback to another model. Made the durable-review wording in
  [SCHEMA.md](SCHEMA.md) and [reviews/README.md](reviews/README.md)
  model-neutral, and required receipts to record the **model ID actually
  used** so the next default change doesn't invalidate the archive. Historical
  receipts keep their accurate Codex attribution — they *were* Codex reviews.
- **Recorded the Hermes Kanban direction: external / orchestrator-only.**
  Answered [open-questions.md](open-questions.md) Q3 in principle (build still
  deferred, nothing implemented). GitHub remains canonical for issues, PRs, and
  milestones; the kit ships no board/queue/DB runtime and this decision adds
  none. A Hermes Kanban, if built, mirrors GitHub and reads the
  fence-parseable `design/state.md` zones (`state:in-flight`,
  `state:next-action`) as dispatch inputs; optional backlog import stays
  Hermes-side. No Hermes-specific board internals enter the public kit unless
  a later ADR scopes it. Distinct from ADR-012 (GitHub Projects boards inside a
  *target* project), which is untouched.
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
