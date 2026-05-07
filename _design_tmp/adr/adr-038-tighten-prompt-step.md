# ADR-038: Tighten the prompt step — auto-chain executor and `--no-prompt` mode

**Status:** accepted
**Date:** 2026-04-30

## Context

The per-issue prompt artefact (ADR-008 + ADR-013) is a load-bearing
piece of the audit trail and the natural anchor for ADR-034 (plan
checker) and ADR-035 (state.md continuity). Plan mode in Claude
Code is good but synthesises from whatever is in front of it —
without a prompt, that is "the issue body + whichever ADRs you
remembered to attach," and quality varies by author and session.
The cost of producing the prompt is already near-zero thanks to
`prepare-issue` (ADR-013).

The right move is to keep the artefact and reduce its ceremony, not
remove it. Two specific frictions remain. First, today
`prepare-issue` and `claude-issue-executor` are two separate
commands — one too many for an action that always happens together.
Second, trivial issues (typo fixes, dependency bumps, CI tweaks,
single-line doc fixes — the ADR-less path the issue template
already supports per `templates/issue-template.md:15`) carry
ADR-shaped ceremony they do not earn.

This ADR also carries an explicit alignment review obligation:
several v-next ADRs (ADR-031, ADR-032, ADR-033, ADR-035, ADR-037)
introduce new artefacts whose content overlaps with what the
prompt currently captures. If the kit grows duplicate context
across files, the prompt's content shape needs trimming. The
review must happen before this ADR is implemented.

## Options considered

### Option A: Auto-chain `prepare-issue` into `claude-issue-executor` AND add `--no-prompt` mode

- Pros: reduces ceremony for the common case; trivial issues stop
  carrying ADR-shaped overhead; prompt artefact remains the anchor
  for ADR-034 / ADR-035.
- Cons: two changes coupled into one ADR; `--no-prompt` is a
  slippery slope without tight criteria.

### Option B: Auto-chain only — keep the artefact mandatory

- Pros: smallest change; no new escape hatch.
- Cons: leaves the "this is overkill for a typo fix" friction
  unaddressed.

### Option C: `--no-prompt` only

- Pros: covers the trivial case.
- Cons: leaves the manual two-step (`prepare` then `execute`) for
  every non-trivial issue.

### Option D: Replace prompt artefact with plan-mode-only

- Pros: one fewer file; rely entirely on Claude Code's native plan
  mode.
- Cons: rejected — loses audit trail, session-rerun guarantee, and
  the anchor that ADR-034 (plan-checker) and ADR-035 (state.md)
  depend on.

## Decision

Adopt **Option A**. Two changes to `claude-issue-executor`
(ADR-014):

1. **Auto-chain `prepare-issue`.** Executor checks for
   `prompts/issue-NNN-*.md` at session start. If absent, calls
   `prepare-issue` automatically and proceeds. If present and
   stale (issue body or any linked ADR mtime is newer than the
   prompt mtime), regenerates with confirmation. The prep step is
   logged prominently so users see it happen.
2. **`--no-prompt` mode.** New flag on `claude-issue-executor`
   skips prompt generation and runs from the issue body alone.
   Documented criteria: single-PR scope, no design decisions, no
   ADR linkage. Auto-detected (with confirmation) when the issue
   has zero ADR references and carries one of the labels `chore`,
   `docs`, or `bugfix-trivial`. Explicit `--no-prompt` overrides
   detection. A one-line breadcrumb is left in the commit message
   ("issue executed without prompt per ADR-038") for traceability.

**Mandatory alignment review before implementation.** Before this
ADR moves from `proposed` to `accepted`, audit the prompt's content
shape against ADR-031 (`planning.md`), ADR-032 (phase context in
`build-out-plan.md`), ADR-033 (`decisions.md`), ADR-034 (plan
checker criteria), ADR-035 (`state.md`), and ADR-037 (milestone
summary). If any of those produces an artefact whose content the
prompt currently duplicates, trim the prompt's content boundary so
each artefact has one canonical home and the prompt links rather
than restates. Record the resulting boundary changes in this ADR
or a follow-up amendment ADR before implementing.

## Consequences

- Easier: fewer manual steps for the common case; trivial issues
  stop carrying ceremony; prompt artefact remains the anchor for
  ADR-034 and ADR-035.
- Harder: auto-chain hides a step users may want to see (mitigation:
  prominent logging); `--no-prompt` is a slippery slope without
  tight criteria (mitigation: documented checklist and label-based
  auto-detection).
- Maintain: small — both changes live in `claude-issue-executor`'s
  argument handling and prompt-staleness check; alignment review is
  a one-time content-boundary rewrite once the dependent ADRs are
  accepted.
- Deferred: removing the prompt entirely (Option D, rejected).
  Per-prompt content-shape changes belong to follow-up ADRs once
  ADR-031 / 032 / 033 / 035 / 037 are accepted and exercised.
