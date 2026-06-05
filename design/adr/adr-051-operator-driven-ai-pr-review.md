# ADR-051: Operator-driven, provider-agnostic AI PR review

**Status:** accepted
**Date:** 2026-06-05
**Supersedes:** [ADR-046](adr-046-ai-pr-review-module.md)

## Context

[ADR-046](adr-046-ai-pr-review-module.md) recorded a forward-looking v1
shape for the optional AI PR review module: a GitHub Actions workflow
(`.github/workflows/ai-pr-review.yml`) that runs on `pull_request`
events, calls OpenRouter, and posts a review back to the PR, gated by an
`ai-review-skip` label and a `--with-ai-review` installer flag. It
explicitly chose OpenRouter with **no provider portability in v1** and an
**auto-poster** delivery model.

Milestone M5 (roadmap Issues 22–28) implements AI PR review for real, and
two of its requirements diverge from ADR-046's recorded shape:

1. **Safety model.** The roadmap and this repo's operating rules require
   that review *generation* may be automated but every write to GitHub is
   **dry-run-first and explicitly approved by default**, with receipts to
   prevent duplicate comment spam. An event-triggered auto-poster inverts
   that default: it writes to the PR automatically on every push.
2. **Provider portability.** Issue 23 requires a **provider-agnostic**
   config built around OpenAI-compatible chat/completions endpoints, with
   OpenRouter as the first provider — directly reversing ADR-046's
   "no provider portability in v1".

ADR-046 was recorded with `Target: future` precisely so the concrete
contract could be set when implementation began. Implementation has begun,
and the concrete contract differs enough — delivery mechanism and provider
model both change — that the honest record is a superseding ADR, not an
in-place edit. This ADR records the implemented architecture. The feature
enters through the follow-up PRD workflow (ADR-049) as PRD addendum
[`001-ai-pr-review.md`](../prd-addenda/001-ai-pr-review.md).

## Options considered

### Option A: Operator-driven local flow — generate, preview, approve, publish (chosen)

Three `bin/*` surfaces plus a `/review-pr` skill. `bin/review-pr` fetches
the diff and produces a **local** Markdown+JSON artifact and posts
nothing. `bin/publish-review` previews the exact comments and posts only
on an explicit, deterministic `--confirm publish-pr-N` token, writing an
idempotency receipt. `bin/review-eval` exercises the generator offline
against fixtures. Provider config is a secret-free file naming the env var
that holds the key.

- Pros: matches the dry-run-first / explicit-approval safety model the
  roadmap and operating rules demand; reuses the existing `bin/*` envelope
  (ADR-047), receipts (ADR-050), deterministic approval tokens (ADR-048),
  and permission categories (ADR-041) instead of inventing a parallel
  GitHub Actions surface; provider-agnostic from day one; fully testable
  offline via `--mock`/`--diff`, so it runs in CI without secrets or a
  live PR; no diff leaves the operator's machine until they approve.
- Cons: not automatic — a human runs it per PR rather than it firing on
  every push (acceptable, and the point); the review `bin/*` tools and
  `ai-review/` assets are kit-level in M5 (the `/review-pr` skill ships to
  targets, the tools do not yet), so target-project distribution is a
  deferred follow-up.

### Option B: Keep ADR-046's GitHub Actions auto-poster

- Pros: zero-touch once configured; review appears automatically on the PR.
- Cons: contradicts the safety model — it writes to GitHub without a
  preview-and-approve gate by default; harder to test offline (needs the
  Actions runner and live secrets); locks the kit to OpenRouter and the
  GitHub Actions surface, duplicating rather than reusing the kit's
  existing envelope/receipt/approval machinery. Rejected.

### Option C: Hybrid — local generation, Actions for publishing

- Pros: local dry-run plus an automated post path.
- Cons: two delivery mechanisms to maintain and document for one feature;
  the Actions path still needs the approval gate to be safe, at which
  point it adds complexity without changing the safety contract.
  Premature per CLAUDE.md ("no speculative abstractions"). Rejected for
  v1; can be reconsidered once the local flow has produced real reviews.

## Decision

Adopt **Option A**.

**Surfaces.** Three kit-level `bin/*` scripts, each emitting the standard
JSON envelope (ADR-047) and sourcing `bin/lib/json-envelope.sh`:

