
# ADR-005: Generate documentation and templates directly into the target repository

**Status:** accepted
**Date:** 2026-04-12

## Context

The workflow kit is meant to make a new project immediately usable with Claude Code and GitHub. To do that, it needs to generate the core working documents directly in the target repository, where both the human developer and Claude Code will read them during implementation. Your workflow document already emphasizes `CLAUDE.md`, ADRs, AI summaries, and process templates as repo-local artifacts.

## Options considered

### Option A: Keep most docs in the kit repository only

- Pros: simpler kit maintenance, fewer generated files.
- Cons: weaker per-project integration, more copying by hand, and less repo-specific context for Claude Code.

### Option B: Generate core docs and templates into the target repo

- Pros: stronger integration, clearer project context, and better support for issue-by-issue implementation.
- Cons: more generated files per project, and requires clearer installation/documentation.

## Decision

Generate the core workflow documents and templates directly into the target repository. These should include, at minimum:

- `README.md`
- `CLAUDE.md`
- `design/adr/`
- `design/ai-summary.md`
- workflow docs
- issue and PR templates where appropriate.

## Consequences

- Claude Code gets project-specific context close to the code.
- The repo becomes self-describing and easier to continue later.
- The workflow kit becomes useful even if the user does not fully automate every step.
- Documentation must define the generated file structure clearly.
