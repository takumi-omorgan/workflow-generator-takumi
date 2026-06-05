# `ai-review/eval/` — offline evaluation fixtures

Fixtures for [`bin/review-eval`](../../bin/review-eval) (Milestone M5,
Issue 27, ADR-051). The harness runs the review generator in **mocked,
offline** mode — no network, no GitHub, no API key — and checks that the
resulting artifact meets each fixture's expectations. It guards against a
prompt or model change quietly making the reviewer noisier or less useful.

## Layout

Each `fixtures/<name>/` directory contains:

| File | Purpose |
|---|---|
| `input.diff` | The unified diff to review. |
| `mock-response.json` | The model reply `bin/review-pr --mock` is fed (skips the network). |
| `expectations.json` | Assertions about the generated artifact (see below). |
| `config.json` | Optional provider config override (e.g. a small `maxDiffBytes` to exercise truncation). |

## Fixtures

- **docs-only** — a docs change. The reviewer must **not** invent
  code-level bugs and must not block.
- **simple-bugfix** — a correct fix. No blocking findings; the reviewer
  should flag the missing regression test.
- **risky-change** — an auth check removed before a destructive delete.
  At least one high-severity **blocking** finding, posted inline.
- **large-noisy** — whitespace churn hiding one real regression. The
  reviewer finds the bug, stays quiet on noise, and the oversized diff is
  safely truncated.

## Expectation keys (`expectations.json` → `expect`)

| Key | Meaning |
|---|---|
| `minBlocking` / `maxBlocking` | Bounds on blocking-finding count. |
| `minFindings` / `maxFindings` | Bounds on total findings (noise discipline). |
| `requireCategories` | Each listed category must appear in some finding. |
| `forbidCategories` | None of these categories may appear. |
| `requireSeverity` | At least one finding at this severity. |
| `minCommentable` / `maxCommentable` | Bounds on inline-eligible findings. |
| `truncated` | Required value of the artifact's `truncated` flag. |

The harness also runs a **duplicate-publish** check: publishing one
fixture's artifact twice (in a throwaway receipts dir, via
`bin/publish-review --mock`) must succeed once and then be refused, proving
duplicate-comment prevention without touching a real PR.

Run it: `bin/review-eval` (text) or `bin/review-eval --format json`.
