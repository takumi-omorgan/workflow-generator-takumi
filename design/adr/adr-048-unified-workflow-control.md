# ADR-048: Unified workflow control (operating modes, canonical approval gate, verb layer, next-step routing)

**Status:** accepted
**Date:** 2026-06-05

## Context

The kit grew one flow-control concept at a time. ADR-006 set the
plan-first execution model. ADR-035 added `design/state.md` for
session continuity. ADR-039 added harness-level plan mode for
significant tasks. ADR-041 generalised that into a kit-wide auto-mode
permission contract with three categories. ADR-038 added `--no-prompt`
for trivial issues. Each decision was locally sound, but together they
left the operator facing several overlapping levers with no single
mental model:

- **Approval is described in three places.** The executor's eight-step
  chat plan-gate (`claude-issue-executor/SKILL.md`), the harness plan
  mode (ADR-039, `plan-mode.md`), and the cat-1/2/3 permission contract
  (`workflow-guide.md` §7) all describe "when does the assistant stop
  and ask?" — but no one location states the canonical sequence, and
  the accepted-approval signal is prose ("yes", "go ahead", "LGTM")
  rather than a documented token.
- **"Auto-mode" is an unnamed binary.** ADR-041 repeatedly says
  "under auto-mode" but the kit never named the modes a session can be
  in, nor stated how an operator declares one or where it is recorded.
- **Nineteen skills, no front door.** `docs/skills.md` is an accurate
  but granular inventory. A human asking "what do I run now?" has to
  read it; an agent has `kit.json`. There is no small, human-facing
  verb layer between the two.
- **State is a pointer, not an instruction.** `design/state.md` names
  the in-flight issue and a prose `continue-here` paragraph, but it
  exposes no *structured* next action a `/resume`-style router could
  execute without re-parsing prose.

The roadmap's Milestone M3
(`design/workflow-generator-roadmap-and-issues-20260605.md`) calls for
collapsing these into "one coherent stateful flow" across five issues:
a canonical approval gate (Issue 11), a `/start` or `/next` meta-skill
(Issue 12), a human-facing verb layer (Issue 13), a structured
`next-action` zone in `state.md` (Issue 14), and three named operating
modes (Issue 15). These five cannot be decided independently without
contradiction — a mode determines how the gate behaves; the router
reads the next-action zone; the verb layer is the human surface over
the same skills the router invokes. This ADR records them as one
decision. The follow-up-PRD half of M3 is a separable product-workflow
decision and lives in [ADR-049](adr-049-follow-up-prd-workflow.md).

## Options considered

### Option A: One unified control model, documented in one canonical doc, two thin new skills

Name three operating modes, define one canonical approval-gate
sequence with a deterministic approval token, add a human-facing verb
layer as a documented mapping, add a structured `next-action` zone to
`state.md`, and add one `/start` router skill. House the model in a new
`docs/workflow-control.md` that existing skills and `workflow-guide.md`
§7 cross-reference rather than restate.

- Pros: one mental model and one canonical home; the gate, modes,
  verbs, and next-step routing reinforce each other instead of
  competing; existing permission-category machinery (ADR-041) is
  reused, not replaced; minimal new surface area — two skills and one
  doc, not nineteen new verb-skills.
- Cons: largest single documentation artefact in the kit; one more doc
  for authors to keep in sync with §7 and the skill specs.

### Option B: Implement each of the five issues as an independent change

- Pros: smaller individual diffs; each lands when ready.
- Cons: reproduces the exact problem the milestone exists to solve —
  five more locally-sound levers with no unifying model. The verb layer
  would not know about modes; the router would not know about the gate.
  Rejected as self-defeating.

### Option C: Replace the cat-1/2/3 contract with the three modes

- Pros: fewer concepts — one axis instead of two.
- Cons: conflates two orthogonal things. Permission *category* is a
  property of a **skill operation** (is `gh pr create` reversible?);
  operating *mode* is a property of a **session** (how much has the
  operator pre-authorised?). Collapsing them would make every skill
  re-classify per mode. The right relationship is a small matrix: mode
  × category → behaviour. Rejected.

### Option D: Create a slash command for every human verb (`/decide`, `/backlog`, `/work`, `/ship`, …)

- Pros: each verb is directly invokable.
- Cons: nine new skill files that mostly forward to one existing skill
  each, doubling the inventory the validator and docs must track and
  violating the kit's "no speculative abstractions" rule. The value of
  Issue 13 is *information architecture* — a small vocabulary humans
  reach for first — which a documented mapping delivers without new
  machinery. Only `/start` earns a real skill because it does work no
  existing skill does (inspect state and route). Rejected in favour of
  a mapping plus the single `/start` router.

## Decision

Adopt **Option A**. Define one unified workflow-control model with a
single canonical home, `docs/workflow-control.md`, reusing ADR-041's
permission categories. The model has four parts.

### 1. Three operating modes (Issue 15)

A session runs in exactly one **operating mode**, declared by the
operator and stated by `/start` (and recordable in `CLAUDE.md` as a
project default):

