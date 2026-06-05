<!--
  PRD Addendum 001 — AI PR review capability (Milestone M5).
  Written for Issue 22 using the follow-up PRD workflow (ADR-049,
  templates/prd-addendum-template.md). The addendum EXTENDS the kit's
  product definition; it does not replace it.
-->

# PRD Addendum 001: AI PR review capability

## Context

- **Original PRD:** the kit predates `design/prd.md`; its founding
  product definition is [`archive/mvp-spec.md`](../../archive/mvp-spec.md)
  and its current, governing direction is the roadmap,
  [`design/workflow-generator-roadmap-and-issues-20260605.md`](../workflow-generator-roadmap-and-issues-20260605.md).
  This addendum extends that direction; neither founding document is
  rewritten.
- **Current milestone/state:** M0–M4 have shipped (baseline health,
  front-door simplification, the machine-readable agent contract, unified
  workflow control + follow-up PRD workflow, and reliability/validation/
  self-test). The kit carries a project from idea to release but stops at
  PR creation — the **review** stage on an open PR has no kit support.
- **Trigger for this update:** Milestone M5 (roadmap Issues 22–28) adds an
  AI-assisted PR review capability. Per ADR-049 and the roadmap's own
  dogfood note, M5 is introduced as the first real follow-up PRD addendum
  rather than as ad hoc implementation issues.

## Problem

Review is the one lifecycle stage the kit does not support. Once
`/pr-review-packager` opens a PR, the operator is on their own. Teams that
want a consistent first-pass review — correctness, security, regressions,
test coverage — must either do it entirely by hand or wire up a bespoke
bot. A naïve bot creates its own problems: comment spam, duplicate
comments on re-runs, low-signal style nits, and an external model API that
quietly leaks diffs or burns budget. The kit needs a review capability
that is **safe by default**: review generation can be automated, but any
write to GitHub must be previewed and explicitly approved.

## Goals

- Let an operator run an AI review of a GitHub PR that produces a
  **structured, local** review artifact (Markdown + JSON) without posting
  anything.
- Classify findings as **blocking**, **non-blocking**, **question**, or
  **praise**, with severity, confidence, and a "commentable" flag.
- Provide a **safe publishing** step that previews the exact comments and
  requires explicit, deterministic approval before any GitHub write, and
  records a receipt so re-runs do not duplicate comments.
- Keep the model layer **provider-agnostic**: OpenRouter first, but the
  config represents any OpenAI-compatible chat/completions endpoint.
- Ship a fixture-based **evaluation harness** so prompt/model changes are
  regression-tested offline.
- Expose the capability through a human-facing **`/review-pr`** verb.

## Non-goals

- Full-codebase indexing or retrieval. v1 is diff-first (plus PR
  metadata); deep-context review is deferred.
- Automated remediation — turning unresolved review comments back into a
  Claude Code implementation prompt — is a separate, later feature.
- A GitHub Actions auto-poster that comments on every `pull_request`
  event. The earlier sketch in ADR-046 chose that shape; M5 supersedes it
  with the operator-driven, dry-run-first flow (see **ADR impact**).
- Non-GitHub review providers (GitLab/Bitbucket). The kit stays
  GitHub-first (ADR-004).
- Wiring the new runtime assets into the installer for target projects
  (see **Migration and compatibility notes**).

## What changes

- A new programmatic surface: `bin/review-pr` (generate a dry-run review
  artifact), `bin/publish-review` (preview/approve/post), and
  `bin/review-eval` (offline fixture evaluation) — all speaking the
  standard `bin/*` JSON envelope (ADR-047).
- A new provider-config model (`schemas/ai-review-config.v1.yaml` +
  `ai-review/config.example.json`): provider name, base URL, model, the
  **name of the env var** that holds the API key (never the key itself),
  timeout, diff-size budget, and review profile.
- A review-artifact contract (`schemas/ai-review-artifact.v1.yaml`) shared
  by the generator and the publisher.
- A review quality rubric and prompt pack under `ai-review/prompts/`
  with `strict` / `balanced` / `lightweight` profiles.
- A `/review-pr` skill (the `/review-pr` verb) that guides provider setup,
  dry-run review, artifact inspection, and approved publishing.
- Publishing writes an idempotency **receipt** (`docs/receipts.md`,
  ADR-050) keyed by PR + artifact hash.
- A new ADR (ADR-051) recording the implemented architecture and
  superseding ADR-046.

## What does not change

- The scoping → backlog → implement → ship loop and every existing skill
  are untouched. `/pr-review-packager` still drafts and opens the PR; the
  review capability reads the resulting PR and is purely additive.
- The permission-category model (ADR-041) and the canonical approval gate
  and operating modes (ADR-048) are unchanged — AI review slots into them:
  generating a review is local/reversible; posting comments is a cat-3
  GitHub write that always requires explicit approval.
- The standard `bin/*` envelope, exit codes, and receipt schema (ADR-047,
  ADR-050) are reused as-is; no schema is modified.
- The new-project-only scope (ADR-002, ADR-022) is unchanged — this
  operates on a project the kit already owns.
- No secret is ever committed or requested in chat; the kit's existing
  GitHub-first posture (ADR-004) is preserved.

## Affected assumptions

- ADR-046 assumed AI review would be a **GitHub Actions auto-poster bound
  to OpenRouter only, with no provider portability in v1**. M5 changes
  that assumption on two points: (1) the delivery mechanism is an
  operator-driven, dry-run-first local flow rather than an event-triggered
  auto-poster, and (2) the model layer is provider-agnostic
  (OpenAI-compatible), with OpenRouter as the first configured provider.
  The GitHub-first and diff-first assumptions are retained.

