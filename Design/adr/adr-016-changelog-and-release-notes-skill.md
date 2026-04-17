
# ADR-016: Auto-generated changelog and release notes skill

**Status:** accepted
**Date:** 2026-04-17

## Context

The v1 commit convention (`<verb> <what> (ADR-NNN, #issue)`) makes the git log human-readable, but there is no way to produce polished release notes for stakeholders. Teams need a summary grouped by feature area or issue, not a raw commit list. No versioning or release workflow currently exists in the kit.

## Options considered

### Option A: Claude Code skill parsing git log

- Pros: leverages Claude's summarization, runs inside the existing toolchain, can output to multiple targets.
- Cons: requires a skill to be authored and maintained.

### Option B: Standalone shell script

- Pros: simple, no Claude dependency.
- Cons: limited formatting, no semantic grouping, harder to maintain for non-trivial changelogs.

### Option C: GitHub Action on tag push

- Pros: fully automated on release.
- Cons: requires CI setup, less flexible for ad-hoc summaries.

### Option D: All three

- Pros: maximum coverage.
- Cons: duplication of effort, harder to keep consistent.

## Decision

Build a **/changelog** Claude Code skill that parses git history between two refs, groups commits by verb, ADR, and issue, and outputs formatted markdown. The skill supports three output targets: stdout, a file (e.g. `CHANGELOG.md`), or a GitHub Release body via `gh release create`. A GitHub Action can be added later if automated release publishing is needed.

## Consequences

- Stakeholders get readable, structured release notes without manual effort.
- The commit convention from the workflow docs becomes directly useful beyond traceability.
- The skill depends on consistent commit message formatting; malformed messages are listed in an "Other" group.
- Aligns with the GitHub-first model (ADR-004) by supporting GitHub Releases as a first-class output target.
