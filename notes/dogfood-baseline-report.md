# Dogfood baseline report — M0-5

**Date:** 2026-06-05
**Branch:** `m0-baseline-health-and-drift`
**Issue:** M0-5 (Create first dogfood baseline report)
**Mode:** Autonomous, unsupervised (user-authorised for this M0 run).
**Instruction honoured:** "Do not optimize the workflow while running this
baseline. Record pain honestly; improvements belong in later issues."

## What this baseline measures, and the honesty caveat

The roadmap wants the first dogfood run to execute *one small real issue
through the current kit flow*
(`/prepare-issue → /claude-issue-executor → /pr-review-packager`) and
record the friction. Per M0-5's fallback clause ("if full current-kit
dogfood cannot be completed safely without human approval/merge,
simulate/document the exact attempted current-kit flow and friction
honestly"), this report **documents the attempted current-kit flow and
why it could not be run literally**, plus the path actually taken. The
selected "small issue" was M0-1 (baseline self-check) — the roadmap's own
nominated first issue.

This is a deliberately honest record, not a success story. The headline
finding is that the current kit's happy-path flow **does not fit a
multi-issue maintenance/audit milestone like M0**, and that is itself the
most useful baseline signal.

## The canonical flow vs. what actually happened

**Canonical current-kit flow (what the docs prescribe):**

```
/issue-planner            # create GitHub issues from the backlog
  → /prepare-issue N      # read issue N, emit prompts/issue-N-*.md
    → /claude-issue-executor   # consume the prompt, implement on a branch
      → /pr-review-packager    # gh pr create from the branch
```

**What actually happened this session:**

```
read roadmap M0 section + CLAUDE.md + docs + bin/ + all 19 SKILL.md
  → branch from main (m0-baseline-health-and-drift)
    → run current-kit *non-mutating* tooling directly:
        bin/check-plan (adr + prompt), bin/check-state-cap --check,
        bin/sync-adr-index --check, notes/skills-audit-2026-05-07/audit.py
    → hand-assemble checks with no kit entry point (bash -n sweep,
        inline python link-checker, installer smoke test in a temp dir)
    → write the four audit notes + two low-risk fixes directly
      → gh pr create (manual packaging, not via /pr-review-packager)
```

The slash-command chain was **not** invoked. Three concrete blockers
forced the direct path — each is a friction finding, classified below.

## Friction log (classified)

Classification scheme per M0-5: **human confusion**, **agent ambiguity**,
**missing tool support**, **documentation drift**.

| # | Friction | Class | Detail |
|---|---|---|---|
| F1 | **No entry point for a maintenance milestone.** M0 is five related audit/doc tasks (M0-1..5), not one feature. `prepare-issue` is single-issue and feature-shaped (assumes a governing ADR + one implementation branch). There is no `/audit`, `/baseline`, or batch verb. | missing tool support | The agent had to invent its own decomposition (a TodoWrite list) and ordering. Maps directly to roadmap M3 Issue 12 (`/start`–`/next` meta-skill) and Issue 13 (human-facing verb layer). |
| F2 | **Issues exist only as roadmap prose, not GitHub issues.** The canonical flow assumes `gh issue view N`. To dogfood literally, the agent would first run `/issue-planner` — a **cat-3** mutating action (`gh issue create`) that needs explicit approval *and* that the roadmap explicitly says to defer ("Do not create the entire roadmap as issues until the first dogfood pass has taught you what needs to change"). | agent ambiguity | The canonical path is blocked at step 1 by a gated, roadmap-discouraged action. The baseline therefore *cannot* follow the prescribed chain without violating the roadmap's own sequencing rule. This is the central tension. |
| F3 | **Preparation is prose-interpretation, not a callable surface.** To know how each skill behaves, the agent read SKILL.md (+ reference.md, + docs) prose. There is no `bin/prepare-issue --format json` yet. | missing tool support | Exactly the gap M2 Issue 9 targets. The agent spent most of its "understand the kit" budget reading prose that a JSON contract would have collapsed. |
| F4 | **Fresh-install dirty state.** The installer's `git add Design` (capital) vs created `design/` (lowercase) leaves a fresh install with an untracked `design/adr/README.md`. A first-time human would see a "successful install" immediately followed by a dirty `git status`. | documentation drift / defect | Surfaced during the M0-3 smoke test. Already fixed on the open M1 PR; see `notes/installer-idempotency-audit.md`. |
| F5 | **No single self-check command.** Producing the baseline health note meant hand-running ~13 separate commands (per-script `bash -n`, each `bin/check-*`, `sync-adr-index --check`, `audit.py`, two inline link-checkers, three installer runs). There is no `make check` / self-test / CI. | missing tool support | Maps to M4 Issue 19 (self-test) and Issue 20 (consistency checks). The "baseline" had to be constructed, not invoked. |
| F6 | **Unresolved template syntax in generated `CLAUDE.md`.** 25 raw `{{TOKEN}}` placeholders (incl. a stray `{{UPPER_SNAKE}}` from a doc comment) survive a non-interactive install, indistinguishable from "must fill" vs "fill later". | documentation drift | Maps to M1 Issue 3. An agent reading the generated file can't tell acceptable-unknown from required-unfilled. |