- `bin/review-pr --pr N [--diff FILE] [--mock FILE] [--format json|md]
  [--profile …] [--out DIR]` — gather the diff (via `gh pr diff`/`gh pr
  view`, or `--diff` for offline use), call the configured provider (or
  use `--mock` to skip the network), validate the model output against the
  artifact schema, and write `ai-review/artifacts/pr-N-<hash>.{json,md}`.
  It **writes only local files and never posts**. Exit 3 with a setup
  message when no credential is configured.
- `bin/publish-review --artifact F [--pr N] [--confirm publish-pr-N]
  [--force] [--mock]` — by default **preview only**: print the exact
  top-level review body and the inline comments, post nothing. Posting
  requires the deterministic `--confirm publish-pr-N` token (ADR-048).
  Findings whose file/line is not in the diff go to the top-level body,
  never a broken inline comment. On post, write a receipt (ADR-050) keyed
  by PR + artifact hash; a matching `completed` receipt blocks a duplicate
  post unless `--force`.
- `bin/review-eval [--fixtures DIR]` — run the generator in mocked mode
  over fixtures (docs-only, simple bugfix, risky change, large noisy diff)
  and check expected finding categories and duplicate-comment prevention.

**Skill.** `skills/review-pr/` exposes the `/review-pr` verb. It is
**permission-category 3**: although its default action (dry-run generation)
is local and reversible, the skill's terminal capability is posting
comments to a PR — a GitHub write — so it is categorised by its
highest-impact action, consistent with the kit's other GitHub-writing
skills (`issue-planner`, `pr-review-packager`, `release`), each of which
offers a `--dry-run` safety valve within a cat-3 skill. The dry-run review
is that safety valve here, and publishing always requires explicit
approval regardless of operating mode (ADR-041, ADR-048).

**Provider model.** Config is a secret-free JSON file
(`ai-review/config.example.json`, schema
`schemas/ai-review-config.v1.yaml`): `provider`, `baseURL`, `model`,
`apiKeyEnv` (the **name** of the env var holding the key — never the key),
`timeoutSeconds`, `maxDiffBytes`, `profile`, and optional `headers`. The
default is OpenRouter (`https://openrouter.ai/api/v1`,
`OPENROUTER_API_KEY`); any OpenAI-compatible endpoint is representable.
The key is read from the named env var at call time; no secret is ever
written to a tracked file or requested in chat.

**Artifact + rubric.** The review artifact
(`schemas/ai-review-artifact.v1.yaml`) classifies each finding as
blocking / non-blocking / question / praise with severity, category,
file, line, suggestion, confidence, and a `commentable` flag. The prompt
pack (`ai-review/prompts/`) carries the rubric and `strict` / `balanced` /
`lightweight` profiles that move the comment threshold.

**Deferrals.** Full-codebase context, automated comment remediation, real
diff chunking (M5 truncates oversized diffs with a logged notice), and
installer distribution of the review tools into target projects are
deferred, recorded in the addendum's Open questions and
`notes/feature-ideas.md`.

## Consequences

- Easier: review becomes the first lifecycle stage with safe,
  kit-shaped support; the safety model (dry-run, approve, receipt) reuses
  existing kit machinery rather than a parallel surface; the whole flow is
  testable offline and in CI without secrets or a live PR; the provider
  layer is portable from day one.
- Harder: review is operator-invoked per PR, not automatic; the review
  `bin/*` tools and `ai-review/` assets are kit-level in M5, so a
  follow-up is needed to distribute them to target projects; an external
  model API and a secret-management path (an env var, not a committed key)
  enter the kit's surface.
- Maintain: three new `bin/*` scripts and their registration in
  `kit.json`; two new schemas under `schemas/`; the `ai-review/` prompt
  pack, config example, and eval fixtures; one new skill; `docs/ai-review.md`
  and the verb-layer / skills-reference entries; `bin/self-test` gains
  offline coverage of the three scripts.
- Superseded: ADR-046's GitHub Actions auto-poster and OpenRouter-only,
  no-portability shape. ADR-046 remains in the record as the historical
  v1 sketch; its status is `superseded by ADR-051`.
