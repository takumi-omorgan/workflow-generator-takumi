
# ADR-003: Support three PRD intake paths

**Status:** accepted
**Date:** 2026-04-12

## Context

Users will not all begin from the same level of planning maturity. Some will have only a rough idea, some will have a clean PRD, and others will have mixed notes or their own custom design format. If the product accepts only one planning format, it will either exclude early-stage users or force too much manual rewriting.

## Options considered

### Option A: Require a standard PRD

- Pros: predictable input structure, easier skill logic.
- Cons: creates friction for users without a formal PRD and adds up-front writing overhead.

### Option B: Support no PRD, standard PRD, and custom PRD

- Pros: lowest adoption friction, supports realistic working styles, and keeps the kit useful at multiple planning stages.
- Cons: requires more skill logic and normalization behavior.

## Decision

Support three entry paths in v1:

1. no PRD yet,
2. standard-format PRD,
3. user-defined PRD format.

This will be handled through separate but related skills: idea capture, PRD normalization, and PRD-to-MVP conversion.

## Consequences

- The kit becomes useful earlier in a project's life.
- Documentation must clearly explain which starting path to choose.
- Skills need to normalize user input into a consistent internal planning structure.
- The workflow remains PRD-first in spirit, even when the product must help create the PRD first.
