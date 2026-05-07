
# ADR-004: Use a GitHub-first workflow model

**Status:** accepted
**Date:** 2026-04-12

## Context

The workflow kit is intended to support project delivery in a practical, widely used software-development environment. Your existing workflow documents are already optimized for GitHub issues, labels, pull requests, and a `main + feature branch` model, and the value of the kit depends on turning planning artifacts into actionable GitHub work items.

## Options considered

### Option A: Keep the workflow fully generic across SCM and issue tools

- Pros: broader compatibility.
- Cons: less actionable, weaker documentation, more abstract outputs, and less fit with the current workflow design.

### Option B: Optimize v1 for GitHub

- Pros: stronger and clearer workflow guidance, more actionable outputs, better issue/PR templates, and alignment with the existing operating model.
- Cons: less useful for teams using other platforms.

## Decision

Use a **GitHub-first workflow model** in v1. The kit should assume:

- GitHub repositories,
- GitHub issues,
- labels and milestones,
- pull requests,
- a `main + feature branch` model,
- and optional branch protection.

## Consequences

- The documentation can include concrete GitHub setup instructions.
- Templates can be written for `.github/` conventions.
- The issue planner can produce GitHub-native outputs.
- Generic support for other platforms is deferred to a later phase.