**No human-confusion findings** were logged — but only because this was
an autonomous agent run with no human in the loop. F1/F2 (no maintenance
entry point; prose-only issues) would very likely present as *human*
confusion for a first-time user trying to apply the kit to its own
roadmap. Recorded as agent-side here; re-evaluate the human angle when a
person runs M1.

## Measurements (baseline numbers to beat)

These are this autonomous session's figures. They are coarse (an agent,
not a stopwatch-timed human) but serve as the before-picture.

| Metric | Baseline (this M0 run) | Notes |
|---|---|---|
| Workflow path | roadmap prose → direct execution → manual PR | Canonical chain not usable (F1, F2) |
| User-facing slash commands used | **0** | None of `/issue-planner`, `/prepare-issue`, `/claude-issue-executor`, `/pr-review-packager` could be cleanly applied |
| Current-kit `bin/` surfaces used | **4** | `check-plan`, `check-state-cap`, `sync-adr-index`, `audit.py` — all ran first-try, zero friction |
| Distinct shell commands to produce the baseline-health note | **~13** | Target: 1 (a self-test) after M4 |
| Raw `{{…}}` tokens in a default-install `CLAUDE.md` | **25** (incl. 1 stray) | Target after M1 Issue 3: ≤4, all real, rendered as `_TBD_` |
| Untracked files after a "successful" fresh install | **1** (`design/adr/README.md`) | Target: 0 (M1 fix) |
| Manual approval / gate moments encountered | **1 conceptual** (`/issue-planner` = cat-3, deferred) | The one place the canonical flow demanded a gated action up front |
| Prose files read to understand how to prepare work | **~22** (19 SKILL.md + 3 docs) | Target after M2 Issue 9: 0 (one JSON call) |

## At least three measurable improvements to re-check after M1 / M2

1. **Fresh-install cleanliness (after M1).** Re-run
   `install-workflow-kit --non-interactive` into a temp dir and assert
   `git status --porcelain` is empty. **Baseline: 1 untracked file →
   target: 0.**
2. **Placeholder legibility (after M1 Issue 3).** Count raw `{{…}}` tokens
   in a default-install `CLAUDE.md`. **Baseline: 25 (incl. stray
   `{{UPPER_SNAKE}}`) → target: ≤4, all genuinely-required, others as
   `_TBD_`.**
3. **Single self-check entry point (after M4 Issue 19/20).** Count the
   shell commands needed to regenerate `notes/baseline-health.md`.
   **Baseline: ~13 hand-run commands → target: 1 self-test invocation
   emitting structured pass/fail.**
4. **Machine-readable preparation (after M2 Issue 9).** Count prose files
   an agent must read to prepare one issue. **Baseline: ~22 → target: 0
   (a single `bin/prepare-issue --format json` call).**
5. **Next-step routing (after M3 Issue 12).** Count the "which skill runs
   next / how do I decompose this?" decisions the operator must make
   unaided. **Baseline: the entire M0 decomposition + ordering was
   agent-invented → target: `/start`/`/next` proposes it from state.**

## One concrete recommendation for the roadmap

F2 is a real sequencing knot: the canonical flow's first step
(`/issue-planner`) is both gated (cat-3) and roadmap-discouraged for the
backlog, so *the prescribed flow cannot be dogfooded on the kit's own
roadmap without breaking the roadmap's own rule*. Before M1's front-door
work, consider whether maintenance/audit milestones need an explicit,
non-`gh`-mutating intake path (a local "issue draft" mode, or letting
`prepare-issue` accept a roadmap section instead of only a GitHub issue
number). This is offered as evidence for later issues, not fixed here.