| Mode | cat-1 (substitutable) | cat-2 (ack-bypass) | cat-3 (non-substitutable) |
|---|---|---|---|
| **interactive** (default) | assistant proposes, acts step by step | plan gate always runs | explicit approval |
| **assisted** | proceeds without asking | proceeds with a written acknowledgement | explicit approval |
| **autonomous** | proceeds without asking | proceeds with a written acknowledgement | **explicit approval — always** |

The modes are a **named layer over the cat-1/2/3 permission contract**
(ADR-041), not a replacement for it. The cell rule is: mode relaxes
cat-1 and cat-2 friction; **no mode ever relaxes cat-3** — public or
hard-to-reverse operations require explicit approval regardless of
mode. `assisted` and `autonomous` are the two shapes ADR-041 referred
to collectively as "auto-mode"; the difference between them is scope of
pre-authorisation, not cat-3 behaviour (which is identical). This makes
ADR-041's "under auto-mode" language concrete.

### 2. One canonical approval gate (Issue 11)

The approval gate is one sequence, documented once in
`docs/workflow-control.md` and cross-referenced (not restated) by every
skill:

1. **Classify** the work against the permission categories and the
   significance/trivial checklists (the checklists stay where they are,
   in `claude-issue-executor/plan-mode.md`).
2. **Determine whether approval is required** from the mode × category
   matrix above.
3. **Produce a plan** when approval is required (the executor's
   eight-step plan-gate is the reference instance).
4. **Wait for a deterministic approval token.** The accepted tokens are
   a closed set — `approve`, `approved`, `yes`, `go`, `proceed`,
   `lgtm` — matched case-insensitively as the operator's reply. A
   question or any other text is **not** approval: the assistant
   answers it and re-presents the plan.
5. **Proceed**, or — for a cat-2 bypass under `assisted`/`autonomous` —
   write the one-line acknowledgement ADR-041 already requires before
   the first mutating edit.

Trivial cat-1 work bypasses steps 3–4 explicitly: the bypass is a
property of the classification, testable against the trivial checklist.

### 3. Human-facing verb layer (Issue 13)

A small vocabulary sits in front of the nineteen-skill inventory.
Verbs map to underlying skills; the mapping lives in
`docs/workflow-control.md` and is surfaced at the top of
`docs/skills.md` before the full list:

| Verb | Underlying skill(s) |
|---|---|
| `/start`, `/next` | `start` (router) |
| `/decide` | `clarify` → `adr-writer` → `check-plan` |
| `/backlog` | `issue-planner` |
| `/work` | `prepare-issue` → `claude-issue-executor` |
| `/ship` | `pr-review-packager` |
| `/finish-milestone` | `audit-milestone` → `milestone-summary` → `complete-milestone` |
| `/feature` | `feature-prd` (see ADR-049) |
| `/release`, `/resume`, `/pause` | the same-named skills (1:1) |

Only `/start` is a new slash command. The other aggregate verbs are
**documentation aliases** for existing skills, not new skill files.
Agents continue to read exact skill names from `kit.json`; the full
inventory is never hidden from them.

### 4. `/start` router and the `next-action` state zone (Issues 12, 14)

- **`/start` (and its alias `/next`)** is a new cat-1 skill that
  inspects project state and recommends — or, for cat-1 targets,
  invokes — the next appropriate skill. On an empty project it routes
  toward PRD creation; with a prepared prompt it recommends the
  executor; with an open branch it recommends `/ship`. When the next
  step is genuinely ambiguous it asks **one** clarifying question
  rather than dumping the skill list.
- **`design/state.md` gains a marker-fenced `next-action` zone**
  (extending ADR-035, not superseding it) holding a structured next
  step: `skill`, `args`, and `preconditions`. The flow skills that
  already write `state.md` (`prepare-issue`, `claude-issue-executor`,
  `pr-review-packager`) and `/pause` populate it; `/resume` and
  `/start` read it and propose the action directly, reporting any
  unmet precondition as a blocker.

`docs/workflow-control.md` is the **single source of truth** for all
four parts. Skill specs and `workflow-guide.md` §7 cross-reference it
without restating, exactly as §7 is the single source of truth for the
permission categories it owns.

## Consequences

- Easier: one mental model for "how does the assistant decide to stop
  and ask?"; the approval signal is a documented token, not a guessed
  phrase; operators name a mode once instead of re-deciding per action;
  humans reach for a small verb vocabulary while agents keep exact
  names; `/resume` and `/start` can act on `state.md` without parsing
  prose.
- Harder: one more canonical doc to keep in sync with §7 and the skill
  specs; the mode × category matrix is new shared surface that PR
  review must protect from drift (machine enforcement is deferred to
  the M4 plan-checker, issue #72, alongside the existing §6/§7 drift
  checks).
- Maintain: the operating-mode matrix, the approval-token set, and the
  verb→skill table evolve as the kit grows; new skills are classified
  into a permission category (ADR-041) and, where they belong to a
  verb, added to the mapping at merge time; the `next-action` zone is a
  new state zone every state-writing skill must populate.
- Deferred: per-verb slash commands beyond `/start` (Option D) are not
  built — revisit only if the documentation aliases prove insufficient
  in practice. Recording the active mode as machine-readable session
  state (beyond `/start` stating it and `CLAUDE.md` holding a default)
  is left to a future iteration. This ADR extends — does not supersede
  — ADR-006, ADR-035, ADR-039, and ADR-041.
