---
name: review-pr
description: Run an AI-assisted review of a GitHub PR. Generates a local, dry-run review artifact (Markdown + JSON) from the PR diff using a configured OpenAI-compatible provider (OpenRouter first), classifies findings as blocking / non-blocking / question / praise, and — only after you review the preview and give explicit approval — publishes review comments to GitHub. Safe by default: review generation posts nothing; publishing is a cat-3 GitHub write that always requires explicit approval.
permission-category: 3  # non-substitutable — the skill's terminal action posts comments to a PR (a GitHub write); the dry-run review is the cat-3 safety valve, like --dry-run on issue-planner/release, per ADR-051 and workflow-guide §7
inputs:
  - name: "pr"
    required: true
    description: "The PR number to review (e.g. 42 or #42)"
  - name: "--profile"
    required: false
    description: "Review depth: strict | balanced (default) | lightweight"
  - name: "--publish"
    required: false
    description: "After the dry-run, offer to publish — still requires explicit approval before any GitHub write"
outputs:
  - artefact: ".claude/ai-review/artifacts/pr-N-<hash>.json"
    description: "Structured review artifact (also rendered as .md); local, posts nothing"
  - artefact: "(GitHub PR review)"
    description: "Posted only after explicit approval; records a receipt under .claude/receipts/"
next: []
---

# review-pr

Run an AI-assisted review of a GitHub pull request and, if you choose,
publish the comments — **safely**. Review generation is local and posts
nothing; publishing to GitHub requires you to preview the exact comments
and give explicit approval. It is the `/review-pr` verb.

In a target project this skill is installed only when the project was
installed with `--with-ai-review`. In the kit repo it can also dogfood the
repo-local `bin/review-pr` runtime.

## When to use this skill

- You have an open PR and want a structured first-pass review
  (correctness, security, regressions, test coverage) before or alongside
  human review.
- You want the review as a **local artifact** to read first, and to decide
  later whether any of it is worth posting.

## When NOT to use this skill

- For a self-contained human review you will type yourself — just review.
- This is **not** `/pr-review-packager` (which *opens* a PR from a branch).
  `review-pr` reads an already-open PR and reviews it.

## Inputs

- **Required:** the PR number.
- **Optional:** `--profile strict|balanced|lightweight`, `--publish`.
- **Provider config (read):** `.claude/ai-review/config.json` in target
  projects, or `ai-review/config.json` in the kit repo. The API key is read
  from the env var named by `apiKeyEnv` — **never** ask the user to paste a
  key into chat, and never commit one. If the key is missing, point the user
  to the AI-review setup docs and stop.

## Runtime resolution

Before running commands, resolve the runtime path:

```bash
if [ -x .claude/bin/review-pr ]; then
  REVIEW_PR=.claude/bin/review-pr
  PUBLISH_REVIEW=.claude/bin/publish-review
elif [ -x bin/review-pr ]; then
  REVIEW_PR=bin/review-pr
  PUBLISH_REVIEW=bin/publish-review
else
  echo "AI PR review runtime is not installed. Re-run bin/install-workflow-kit --with-ai-review for this target project." >&2
  exit 2
fi
```

Use `$REVIEW_PR` and `$PUBLISH_REVIEW` in the protocol below, not hardcoded
repo-local paths.

## What this skill produces

1. A **dry-run review artifact** at `.claude/ai-review/artifacts/pr-N-<hash>.json`
   in target projects (and `.md`), with a summary and findings classified
   **blocking / non-blocking / question / praise**, each with severity,
   category, file/line, suggestion, confidence, and a `commentable` flag.
2. **Only on explicit approval:** a GitHub PR review with the previewed
   comments, plus an idempotency receipt under `.claude/receipts/`.

## Protocol

1. **State the mode up front.** Tell the user this run is a *dry-run* that
   posts nothing unless they later approve publishing. Default to dry-run.
2. **Preflight provider config.** Confirm a config exists and the key env
   var is set (`review-pr` exits 3 with a setup message if not). If missing,
   explain how to copy `.claude/ai-review/config.example.json` to
   `.claude/ai-review/config.json`, export the env var named by `apiKeyEnv`,
   and stop — do not ask for secrets in chat.
3. **Generate the review (cat-1, safe):**

   ```bash
   "$REVIEW_PR" --pr N --profile balanced --format md
   ```

   This fetches the diff via `gh`, calls the provider, and writes the
   artifact. Show the user the rendered Markdown and the artifact path.
4. **Inspect together.** Summarise blocking findings first. Note how many
   findings are `commentable` (high-confidence, located) vs. summary-only.
5. **Decide on publishing.** If the user does not want to publish, stop —
   the artifact is the deliverable. If they do, continue.
6. **Preview the exact comments (still posts nothing):**

   ```bash
   "$PUBLISH_REVIEW" --artifact .claude/ai-review/artifacts/pr-N-<hash>.json --pr N
   ```

   Show the exact top-level body and inline comments.
7. **Get explicit approval, then publish (cat-3).** Publishing is a GitHub
   write and **always** requires an explicit `yes`, regardless of operating
   mode. Only after approval, post with the deterministic token:

   ```bash
   "$PUBLISH_REVIEW" --artifact .claude/ai-review/artifacts/pr-N-<hash>.json \
     --pr N --confirm publish-pr-N
   ```

   The publisher refuses to re-post the same artifact (a receipt exists)
   unless `--force`. Findings without a valid diff line are folded into the
   top-level body, never posted as broken inline comments.

## Safety rules (non-negotiable)

- **Never** ask the user to paste an API key into chat; **never** commit a
  key. Keys live only in the env var named by the config.
- **Dry-run before any GitHub write.** Always generate and preview first.
- **Explicit approval before posting**, in every operating mode. The
  `--confirm publish-pr-N` token is the deterministic approval gate.
- **Receipts.** A successful post writes a receipt; re-runs are idempotent.

## Handoff

The artifact path and the next recommended action are reported by
`review-pr`. After publishing, the receipt under `.claude/receipts/` records
what was posted. See `example.md` for a worked dry-run → preview → publish
walk.
