# Workflow Kit Live GitHub + Human Evaluation — 20260608-163948

## Purpose

This report covers the workflow steps that the prior three-project local eval intentionally did not exercise because they require human product decisions or a real GitHub repo with pushes to `main`.

## Scope

- Kit source: `/Users/hermes/workflow-generator-takumi-m5`
- Eval workspace: `/Users/hermes/workflow-kit-github-evals/20260608-163948`
- Scratch repo: `takumi-omorgan/wk-eval-live-github-human-20260608`
- Project: `live-github-human-web-task-board`
- Repo cleanup: left in place for inspection; delete manually after review.

## Summary

- PASS: 12
- FAIL: 0
- NOT RUN: 0
- Final status: complete

## GitHub evidence

```json
{
  "repo": "takumi-omorgan/wk-eval-live-github-human-20260608",
  "issues": [
    {
      "number": 1,
      "state": "OPEN",
      "title": "Implement task model and JSON persistence",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/1"
    },
    {
      "number": 2,
      "state": "OPEN",
      "title": "Implement HTTP routes and board rendering",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/2"
    },
    {
      "number": 3,
      "state": "OPEN",
      "title": "Add smoke test and release notes",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/3"
    }
  ],
  "prs": [
    {
      "baseRefName": "main",
      "headRefName": "issue-1-task-model-json-persistence",
      "number": 4,
      "state": "OPEN",
      "title": "Implement task store persistence",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/pull/4"
    }
  ],
  "releases": [
    {
      "isDraft": false,
      "isPrerelease": false,
      "name": "v0.0.0-eval-20260608-163948",
      "tagName": "v0.0.0-eval-20260608-163948",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/releases/tag/v0.0.0-eval-20260608-163948"
    }
  ],
  "repo_view": {
    "default_branch": "main",
    "full_name": "takumi-omorgan/wk-eval-live-github-human-20260608",
    "html_url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608",
    "permissions": {
      "admin": true,
      "maintain": true,
      "pull": true,
      "push": true,
      "triage": true
    },
    "private": false
  },
  "pr_reviews": {
    "reviews": [
      {
        "author": {
          "login": "takumi-omorgan"
        },
        "authorAssociation": "OWNER",
        "body": "Review result: PASS for live eval. Tests and issue linkage are present; persistence is covered by reload test.",
        "commit": {
          "oid": "a2fa0afb59b1800b1ea08ed9b812759f5e852e2c"
        },
        "id": "PRR_kwDOS0fTjM8AAAABCUYnNw",
        "includesCreatedEdit": false,
        "reactionGroups": [],
        "state": "COMMENTED",
        "submittedAt": "2026-06-08T14:41:31Z"
      }
    ]
  },
  "issue_list_final": [
    {
      "number": 3,
      "state": "OPEN",
      "title": "Add smoke test and release notes",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/3"
    },
    {
      "number": 2,
      "state": "OPEN",
      "title": "Implement HTTP routes and board rendering",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/2"
    },
    {
      "number": 1,
      "state": "CLOSED",
      "title": "Implement task model and JSON persistence",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/1"
    }
  ],
  "issue_1_completion": {
    "comments": [
      {
        "id": "IC_kwDOS0fTjM8AAAABFSvTEA",
        "author": {
          "login": "takumi-omorgan"
        },
        "authorAssociation": "OWNER",
        "body": "Completed by merged live eval PR #4. Closing as part of /complete-milestone path verification.",
        "createdAt": "2026-06-08T14:43:09Z",
        "includesCreatedEdit": false,
        "isMinimized": false,
        "minimizedReason": "",
        "reactionGroups": [],
        "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/1#issuecomment-4650160912",
        "viewerDidAuthor": true
      }
    ],
    "number": 1,
    "state": "CLOSED",
    "title": "Implement task model and JSON persistence",
    "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/issues/1"
  },
  "pr_list_final": [
    {
      "baseRefName": "main",
      "headRefName": "issue-1-task-model-json-persistence",
      "number": 4,
      "state": "MERGED",
      "title": "Implement task store persistence",
      "url": "https://github.com/takumi-omorgan/wk-eval-live-github-human-20260608/pull/4"
    }
  ],
  "release_list_final": [
    {
      "isDraft": false,
      "isPrerelease": false,
      "name": "v0.0.0-eval-20260608-163948",
      "tagName": "v0.0.0-eval-20260608-163948"
    }
  ]
}
```

