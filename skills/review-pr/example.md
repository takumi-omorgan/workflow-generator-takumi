# review-pr — worked example

A dry-run AI review of PR #42, then an approved publish. Nothing is posted
to GitHub until the explicit `--confirm` step.

## 1. Generate a dry-run review (posts nothing)

```bash
$ bin/review-pr --pr 42 --profile balanced --format md
# AI review — PR #42

_provider `openrouter` · model `openai/gpt-4o-mini` · profile `balanced`_

## Summary

Adds a delete endpoint but drops the ownership check; any user can delete
any record. One missing test.

**Findings:** 1 blocking · 1 non-blocking · 0 question · 0 praise

## 🛑 Blocking

### Authorization check removed before delete — `api/records.py:22`

[high/security, confidence high] (inline-commentable)

The ownership guard was deleted, so any authenticated user can delete any
record by id.

**Suggested fix:** Restore the ownership check before deleting.
...
```

The artifact is written to `ai-review/artifacts/pr-42-<hash>.json` (and
`.md`). Nothing has touched GitHub.

If the provider key is not set, the command stops cleanly:

```bash
$ bin/review-pr --pr 42
review-pr: no API key — set $OPENROUTER_API_KEY (see docs/ai-review.md), or
pass --mock FILE for offline use.
```

Set the key in your shell (never in a file or in chat):
`export OPENROUTER_API_KEY=...`.

## 2. Preview the exact comments (still posts nothing)

```bash
$ bin/publish-review --artifact ai-review/artifacts/pr-42-<hash>.json --pr 42
publish-review: PREVIEW for PR #42 — nothing has been posted.

--- top-level review body ---
## AI review
...
--- inline comments (1) ---
  api/records.py:22
    **Authorization check removed before delete** [high/security] ...

To post these to GitHub, re-run with:  --confirm publish-pr-42
```

## 3. Publish — only after explicit approval

```bash
$ bin/publish-review --artifact ai-review/artifacts/pr-42-<hash>.json \
    --pr 42 --confirm publish-pr-42
publish-review: posted review 12345 to PR #42 (1 inline comment(s)). Receipt written.
```

Re-running the same publish is refused (idempotent):

```bash
$ bin/publish-review --artifact ai-review/artifacts/pr-42-<hash>.json \
    --pr 42 --confirm publish-pr-42
publish-review: a review for PR #42 with this exact artifact was already
posted (receipt exists). Use --force to post again.
```

## Offline / CI

Both steps run without a network or a real PR using `--mock` (a canned
model reply) and `--diff` (a local diff file). That is how
[`bin/review-eval`](../../bin/review-eval) regression-tests the reviewer.
