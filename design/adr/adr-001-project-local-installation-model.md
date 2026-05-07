
# ADR-001: Use project-local installation for the workflow kit

**Status:** accepted
**Date:** 2026-04-12

## Context

The first release of the Claude Code Workflow Kit needs a simple installation model that is easy for solo developers to understand and use consistently. The product is intended to help set up the workflow for a **specific new project**, not to act as a cross-project platform from day one.

Claude Code supports project-specific skills, which makes it possible to place skills directly in a repository-local `.claude/skills/` directory. A local install keeps the workflow artifacts, instructions, and generated docs close to the target project and reduces ambiguity about where skills should live.

## Options considered

### Option A: Global installation in a personal skills directory

- Pros: install once, reuse across many projects, easier long-term maintenance.
- Cons: harder to explain to first-time users, separates the workflow kit from the project it configures, and introduces personal-environment management too early.

### Option B: Project-local installation in the target repository

- Pros: simplest mental model, all workflow assets live with the project, easy to document, and aligns with the product's project-specific workflow setup goal.
- Cons: requires a fresh install for each new project, and updates are not automatically shared across projects.

## Decision

Use a **project-local installation model** for v1. The user installs the workflow kit into each new target project, and the active Claude Code skills live in that project's `.claude/skills/` directory.

This must be the default usage model in the documentation and examples.

## Consequences

- Each new project gets its own installation of the workflow kit.
- The product is easier to onboard and explain.
- The kit can generate and maintain project docs in place.
- Global or reusable personal installation is deferred to a later iteration.