## Evaluated steps

### 1 — install-workflow-kit + GitHub remote setup
- Status: **PASS**
- Mode: live GitHub
- Inputs: empty scratch repo with real origin/main
- Artifacts:
  - `CLAUDE.md`
  - `.claude/skills/`
  - `.github/pull_request_template.md`
- Checks:
  - Repo API view succeeded
  - Initial kit commit pushed to origin/main
  - Workflow kit artifacts exist

### 2 — /idea-to-prd
- Status: **PASS**
- Mode: human-gated fixture
- Inputs: `eval/human-script.md` product answers
- Artifacts:
  - `eval/human-script.md`
  - `design/prd.md`
- Checks:
  - PRD created with goals, non-goals, acceptance criteria
  - Human decisions preserved

### 3 — /prd-normalizer + /prd-to-mvp
- Status: **PASS**
- Mode: human-gated fixture
- Inputs: approved PRD scope
- Artifacts:
  - `design/mvp.md`
- Checks:
  - MVP created
  - MVP narrows scope and defers non-goals

### 4 — /adr-writer + sync-adr-index
- Status: **PASS**
- Mode: human-gated fixture + local executable
- Inputs: storage decision from human fixture
- Artifacts:
  - `design/adr/adr-001-json-file-persistence.md`
  - `design/adr/README.md`
- Checks:
  - sync-adr-index --check rc=0

### 5 — /pause + /resume state shape
- Status: **PASS**
- Mode: human-gated fixture
- Inputs: session continuity checkpoint
- Artifacts:
  - `design/state.md`
- Checks:
  - State marker fences present
  - Next action points to issue planning

### 6 — /planning + /issue-planner
- Status: **PASS**
- Mode: live GitHub
- Inputs: build-out plan backlog
- Artifacts:
  - `design/build-out-plan.md`
- Checks:
  - Created 3 real GitHub issues

### 7 — /prepare-issue
- Status: **PASS**
- Mode: live GitHub
- Inputs: GitHub issue #1
- Artifacts:
  - `prompts/issue-001-task-model-json-persistence.md`
- Checks:
  - Canonical prompt path prompts/issue-001-task-model-json-persistence.md used

### 8 — /claude-issue-executor
- Status: **PASS**
- Mode: live GitHub branch
- Inputs: Issue #1
- Artifacts:
  - `app/store.py`
  - `tests/test_store.py`
- Checks:
  - Unit tests pass
  - Feature branch commit created
  - Main not modified directly

### 9 — /pr-review-packager
- Status: **PASS**
- Mode: live GitHub
- Inputs: Branch for issue #1
- Checks:
  - Created PR #4
  - PR targets main
  - PR body contains verification evidence

### 10 — /review-pr
- Status: **PASS**
- Mode: live GitHub
- Inputs: PR #4
- Checks:
  - Submitted real PR review comment
  - Review checked tests, issue linkage, persistence evidence

### 11 — merge to main + /complete-milestone path
- Status: **PASS**
- Mode: live GitHub
- Inputs: PR #4
- Checks:
  - PR squash-merged
  - Local main fast-forwarded from origin/main
  - Issue #1 closed with completion comment
- Notes: f88e340 feat: implement task store persistence (#4)
affae2d chore: install workflow kit (project-local)

### 12 — /changelog + /release
- Status: **PASS**
- Mode: live GitHub
- Inputs: Merged main at v0.0.0-eval-20260608-163948
- Artifacts:
  - `CHANGELOG.md`
- Checks:
  - CHANGELOG committed and pushed to main
  - Release v0.0.0-eval-20260608-163948 created against main

## Findings

- Live GitHub setup, issue creation, PR creation, review comment, squash merge to `main`, changelog update, and release creation were exercised against the scratch repo.
- Human-gated steps were evaluated with a scripted human fixture. This validates artifact handling and scope preservation, but not full conversational UX inside an actual Claude Code PTY session.
- This should remain a separate live E2E lane from local/offline fixture evals because it has real GitHub side effects.

## Cleanup

- Scratch GitHub repo was intentionally left in place for inspection.
- Local eval workspace retained at the path above for audit/debugging.
