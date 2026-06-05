# Workflow Control — modes, the approval gate, verbs, and the next step

This is the **single source of truth** for how the kit decides when to
stop and ask, what vocabulary humans reach for, and how a session finds
its next action. It unifies four flow-control concepts that used to be
described in several places, governed by
[ADR-048](../design/adr/adr-048-unified-workflow-control.md):

1. [Operating modes](#1-operating-modes) — how much you have
   pre-authorised for the session.
2. [The approval gate](#2-the-approval-gate) — the one sequence by which
   the assistant decides to stop, plan, and wait.
3. [The verb layer](#3-the-human-facing-verb-layer) — a small vocabulary
   in front of the nineteen-skill inventory.
4. [Finding the next step](#4-finding-the-next-step) — `/start`, `/next`,
   and the structured `next-action` zone in `design/state.md`.

It reuses, and does not replace, the permission categories in
[`workflow-guide.md` §7](workflow-guide.md#7-auto-mode-permission-contract-adr-041).
Permission **category** is a property of a skill *operation* (is it
reversible?); operating **mode** is a property of a *session* (how much
have you pre-authorised?). The two compose as a small matrix below.

**For agents:** the machine-readable mirror of the permission categories
and skill names is [`kit.json`](../kit.json); see
[`agent-contract.md`](agent-contract.md). This doc is the human-readable
control model; the verb layer never hides exact skill names from agents.

---

## 1. Operating modes

A session runs in exactly **one** operating mode. The mode says how much
the operator has pre-authorised, and therefore how much friction the
assistant removes from substitutable (cat-1) and acknowledged-bypass
(cat-2) work. **No mode ever relaxes cat-3** — public or hard-to-reverse
operations always require explicit approval.

| Mode | cat-1 (substitutable) | cat-2 (ack-bypass) | cat-3 (non-substitutable) |
|---|---|---|---|
| **interactive** (default) | proposes and acts step by step | plan gate always runs | explicit approval |
| **assisted** | proceeds without asking | proceeds **with a written acknowledgement** | explicit approval |
| **autonomous** | proceeds without asking | proceeds **with a written acknowledgement** | explicit approval — **always** |

- **interactive** is the default and needs no declaration. It is the
  right mode for unfamiliar work, design-heavy sessions, and anyone
  learning the kit.
- **assisted** and **autonomous** are the two shapes ADR-041 referred to
  collectively as "auto-mode". They differ only in how much cat-1 work
  you have pre-authorised across the session — **not** in cat-3
  behaviour, which is identical (explicit approval, every time).
- The **cat-2 acknowledgement** is mandatory under `assisted` and
  `autonomous`: before the first mutating edit the assistant writes one
  line in chat — *"Plan mode bypassed by operator (cat-2
  operator-acknowledged bypass per workflow-guide §7)."* Without it the
  bypass is silent and the contract is violated.

### Declaring the mode

- **Per session:** tell the assistant at the start ("run in assisted
  mode" / "autonomous for this task"). `/start` states the active mode
  in its brief so it is visible in one place.
- **Per project default:** record a line in `CLAUDE.md`, e.g.
  `Operating mode: interactive` — sessions inherit it unless you say
  otherwise.

The cat-2 reference instance — `claude-issue-executor`'s ask-once
question under `assisted`/`autonomous` — is unchanged; see
[`skills/claude-issue-executor/plan-mode.md`](../skills/claude-issue-executor/plan-mode.md).

---

## 2. The approval gate

There is **one** approval-gate sequence. Every skill that stops to ask
follows it; skill specs cross-reference this section rather than
redefining it. The reference instance is `claude-issue-executor`'s
eight-step chat plan-gate, but the sequence is kit-wide:

1. **Classify** the work — its permission category
   ([`workflow-guide.md` §7](workflow-guide.md#7-auto-mode-permission-contract-adr-041))
   and, for implementation sessions, the significance/trivial checklists
   in [`claude-issue-executor/plan-mode.md`](../skills/claude-issue-executor/plan-mode.md).
2. **Determine whether approval is required** from the mode × category
   matrix in §1. cat-3 always requires it; cat-2 requires a plan or an
   acknowledged bypass; trivial cat-1 bypasses the gate.
3. **Produce a plan** when approval is required: the branch, every file
   to be created or modified with a one-line reason, the commit
   sequence, whether tests are written, and the verification steps.
4. **Wait for a deterministic approval token** (see below). Do not call
   any mutating tool until it arrives.
5. **Proceed** — or, for a cat-2 bypass under `assisted`/`autonomous`,
   write the one-line acknowledgement from §1 before the first mutating
   edit.

### The approval token

The accepted approval signal is a **closed set** of tokens, matched
case-insensitively as the operator's reply:

```
approve   approved   yes   go   proceed   lgtm
```

Anything else — a question, a request for a change, a partial comment —
is **not** approval. The assistant answers it and re-presents the plan
(returning to step 3). A clarifying reply ("why are you doing X?") never
counts as a yes. This makes "did the operator approve?" a deterministic
check rather than a judgement call.

### The trivial bypass

Genuinely-trivial cat-1 work — a single typo, an ADR status flip, a
one-line doc tweak, a `feature-ideas.md` status change — skips steps 3–4
**explicitly**. The bypass is a property of the classification (it is
the Trivial checklist in
[`claude-issue-executor/plan-mode.md`](../skills/claude-issue-executor/plan-mode.md)),
so it is testable, not a matter of taste. `--no-prompt` (ADR-038) is the
executor's instance of this bypass.

---

## 3. The human-facing verb layer

The kit ships nineteen skills. You do not need to remember all of them.
A small **verb layer** sits in front of the inventory: reach for a verb,
and it maps to the underlying skill(s). The full
[skills reference](skills.md) and [`kit.json`](../kit.json) still expose
every exact skill name — the verb layer is a front door, not a
replacement.

| Verb | What you mean | Underlying skill(s) |
|---|---|---|
| `/start`, `/next` | "what do I run now?" | `start` (router — §4) |
| `/decide` | "capture a decision" | `clarify` → `adr-writer` → `check-plan` |
| `/backlog` | "turn the plan into issues" | `issue-planner` |
| `/work` | "build the next issue" | `prepare-issue` → `claude-issue-executor` |
| `/ship` | "open the PR" | `pr-review-packager` |
| `/review-pr` | "AI-review a PR" | `review-pr` (see [ADR-051](../design/adr/adr-051-operator-driven-ai-pr-review.md)) |
| `/finish-milestone` | "close out the milestone" | `audit-milestone` → `milestone-summary` → `complete-milestone` |
| `/feature` | "plan a major feature update" | `feature-prd` (see [ADR-049](../design/adr/adr-049-follow-up-prd-workflow.md)) |
| `/release` | "cut a release" | `release` |
| `/resume` | "where were we?" | `resume` |
| `/pause` | "save the state" | `pause` |

Only **`/start`** (and its `/next` alias), **`/feature-prd`**, and
**`/review-pr`** are new slash commands. The aggregate verbs — `/decide`,
`/backlog`, `/work`, `/ship`, `/finish-milestone` — are **documentation
aliases** for skills that already exist; say them in conversation and the
assistant runs the underlying skill(s). `/release`, `/resume`, and
`/pause` map one-to-one to the same-named skills.

When you need the precise interface of an underlying skill, follow its
`SKILL.md` from the [skills reference](skills.md). When an agent needs
exact names, it reads [`kit.json`](../kit.json) — the verb layer is for
humans and never narrows what agents can see.

---

## 4. Finding the next step

Two mechanisms answer "what now?" — a router skill and a structured
state zone that the router (and `/resume`) reads.

### `/start` and `/next`

`/start` (alias `/next`) is a cat-1 router skill. It inspects project
state — `design/state.md` (especially the `next-action` zone below), the
presence of `design/prd.md` / `design/mvp.md` / prepared prompts / open
branches — and recommends, or for cat-1 targets directly invokes, the
next appropriate skill:

- Empty project (only an idea) → routes toward `/idea-to-prd`.
- Normalized PRD but no MVP → `/prd-to-mvp`.
- A prepared issue prompt on disk → recommends `/work`
  (`claude-issue-executor`).
- An open branch ahead of `main` → recommends `/ship`
  (`pr-review-packager`).

When the next step is genuinely ambiguous, `/start` asks **one**
clarifying question rather than dumping the full skill list. It states
the active operating mode (§1) in its brief.

### The `next-action` zone in `design/state.md`

`design/state.md` (ADR-035) gains a sixth marker-fenced zone,
`next-action`, holding a machine-readable next step so a router can act
without re-parsing prose:

```markdown
<!-- state:next-action:start -->

## Next action

```yaml
skill: prepare-issue
args: "95"
preconditions:
  - "issue #95 exists and is open"
blocked-by: none
```

<!-- state:next-action:end -->
```

- **`skill`** — the underlying skill name to run next (an exact name
  from `kit.json`, not a verb), or `none` when nothing is queued.
- **`args`** — the argument string to pass, or `n/a`.
- **`preconditions`** — what must hold before the action is valid.
- **`blocked-by`** — `none`, or a one-line description of what is
  blocking execution.

The zone is written by the skills that already update `state.md`
(`prepare-issue`, `claude-issue-executor`, `pr-review-packager`) and by
`/pause`; it is read by `/resume` and `/start`, which propose the action
directly. If a precondition is unmet or `blocked-by` is not `none`, the
reader reports the blocker instead of proposing the action. The zone is
optional and additive — projects that have not adopted it, or skills that
cannot determine a next action, leave it `none` rather than guessing.

The structured `next-action` is the deterministic complement to the
prose `continue-here` zone: `continue-here` is the human paragraph,
`next-action` is the executable form.

---

## Pointers

- ADR: [`adr-048-unified-workflow-control.md`](../design/adr/adr-048-unified-workflow-control.md)
- Permission categories (owned elsewhere): [`workflow-guide.md` §7](workflow-guide.md#7-auto-mode-permission-contract-adr-041)
- State file: [`workflow-guide.md` §5](workflow-guide.md#5-across-sessions-designstatemd-resume-pause), [ADR-035](../design/adr/adr-035-state-md-session-continuity.md)
- Significance / trivial checklists: [`skills/claude-issue-executor/plan-mode.md`](../skills/claude-issue-executor/plan-mode.md)
- Follow-up PRD workflow: [ADR-049](../design/adr/adr-049-follow-up-prd-workflow.md)
- Skills reference (full inventory): [`skills.md`](skills.md)
