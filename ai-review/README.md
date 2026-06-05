# `ai-review/` — AI PR review assets

The non-code assets for the kit's AI PR review capability (Milestone M5,
[ADR-051](../design/adr/adr-051-operator-driven-ai-pr-review.md)). The
operator-facing guide is [`docs/ai-review.md`](../docs/ai-review.md); the
human verb is `/review-pr` ([`skills/review-pr/`](../skills/review-pr/)).

| Path | What it is |
|---|---|
| `config.example.json` | Copy to `config.json` and edit. Secret-free; names the env var that holds the API key (`schemas/ai-review-config.v1.yaml`). |
| `prompts/system.md` | Base system prompt; pins the JSON output contract. |
| `prompts/rubric.md` | Review quality rubric — what to look for, how to classify, what not to comment on. |
| `prompts/profiles.md` | `strict` / `balanced` / `lightweight` comment-threshold profiles. |
| `eval/` | Offline fixture harness inputs for `bin/review-eval`. |
| `artifacts/` | Generated review artifacts (gitignored, regenerable). |

The programmatic surfaces that consume these assets are
[`bin/review-pr`](../bin/review-pr) (generate a dry-run artifact),
[`bin/publish-review`](../bin/publish-review) (preview / approve / post),
and [`bin/review-eval`](../bin/review-eval) (offline evaluation).

**Secrets never live here.** The API key is read at call time from the
environment variable named by `apiKeyEnv` in the config. No key value is
ever written to a tracked file. See [`docs/ai-review.md`](../docs/ai-review.md).