## ADR impact

- **Create: ADR-051 — Operator-driven, provider-agnostic AI PR review.**
  Records the dry-run-first, approval-gated, receipt-backed local flow and
  the provider-agnostic config model.
- **Revise (via supersession): ADR-046 → ADR-051.** ADR-046's GitHub
  Actions / OpenRouter-only shape is superseded. ADRs are never edited in
  place; ADR-046's status flips to `superseded by ADR-051` and its body
  stays as the historical record.
- **No change but relevant:** ADR-004 (GitHub-first, extended not
  contradicted), ADR-041 (permission contract — publishing is cat-3),
  ADR-047 (bin envelope reused), ADR-048 (deterministic approval token
  reused for the publish confirmation), ADR-049 (this addendum is its
  first dogfood), ADR-050 (receipts reused).

## User stories

- As a maintainer, I run `/review-pr 42` and get a local Markdown review
  of PR #42 — blocking issues first — **without anything posted to
  GitHub**, so I can read it before deciding what to share.
- As a maintainer, after reading the artifact I publish only the
  high-confidence findings, seeing the exact comments first and giving an
  explicit confirmation, so nothing surprises me on the PR.
- As a maintainer who re-runs the publish step, the kit detects the prior
  receipt and refuses to post duplicates unless I force it.
- As an agent, I read the review artifact JSON and the `commentable` flags
  to decide what to surface, without re-parsing the diff.
- As a kit maintainer, I run the eval harness offline before changing the
  prompt pack, so I know the reviewer still catches seeded issues and
  stays quiet on docs-only diffs.

## Requirements

**Functional**

1. `bin/review-pr --pr N` fetches the PR diff + metadata (via `gh`, or a
   supplied `--diff` file for offline use), calls the configured provider
   (or a supplied `--mock` response), and writes a JSON + Markdown artifact
   locally. It posts nothing.
2. The JSON artifact includes summary, and per finding: classification,
   severity, category, file, line (or null), title, detail, suggestion,
   confidence, and `commentable`.
3. `bin/publish-review --artifact F` previews the exact top-level review
   body and inline comments. Posting requires an explicit, deterministic
   `--confirm publish-pr-N` token; findings without a valid diff line go to
   the top-level body, never a broken inline comment.
4. Publishing writes a receipt (PR, artifact hash, review/comment ids,
   timestamp, provider, model) and refuses to re-post the same artifact
   unless `--force`.
5. `bin/review-eval` runs the generator against fixtures (docs-only,
   simple bugfix, risky change, large noisy diff) in mocked mode and
   checks expected finding categories and duplicate-comment prevention,
   without touching a real PR.
6. The `/review-pr` skill explains dry-run vs publish, points to provider
   setup when credentials are missing (never asking for secrets in chat),
   and records the artifact path + next action.

**Non-functional**

7. No secret value in any tracked file; the API key is read from the env
   var named by the config.
8. With no credential configured, `bin/review-pr` fails with a clear setup
   message (exit 3), not a stack trace.
9. Oversized diffs are truncated with an explicit, logged notice rather
   than failing silently.
10. All three scripts pass `bash -n`, emit the standard envelope under
    `--format json`, and are covered by `bin/self-test` offline.

## Migration and compatibility notes

Purely additive; no migration. Expected version bump: **minor** (new
optional capability, no breaking change). The `/review-pr` skill ships to
target projects through the existing `skills/` copy in the installer. The
`bin/*` review tools and the `ai-review/` assets are **kit-level** in this
addendum (like `bin/prepare-issue` and the other programmatic surfaces);
copying them into target projects behind an installer flag is a deferred
follow-up recorded in **Open questions**, not a blocker for M5.

## Issue decomposition

1. **Issue 22** — this PRD addendum (deps: none; non-goal: implementation).
2. **Issue 23** — provider-agnostic config model + schema + setup docs
   (deps: 22; non-goal: posting to GitHub).
3. **Issue 24** — `bin/review-pr` dry-run generator + artifact schema
   (deps: 23; non-goal: any GitHub write).
4. **Issue 26** — review rubric + prompt pack with profiles
   (deps: 23; non-goal: model orchestration).
5. **Issue 25** — `bin/publish-review` preview/approve/receipt path
   (deps: 24; non-goal: auto-posting without approval).
6. **Issue 27** — `bin/review-eval` fixture harness
   (deps: 24, 26; non-goal: live model calls).
7. **Issue 28** — `/review-pr` skill (deps: 24, 25; non-goal: new provider
   integrations beyond the config model).

## Success metrics

- A dry-run review of a PR produces a local artifact and posts nothing.
- Findings are classified blocking / non-blocking / question / praise.
- Publishing previews the exact comments and requires explicit approval;
  a second publish of the same artifact is refused without `--force`.
- The provider layer is configured for OpenRouter and can represent any
  OpenAI-compatible endpoint (base URL, model, headers, timeout).
- The eval harness runs offline and flags a docs-only diff that invents
  code bugs or a risky diff that misses its seeded high-severity issue.
- No secret is committed; missing credentials fail with a setup message.

## Open questions

- Installer distribution: should a `--with-ai-review` flag copy
  `ai-review/` + the review `bin/*` tools into target projects, or should
  these stay kit-level and be invoked from a cloned kit? (Deferred; M5
  keeps them kit-level.)
- Real diff **chunking** for very large PRs (M5 truncates with a logged
  notice; map/reduce summarization is a follow-up).
- Whether to offer a non-interactive "autonomous publish" policy gated by
  an explicit per-repo opt-in (kept out of M5 — approval is always
  required).
