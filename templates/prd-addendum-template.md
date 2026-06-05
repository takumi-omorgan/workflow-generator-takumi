<!--
  Template: Follow-up PRD addendum
  Filled by: feature-prd
  Output in a target project: design/prd-addenda/NNN-<feature-name>.md

  Purpose. Capture a major feature update as an ADDITIVE addendum that
  extends design/prd.md rather than replacing it (ADR-049). Use for a
  new capability area, a change to original-PRD assumptions, work
  spanning multiple issues/ADRs, or compatibility/migration concerns.
  Do NOT use for one-off bugs, small docs fixes, obvious refactors, or
  a single self-contained issue — those stay on the steady-state loop.

  Numbering. NNN is the next free sequential number in
  design/prd-addenda/ (001, 002, …). The original design/prd.md is
  never edited by this flow.

  Required sections. "What does not change", "Affected assumptions", and
  "ADR impact" must be filled — they are what keep the feature additive
  and well-specified. ADRs are never edited in place: a revision means a
  new ADR that supersedes the old one.
-->

# PRD Addendum NNN: {{Feature name}}

## Context

- **Original PRD:** {{path, e.g. design/prd.md}}
- **Current milestone/state:** {{from design/state.md / build-out-plan}}
- **Trigger for this update:** {{what prompted the feature now}}

## Problem

{{What hurts today that this feature addresses, and for whom.}}

## Goals

{{What success looks like — a few concrete bullets.}}

## Non-goals

{{Explicitly out of scope for this feature.}}

## What changes

{{New capabilities, APIs, surfaces, or behaviours this feature adds.}}

## What does not change

{{REQUIRED. Name the existing scope the feature deliberately leaves
alone — APIs, behaviours, decisions that stay exactly as they are.
Do not leave empty.}}

## Affected assumptions

{{REQUIRED. Original-PRD assumptions this feature changes, or
"none". Records divergence from the founding definition.}}

## ADR impact

{{REQUIRED. Each affected ADR with its action:
- Create: <new decision needed>
- Revise (via supersession): <ADR-NNN → new ADR>
- No change but relevant: <ADR-NNN, extended not contradicted>}}

## User stories

{{"As a <user>, I <do X> so that <Y>." A handful of concrete stories.}}

## Requirements

{{The functional and non-functional requirements the feature must meet.}}

## Migration and compatibility notes

{{Migration steps, backward-compatibility guarantees, and the expected
version bump (major/minor/patch). "Purely additive; no migration" is a
valid answer.}}

## Issue decomposition

{{Phased issues with dependencies and per-issue non-goals, ready for
/issue-planner:
1. <issue> (deps: …; non-goal: …)
2. <issue> (deps: …; non-goal: …)}}

## Success metrics

{{How you will know the feature works.}}

## Open questions

{{What is not yet decided. It is fine for this to be non-empty.}}
