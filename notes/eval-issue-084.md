# Eval — issue #84 Phase 2: SKILL.md body slimming via sidecar lift

**Branch:** `issue-084-phase2-body-slimming`
**Status:** verified (Phase 2 only — Phase 3 deferred)
**Date:** 2026-05-08

> **Note on supersession:** this file overwrites Phase 1's eval summary
> (committed `6aefd6d` on `main`, shipped in PR #86). Phase 1's content
> is preserved in git history — `git show 6aefd6d:notes/eval-issue-084.md`
> retrieves it. `notes/eval-issue-NNN.md` is a single-slot file per
> ADR-040 (pr-review-packager reads that exact path); each phase's eval
> overwrites the previous, with the prior phase's content always
> recoverable from git.

## Scope

Phase 2 of issue #84. Per the issue body's "Phases are independent.
Each phase ships as its own PR" rule:

| Phase | Status | Next session |
|---|---|---|
| 1 — Description rewrites | shipped (PR #86) | — |
| **2 — Body slimming for over-budget skills** | shipped here | this PR |
| 3 — Sidecar consistency (`examples.md` → `example.md`, `complete-milestone` / `milestone-summary` policy) | **deferred** | separate session, separate PR |

## What changed

### `skills/claude-issue-executor/`

| File | Change | Lines |
|---|---|---|
| `SKILL.md` | trimmed | 589 → 379 (−210) |
| `plan-mode.md` | NEW | 183 |
| `reference.md` | NEW | 71 |
| `example.md` | unchanged | — |

Two sidecars (rationale: governance vs operational housekeeping; both
independently one-level-deep from SKILL.md). `plan-mode.md` holds the
significance/trivial checklists, hybrid path, auto-mode behaviour,
alignment-review obligation, and entire `--no-prompt` mode body.
`reference.md` holds edge cases, design-questions populate rules, and
the seven-item alignment checklist. SKILL.md retains the chat
plan-gate (load-bearing 8-step rule), the 13-step session protocol,
the evaluation summary structure, and the `### design-questions`
schema spec.

**Cross-reference preservation verified:**
- The Trivial-checklist "single source of truth shared with ADR-038"
  claim survives intact in `plan-mode.md` (the `--no-prompt` body
  lives there too, so the cross-reference is internal to the sidecar).
- The Alignment-review obligation cross-reference to
  `docs/workflow-guide.md` §7 survives in `plan-mode.md` with the
  same `../../` relative path (sidecar and SKILL.md are at the same
  depth).
- The `### design-questions` schema spec at the end of the Evaluation
  summary section stays in SKILL.md (not lifted) — Risk #4 from the
  plan.

### `skills/pr-review-packager/`

| File | Change | Lines |
|---|---|---|
| `SKILL.md` | trimmed | 477 → 332 (−145) |
| `reference.md` | NEW | 157 |
| `example.md` | unchanged | — |

One sidecar. `reference.md` holds the issue-link / ADR-link extraction
rules, change-summary derivation algorithm, edge cases, pre-`gh`
self-check (preserving the ADR-023 sync-adr-index gate and ADR-040
Notes-for-#M emission gate), and relationship-to-other-skills map.
SKILL.md retains the cat-3 auto-mode permission contract, the 16-step
execution protocol, and the load-bearing review-before-create
approval gate. The pointer block surfaces both gates in its bullet
list so they remain visible at the routing surface.

### `skills/release/`

| File | Change | Lines |
|---|---|---|
| `SKILL.md` | trimmed | 479 → 357 (−122) |
| `reference.md` | NEW | 146 |
| `example.md` | unchanged | — |

One sidecar. `reference.md` holds the suggested-version heuristic,
project-shape detection signals + threshold + outcome bodies (with
the "single source of truth" claim and the workflow-guide §2.i
back-reference intact), edge-cases table, invariants, and both
self-check checklists. SKILL.md retains all invocation flags, the
default release boundary inference, prerequisites check, the
project-shape detection intro paragraph (referenced from `Release
flow` step 2 by name — Risk #3), `### Overrides` (CLI surface), the
release flow, the execution sequence (load-bearing orchestration),
and dry-run mode.

### `skills/prepare-issue/`

| File | Change | Lines |
|---|---|---|
| `SKILL.md` | trimmed | 408 → 253 (−155) |
| `reference.md` | NEW | 168 |
| `example.md` | unchanged | — |

One sidecar. `reference.md` holds the short-title derivation
algorithm, the full template-filling slot map (with the multi-ADR
repetition rule), the carry-forward subsection format and placement
rule (preserving the workflow-guide §6 schema-source-of-truth
pointer), edge cases, and the 8-item self-check. SKILL.md retains
inputs / output (with both optional flags), data sources priority
order, the 13-step execution protocol (including the `/check-plan`
gate at step 10), and the load-bearing review-before-write approval
gate.

### `notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv`

All 19 rows updated. The `change_from_v1` column now carries phased
history with semicolon-separated phase entries. The four touched rows
get a `phase2: lifted X + Y to <sidecar>.md (BBBL→AAAL, BBBkT→AAAkT
tokens)` annotation; the other 15 get `phase2: no change`. Rubric
columns 2–5 unchanged — all rows still score `has_what=yes,
has_when=yes, has_triggers=yes, third_person=yes`. Note column
extended with Phase 2 context where material (two-sidecar rationale,
preserved cross-references).

## Cohort budget after Phase 2

```
skill                     lines tokens >500  >5k
--------------------------------------------------
adr-writer                  202   2279    0    0
audit-milestone             186   2072    0    0
changelog                   435   4308    0    0
check-plan                  239   2752    0    0
clarify                     203   2255    0    0
claude-issue-executor       379   4359    0    0   <- was 589 / 6685
complete-milestone          246   2767    0    0
idea-to-prd                  97    966    0    0
issue-planner               359   3984    0    0
milestone-summary           221   2487    0    0
pause                       172   2064    0    0
planning                    198   2362    0    0
pr-review-packager          332   4036    0    0   <- was 477 / 5602
prd-normalizer              136   1386    0    0
prd-to-mvp                  145   1666    0    0
prepare-issue               253   3156    0    0   <- was 408 / 5197
release                     357   3734    0    0   <- was 479 / 5438
resume                      144   1562    0    0
workflow-docs               333   4020    0    0
```

All 19 cohort skills under both `over_500_lines == 0` and
`over_5k_tokens_est == 0`. The largest remaining skill is `changelog`
at 435L / 4,308 tokens (intentionally not touched — was 87% of token
target at audit time, leave-alone-unless-it-grows per Finding #2).

## Note on per-skill targets vs acceptance criteria

The issue body's Finding #2 set per-skill *preferred* targets (e.g.
`claude-issue-executor` ≤300L / ≤3,500T). The acceptance criterion
is the strict cohort-wide pass: all 19 under 500L AND under 5k tokens.

`claude-issue-executor` lands at 379L / 4,359T — under the strict AC
but above its preferred ≤300L target. Reaching 300L would require
lifting load-bearing orchestration (the 60-line Session protocol step
list at the centre of the skill). Judgment call: accept 379L as a
better trade-off than fragmenting the orchestration. Plan flagged
this explicitly; no AC violation.

## Commits

```
97426c4  refactor(skills/claude-issue-executor): lift plan-mode + reference into sidecars (#84 Phase 2)
6ff38fc  refactor(skills/pr-review-packager):    lift extraction rules and edge cases to reference.md (#84 Phase 2)
a006f2a  refactor(skills/release):                lift detection signals and edge cases to reference.md (#84 Phase 2)
6b207be  refactor(skills/prepare-issue):          lift template-filling rules and edge cases to reference.md (#84 Phase 2)
95ab96b  docs(notes/audit):                       re-score four touched skills for Phase 2 (#84 Phase 2)
[this commit]  chore(eval):                       record issue #84 Phase 2 verified state + eval summary (#84 Phase 2)
```

No ADR drives this work — same as Phase 1. All commit messages cite
`(#84 Phase 2)` only.

## Verification performed

| Acceptance criterion | Verification | Result |
|---|---|---|
| 1. `audit.py` reports `over_500_lines == 0` AND `over_5k_tokens_est == 0` across all 19 | `python3 notes/skills-audit-2026-05-07/audit.py` then per-row scan | empty list of over-budget skills ✓ |
| 2. No sidecar links to another sidecar | grep over the 5 new sidecar files for cross-sidecar references | no hits ✓ |
| 3. No behaviour change | structural preservation (only reference-style sections lifted; orchestration / approval gates / execution protocols stay inline); cross-references verified intact | ✓ |
| 4. v2-rubric still passes for all 19 | `awk -F, 'NR>1 && ($2!="yes" \|\| $3!="yes" \|\| $4!="yes" \|\| $5!="yes")' skills-audit-judgment-v2.csv` | empty ✓ |
| Secondary (prompt L50): check-plan ADR parser sane | `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` | `result: pass`, exit 0 ✓ |

## Follow-ups

### `### design-questions` block — OMITTED

Phase 2 is mechanical voice/structure refactor with no cross-issue
design coupling. Per ADR-040's when-NOT-to-populate rule (§6 of the
workflow guide), the block is omitted — not emitted as
`design-questions: []`.

### `notes/refactoring-ideas.md` entry #9 status update

At PR merge time, entry #9 needs another partial-shipped flip. Suggested
format:

```
**Status:** filed-#84 (Phase 1 shipped in #86, Phase 2 shipped in #<PR>)
**Captured:** 2026-05-06
**Filed:** #84 (2026-05-07)
**Shipped (Phase 1):** #86 (2026-05-07)
**Shipped (Phase 2):** #<PR> (2026-05-08)
```

Don't fully flip to `shipped-#PR` until Phase 3 ships. This is
post-merge bookkeeping, not part of the executor session — handle in
a direct-to-main commit alongside the PR merge, mirroring the
post-#86 commit `242ccba`.

### Phase 3 sequencing

Phase 3 (sidecar consistency) is the smallest of the three:
- Rename `skills/prd-normalizer/examples.md` → `example.md` (cohort uses singular; one drift)
- Decide cohort policy on the two skills currently with no sidecar (`complete-milestone`, `milestone-summary`): either add an `example.md` to each (matches 17/19 cohort default), or document in `docs/skills.md` why they're orchestration-only

Phase 3 acceptance is a small docs/file-rename PR. No coupling to
Phase 2's lift work.

## Commands to reproduce the verification

```bash
# 1. Mechanical audit — should report all 19 under budget.
python3 notes/skills-audit-2026-05-07/audit.py
python3 -c "
import csv
with open('notes/skills-audit-2026-05-07/skills-audit.csv') as f:
    rows = list(csv.DictReader(f))
over = [r['skill'] for r in rows if r['over_500_lines']=='1' or r['over_5k_tokens_est']=='1']
print('over budget:', over or 'NONE')
"

# 2. Sidecar depth check — no cross-sidecar links.
for f in skills/claude-issue-executor/{plan-mode,reference}.md skills/{pr-review-packager,release,prepare-issue}/reference.md; do
  grep -nE '\]\([^)]*(reference|plan-mode|criteria|example)\.md' "$f" | grep -v '\](SKILL\.md)' || true
done

# 3. v2-rubric still green — empty output.
awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' \
  notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv

# 4. check-plan ADR parser sanity.
bin/check-plan --criteria-set adr \
  --input design/adr/adr-046-ai-pr-review-module.md --format json

# 5. Spot-check the lifted SKILL.md files load cleanly (no broken refs).
for f in skills/{claude-issue-executor,pr-review-packager,release,prepare-issue}/SKILL.md; do
  echo "=== $f ==="
  head -10 "$f"
done

# 6. Full diff vs main.
git log main..HEAD --stat
```

## Next step

```
/pr-review-packager
```

The PR body should:

- Cite `notes/refactoring-ideas.md` entry #9 (origin) and
  `notes/skills-audit-2026-05-07/findings-v2.md` Finding #2 (Phase 2 work plan).
- State that this PR ships **Phase 2 only**; Phase 3 is a separate session.
- Use `Refs #84` not `Closes #84` (Phase 3 keeps the issue open) — same
  convention as PR #86.
- Note the cohort-wide budget pass (all 19 under 500L AND 5k tokens).
- Mention the `claude-issue-executor` two-sidecar split rationale
  (governance vs operational housekeeping).
