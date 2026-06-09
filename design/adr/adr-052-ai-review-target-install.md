# ADR-052: Target-local AI review installer option

**Status:** accepted

## Context

ADR-051 accepted the operator-driven AI PR review safety model, but deferred
installer distribution of the review runtime. That left target projects in a
confusing halfway state: the `/review-pr` skill could appear without the
scripts, prompt pack, receipt helper, and config layout needed to run it from
the target repository.

The runtime also has path-sensitive behavior. `review-pr` derives `KIT_ROOT`
from its script location; when installed at `.claude/bin/review-pr`, the
prompt pack and config must resolve under `.claude/`, not the original kit
source tree.

## Decision

AI PR review is a default-off, explicit install-time option:

```bash
bin/install-workflow-kit --with-ai-review
```

Default installs do not install the review runtime and do not expose a
target-local `/review-pr` skill.

When enabled, the installer copies the complete runtime into the target under
`.claude/`:

- `.claude/bin/review-pr`
- `.claude/bin/publish-review`
- `.claude/bin/review-eval`
- `.claude/bin/write-receipt`
- `.claude/bin/lib/json-envelope.sh`
- `.claude/bin/lib/review-*.py` and `review_common.py`
- `.claude/ai-review/prompts/`
- `.claude/ai-review/eval/`
- `.claude/ai-review/config.example.json`
- `.claude/schemas/ai-review-*.yaml` as reference schemas
- `.claude/skills/review-pr/`

The chosen layout is `.claude/ai-review/`, matching `KIT_ROOT` derivation
from `.claude/bin/*` scripts. Generated artifacts live under
`.claude/ai-review/artifacts/`.

Provider config remains secret-free. The installer may create or refresh
`config.example.json`, but it must not create a real `config.json`. If a user
creates `.claude/ai-review/config.json`, `--force` preserves it.

Target `.gitignore` ignores generated artifacts and user-local review config:

```gitignore
.claude/ai-review/artifacts/
.claude/ai-review/config.json
```

## Consequences

- Operators make an all-or-nothing per-target choice instead of receiving a
  half-installed feature.
- The target layout works without the kit source repo because scripts resolve
  prompt/config assets relative to `.claude/`.
- Tests must cover both default and `--with-ai-review` installs.
- Mocked review checks are not enough; regression coverage must also exercise
  prompt-pack resolution and receipt-writing dependencies.
- Existing user config is protected across forced refreshes.

## Safety model

This ADR does not change ADR-051's safety model:

- review generation is dry-run by default
- publishing requires explicit `--confirm publish-pr-N`
- receipts make posting idempotent
- API keys are read only from environment variables named by config
- API keys are never written by the installer or requested in chat
