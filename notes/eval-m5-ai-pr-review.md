# Evaluation — Milestone M5 (AI PR review integration)

**Branch:** `m5-ai-pr-review-integration`
**ADR:** ADR-051 (operator-driven, provider-agnostic AI PR review) — supersedes ADR-046
**PRD:** `design/prd-addenda/001-ai-pr-review.md` (first real use of the follow-up PRD workflow, ADR-049)
**Roadmap:** `design/workflow-generator-roadmap-and-issues-20260605.md` §M5 — Issues 22–28

M5 was executed as **one reviewable PR**. The seven issues form one
coherent capability: the provider config feeds the generator, the artifact
schema is the contract between generator and publisher, the rubric/prompt
pack shapes the generator's output, the eval harness regression-tests the
generator, and the skill ties them together. Splitting them would fragment
a single decision (the M2/M4 precedent: one ADR per coherent milestone).

## Plan and decisions

| Roadmap issue | Delivered as | Decision note |
|---|---|---|
| 22 — PRD addendum | `design/prd-addenda/001-ai-pr-review.md` | First dogfood of the follow-up PRD workflow (ADR-049). "What does not change" / "Affected assumptions" / "ADR impact" filled. |
| 23 — provider-agnostic config | `schemas/ai-review-config.v1.yaml` + `ai-review/config.example.json` | Secret-free file; `apiKeyEnv` names the env var, the key value is never stored. OpenAI-compatible transport; OpenRouter default. No key → exit 3 setup message. |
| 24 — dry-run generator | `bin/review-pr` (+ `lib/review-build-request.py`, `lib/review-render.py`, `lib/review_common.py`) | Writes a local JSON+MD artifact, posts nothing. `--diff`/`--mock` make it fully offline. Oversized diffs truncate with a logged `truncated:true`, not silent failure. Commentability recomputed against the actual diff hunks. |
| 25 — safe publish | `bin/publish-review` (+ `lib/review-publish.py`) | Preview by default (posts nothing). Posting needs the deterministic `--confirm publish-pr-N` token (ADR-048). Findings without a valid diff line → top-level body, never broken inline. Idempotent via a receipt (ADR-050) keyed by PR + artifact hash; duplicate refused unless `--force`. |
| 26 — rubric + prompt pack | `ai-review/prompts/{system,rubric,profiles}.md` + `schemas/ai-review-artifact.v1.yaml` | Findings classified blocking/non-blocking/question/praise with severity, category, confidence, commentable. `strict`/`balanced`/`lightweight` profiles move the comment threshold. Docs-only diffs told not to invent code bugs. |
| 27 — eval harness | `bin/review-eval` (+ `lib/review-eval-check.py`) + `ai-review/eval/fixtures/*` | Four fixtures (docs-only, simple-bugfix, risky-change, large-noisy) run offline via `--mock`; checks finding categories, noise discipline, truncation, and duplicate-publish prevention. Wired into `bin/self-test`. |
| 28 — `/review-pr` skill | `skills/review-pr/{SKILL.md,example.md}` | cat-3 (its terminal action is a GitHub write; dry-run is the safety valve, like `--dry-run` on issue-planner/release). Points to provider setup when the key is missing; never asks for secrets in chat. |

### Why ADR-051 supersedes ADR-046

ADR-046 was a forward-looking sketch (GitHub Actions auto-poster, OpenRouter
only, no provider portability, `Target: future`). M5's requirements diverge
on two points the kit's rules say must be honoured by a *new* ADR, not an
in-place edit: (1) the safety model is dry-run-first + explicit approval,
not an event-triggered auto-poster; (2) the provider layer is
provider-agnostic, reversing ADR-046's no-portability stance. ADR-051
records the implemented architecture; ADR-046's status flipped to
`superseded by ADR-051` (status-line flip only, per the ADR-045 precedent).

## Safety posture (operating-rule compliance)

- No secret is committed or requested in chat — keys live only in the env
  var named by the config; `ai-review/config.json` is gitignored.
- Dry-run before any GitHub write; publishing is preview → explicit token →
  receipt.
- **No real PR comments were posted during implementation.** Every publish
  path was exercised with `--mock` (simulated post, no `gh` call) or as a
  no-`--confirm` preview. The real `gh api … /reviews` path is coded and
  `bash -n`-clean but was never executed.

## Checks run

- `bash -n` on all `bin/*` shell scripts; `python3 -c ast.parse` on the
  `bin/lib/review*.py` helpers — clean.
- `bin/validate-kit-json` — in sync (22 skills).
- `bin/check-consistency` — consistent (C1 skills.md, C2 verb layer, C3 bin
  registry incl. the three new envelope scripts, C4 the two new schemas vs
  `docs/ai-review.md`, C5 categories).
- `bin/review-eval` — 4/4 fixtures pass + duplicate-prevention holds.
- `bin/self-test` — ok (now includes review-eval + a review-pr/publish-review
  offline stub + a bad-token refusal).
- `python3 -c "import json"` on `kit.json` and all new JSON.

## Deferred (recorded in ADR-051 / addendum Open questions)

- Installer distribution of the review `bin/*` tools + `ai-review/` assets
  into target projects (kit-level for now; the `/review-pr` skill ships via
  `skills/`).
- Real diff chunking for very large PRs (M5 truncates with a notice).
- Full-codebase context, automated comment remediation, autonomous publish
  policy.

## Friction / notes for next pass

- The diff-line parser had to tolerate whitespace-stripped blank context
  lines (editors strip the leading space git emits); the parser now treats
  a bare empty interior line as blank context after dropping only the
  trailing-newline artifact. Worth keeping in mind if a future surface
  re-parses diffs.
- `check-consistency` C4 uses a hard-coded schema→home map; adding a schema
  means editing that map. A future improvement could derive it from each
  schema file's `spec:` field.
