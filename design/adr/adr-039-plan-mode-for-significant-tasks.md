# ADR-039: Require Claude Code plan mode for significant tasks in `claude-issue-executor`

**Status:** accepted
**Date:** 2026-04-30

## Context

`claude-issue-executor` (ADR-014) enforces "plan-first" via a
**chat-level** protocol: the assistant proposes a written plan and
waits for explicit user approval before any mutating tool call. That
is convention. Claude Code also ships a **harness-level** mechanism
— plan mode (toggled with `shift+tab shift+tab`) — that locks the
assistant out of all mutating tools until the user explicitly exits
plan mode with approval. The two are complementary, but the kit
currently relies only on the soft one.

During the v-next planning batch (ADR-031 → ADR-038, issues
#40–#47) the user noticed the gap: the chat plan-gate held cleanly
because every plan was being reviewed deliberately, but it depended
entirely on the assistant *following* the rule rather than the
harness *enforcing* it. The user asked for harness-level enforcement
to become standard for "significant" tasks going forward, with an
explicit ask-the-user fallback for cases where the criterion is
ambiguous.

This ADR also interacts with ADR-038 (`#29` — tighten the prompt
step). ADR-038's `--no-prompt` mode targets trivial issues
(single-line bug fixes, doc tweaks, dependency bumps); those are
exactly the cases that should *not* trigger plan mode either. The
two ADRs share a "trivial issue" definition; keeping them in sync
matters.

## Options considered

### Option A: Auto-enter plan mode for every significant task

- Pros: maximum enforcement; zero reliance on assistant discipline;
  no per-session "should I?" question.
- Cons: friction for borderline cases (a 2-file change that crosses
  the line into a 3rd file mid-session); user has no easy way to
  override for a specific task without editing the criteria; assumes
  the criteria are precise enough to act on without judgment.

### Option B: Ask the user at session start whether to enter plan mode

- Pros: maximum transparency; preserves user control; one extra
  interaction per session is small overhead; works regardless of how
  fuzzy the criteria are.
- Cons: still relies on assistant discipline to *ask* — if the
  assistant forgets, no enforcement; one extra round-trip per
  session, even when the answer is obviously "yes."

### Option C: Hybrid — auto-enter for clearly-significant, auto-skip for clearly-trivial, ask only on borderline

- Pros: best balance of transparency and friction; trivial work
  ships fast; clearly-significant work gets the full lock; ambiguous
  cases get a one-line yes/no question rather than a blanket
  default.
- Cons: requires a clear-enough checklist to classify cases reliably;
  hardest of the three to specify and document.

### Option D: Do nothing — keep relying on the chat plan-gate alone

- Pros: zero implementation cost; the chat-level rule has worked so
  far.
- Cons: leaves the gap that prompted this ADR; no harness-level
  enforcement; one assistant lapse defeats the rule.

## Decision

Adopt **Option C**. Update `skills/claude-issue-executor/SKILL.md` so
the executor classifies each session against a documented "significant"
checklist at session start and:

- **Auto-flag for plan mode entry** — and pause until the user toggles
  plan mode — when the session is **clearly significant**. The
  executor proposes the plan inside plan mode; the user approves and
  exits plan mode (optionally enabling auto-accept) for the
  implementation phase; the executor pauses again at the next
  significant boundary.
- **Auto-skip plan mode** when the session is **clearly trivial**.
  The chat plan-gate alone holds the line.
- **Ask once** when the classification is borderline ("Significant?
  yes / no / decide for me") and proceed accordingly.

**The "significant" checklist** (single source of truth, documented
in `skills/claude-issue-executor/SKILL.md` and cross-referenced from
the workflow guide):

- modifies 3+ files, OR
- edits any `skills/*/SKILL.md`, OR
- edits any `templates/*` file, OR
- edits `bin/*` (scripts, installer), OR
- modifies `.claude/settings*.json` or other harness config, OR
- otherwise carries blast radius beyond a single small fix.

**The "trivial" checklist** (must stay aligned with ADR-038's
`--no-prompt` criteria — drift between the two silently breaks the
rhythm):

- single typo,
- single-line doc tweak,
- status-line / config-default tweak,
- single-file rename within scratch space,
- `feature-ideas.md` status flip,
- ADR status flip (proposed → accepted),
- single-PR scope with no design decisions and no ADR linkage.

ADR-038's `--no-prompt` mode and this ADR's auto-skip path reference
the same trivial checklist. When either checklist evolves, both
must move together; the documented home is
`skills/claude-issue-executor/SKILL.md` and ADR-038's content
boundary review is the enforcement point.

## Consequences

- Easier: harness-level enforcement removes a class of "I forgot to
  wait" failures; trivial work ships without ceremony; significant
  work gets the full lock automatically.
- Harder: borderline-case ask adds one round-trip; the criteria
  checklist must stay current as the kit grows; new contributors
  need to learn when plan mode kicks in.
- Maintain: the two checklists (significant, trivial) live in
  `skills/claude-issue-executor/SKILL.md` as the single source of
  truth, cross-referenced from the workflow guide and ADR-038. CI
  or PR-review should flag edits to one without the other.
- Deferred: applying the same rhythm to other skills
  (`pr-review-packager`, `prepare-issue`, `release`) — covered in
  follow-up if the executor pattern proves out. Auto-accept
  behaviour during the implementation phase is a user toggle and not
  in scope for this ADR.
