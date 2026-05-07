
# ADR-017: /release skill for version tagging and GitHub Releases

**Status:** accepted
**Date:** 2026-04-17

## Context

No skills exist for versioning, releasing, or tagging. Projects reach "merge to main" but have no structured path to tagged releases. The `/changelog` skill (ADR-016) generates release-note content but nothing orchestrates the actual release — creating the git tag, pushing it, and publishing a GitHub Release.

## Options considered

### Option A: Full end-to-end /release skill

- Pros: one command covers tag, changelog, and GitHub Release; consistent and repeatable.
- Cons: larger skill surface, must handle edge cases (dirty worktree, existing tags).

### Option B: Lightweight script that tags and delegates to /changelog

- Pros: simpler implementation, reuses existing skill.
- Cons: two manual steps, easy to forget the GitHub Release half.

### Option C: Document convention only

- Pros: zero code.
- Cons: manual, error-prone, no consistency across projects.

## Decision

Implement a full `/release` skill. It determines the next semver bump (from user input or a suggestion based on ADR impact since the last tag), calls `/changelog` to generate release notes, creates an annotated git tag, pushes the tag, and creates a GitHub Release via `gh release create`. Optionally updates the build-out plan phase status to mark the release milestone complete.

## Consequences

- Users get a single command to go from merged main to a published GitHub Release.
- The skill depends on `gh` and on the `/changelog` skill (ADR-016).
- Semver suggestion logic must be conservative — it proposes, the user confirms.
- Aligns with the GitHub-first model (ADR-004) by using native GitHub Releases.
