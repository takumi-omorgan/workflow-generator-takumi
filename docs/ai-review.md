# AI PR review

The kit can generate an AI-assisted review of a GitHub pull request and —
**only after you preview the exact comments and explicitly approve** —
publish them to the PR. It is safe by default: review generation is local
and posts nothing; publishing is a cat-3 GitHub write gated by an explicit,
deterministic approval token and made idempotent by a receipt.

This capability is governed by
[ADR-051](../design/adr/adr-051-operator-driven-ai-pr-review.md) (which
supersedes ADR-046) and entered the kit through PRD addendum
[`001-ai-pr-review.md`](../design/prd-addenda/001-ai-pr-review.md). The
human entry point is the `/review-pr` verb
([`skills/review-pr/`](../skills/review-pr/)); the assets live under
[`ai-review/`](../ai-review/).

## The three surfaces

| Tool | What it does | Posts to GitHub? |
|---|---|---|
| [`bin/review-pr`](../bin/review-pr) | Generate a dry-run review artifact from the PR diff | **No** |
| [`bin/publish-review`](../bin/publish-review) | Preview, then post on explicit `--confirm` | Only with the token |
| [`bin/review-eval`](../bin/review-eval) | Offline fixture harness for review quality | No |

## 1. Configure a provider (no secrets committed)

The model layer is provider-agnostic: any OpenAI-compatible
chat/completions endpoint works, with **OpenRouter** as the first
provider. Configuration is a small, **secret-free** JSON file. Copy the
example and edit it:

```bash
cp ai-review/config.example.json ai-review/config.json
```

```json
{
  "schema": "ai-review-config",
  "version": 1,
  "provider": "openrouter",
  "baseURL": "https://openrouter.ai/api/v1",
  "model": "openai/gpt-4o-mini",
  "apiKeyEnv": "OPENROUTER_API_KEY",
  "timeoutSeconds": 60,
  "maxDiffBytes": 200000,
  "profile": "balanced"
}
```

The config never contains the key. `apiKeyEnv` names the **environment
variable** that holds it. Export the key in your shell (or your secret
manager); never paste it into chat and never commit it:

```bash
export OPENROUTER_API_KEY=sk-or-...   # in your shell, not in any file
```

The full field list is in the schema,
[`schemas/ai-review-config.v1.yaml`](../schemas/ai-review-config.v1.yaml).
Config resolves in this order (later wins): built-in defaults →
`ai-review/config.json` → `--config FILE` → CLI flags
(`--provider/--model/--base-url/--profile`).

**Another OpenAI-compatible provider?** Set `baseURL`, `model`,
`apiKeyEnv`, and any non-secret `headers`. The transport is the same
`/chat/completions` call.

If no key is set, `bin/review-pr` exits `3` with a setup message rather
than failing obscurely — and never asks you for the key.

## 2. Generate a dry-run review (posts nothing)

```bash
bin/review-pr --pr 42 --profile balanced --format md     # rendered report
bin/review-pr --pr 42 --format json                      # standard envelope
```

It fetches the diff (`gh pr diff`) and metadata (`gh pr view`), calls the
model, validates the reply against
[`schemas/ai-review-artifact.v1.yaml`](../schemas/ai-review-artifact.v1.yaml),
and writes `ai-review/artifacts/pr-42-<hash>.json` and `.md`. Findings are
classified **blocking / non-blocking / question / praise** with severity,
category, file/line, suggestion, confidence, and a `commentable` flag.

Each finding is `commentable` only when it is high-confidence, not praise,
and its file+line actually appear in the diff — so a model that points at a
line it cannot see is never posted inline. Oversized diffs (over
`maxDiffBytes`) are **truncated with an explicit notice** (the artifact
records `truncated: true`) rather than failing silently.

### Review profiles

Set with `--profile` or the config:

- **strict** — everything, including style nitpicks.
- **balanced** (default) — real risk; no style nits.
- **lightweight** — blocking findings only; low noise.

The rubric and profiles are the prompt pack under
[`ai-review/prompts/`](../ai-review/prompts/).

## 3. Publish — preview, approve, post

```bash
# preview the EXACT comments — still posts nothing
bin/publish-review --artifact ai-review/artifacts/pr-42-<hash>.json --pr 42

# post, only after you approve, with the deterministic token
bin/publish-review --artifact ai-review/artifacts/pr-42-<hash>.json \
  --pr 42 --confirm publish-pr-42
```

- **Dry-run is the default.** With no `--confirm`, it prints the top-level
  review body and every inline comment and exits — nothing is posted.
- **Explicit, deterministic approval.** Posting requires
  `--confirm publish-pr-<N>`; any other value is refused (exit 4). This is
  the [ADR-048](../design/adr/adr-048-unified-workflow-control.md)
  deterministic-token gate, and it always applies — in every operating
  mode, a GitHub write needs explicit approval.
- **No broken inline comments.** Findings without a valid diff line are
  folded into the top-level body.
- **Idempotent.** A successful post writes a receipt
  ([`docs/receipts.md`](receipts.md)) keyed by PR + artifact hash; posting
  the same artifact again is refused unless `--force`.

## 4. Evaluate review quality offline

```bash
bin/review-eval                 # text
bin/review-eval --format json
```

Runs the generator in mocked, offline mode over the fixtures in
[`ai-review/eval/fixtures/`](../ai-review/eval/) (docs-only, simple
bugfix, risky change, large noisy diff) and checks each artifact against
the fixture's expectations — e.g. a docs-only diff must not invent code
bugs, a risky diff must surface its seeded high-severity issue. It also
verifies duplicate-comment prevention without touching a real PR. Run it
before changing the prompt pack or model. It is wired into
[`bin/self-test`](../bin/self-test).

## Safety summary

- **No secret is ever committed or requested in chat.** Keys live only in
  the env var named by the config.
- **Dry-run before any GitHub write**, always.
- **Explicit approval before posting**, in every operating mode.
- **Receipts** make publishing idempotent and auditable.

## Offline / CI use

`bin/review-pr --diff FILE --mock FILE` reviews a local diff with a canned
model reply — no network, no key, no GitHub. That is how the eval harness
and `bin/self-test` exercise the whole flow deterministically.

## Scope and deferrals (ADR-051)

v1 is **diff-first** and operator-driven. Deferred: full-codebase context,
automated comment remediation, real diff chunking (v1 truncates), and
copying the review `bin/*` tools into target projects via the installer
(they are kit-level for now; the `/review-pr` skill itself ships with
`skills/`).
