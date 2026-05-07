# Eval — issue #84 Phase 3: cohort sidecar consistency (final phase)

**Branch:** `issue-084-phase3-sidecar-consistency`
**Status:** verified (Phase 3 — closes issue #84)
**Date:** 2026-05-08

> **Note on supersession:** this file overwrites Phase 2's eval summary
> (committed `bf3a5ae` on `main`, shipped in PR #87). Phase 2's content
> is preserved in git history — `git show bf3a5ae:notes/eval-issue-084.md`
> retrieves it. Phase 1's content is at `git show 6aefd6d:notes/eval-issue-084.md`.
> `notes/eval-issue-NNN.md` is a single-slot file per ADR-040
> (pr-review-packager reads that exact path); each phase's eval
> overwrites the previous, with prior phases always recoverable from git.

## Scope

Phase 3 of issue #84 — the final phase. Closes the cohort-consistency
drifts called out in `notes/skills-audit-2026-05-07/findings-v2.md`
Finding #3.

| Phase | Status | PR |
|---|---|---|
| 1 — Description rewrites | shipped | #86 |
| 2 — Body slimming | shipped | #87 |
| **3 — Sidecar consistency** | **shipped here** | this PR |

After this PR ships, issue #84 closes.

## Headline decision: Option B (document the exception)

The prompt offered two options for handling the two no-sidecar skills:
- **Option A** — author worked `example.md` files for `complete-milestone` and `milestone-summary` to match the 17/19 cohort default.
- **Option B** — document in `docs/skills.md` why these two are orchestration-only and don't need their own example.

**Picked Option B.** Both skills already end their `## Handoff` section
with `See [audit-milestone/example.md](../audit-milestone/example.md)`
— the cohort already routes their walkthrough through the shared
`audit-milestone` example. Adding local `example.md` files would have
created cross-reference ambiguity and required either duplicating the
audit-milestone walkthrough or inventing synthetic per-skill ones.
Both skills are flow-orchestration (`complete-milestone` chains 3
skills; `milestone-summary` reads + composes one file) — they have no
inherent algorithmic complexity that warrants a per-skill example.
Option B preserved the existing cross-references intact and added a
single short subsection in `docs/skills.md`.

## What changed

### File rename (Phase 3 requirement #1)

| Before | After |
|---|---|
| `skills/prd-normalizer/examples.md` (336L) | `skills/prd-normalizer/example.md` (336L) |

`git mv` preserved blame (rename detected at 100% similarity). After
this rename, 17/17 sidecar-bearing skills use the singular `example.md`
filename — cohort consistency on the naming drift restored.

### Live tracked references updated (4 files)

| File | Edit |
|---|---|
| `skills/prd-normalizer/SKILL.md` | end-of-skill link from `[examples.md](examples.md)` to `[example.md](example.md)` |
| `skills/prd-to-mvp/example.md` | sibling-sidecar cross-reference updated |
| `examples/idea-only-example.md` | worked-example artifact link updated |
| `examples/custom-prd-example.md` | worked-example artifact link updated |

### Tracked references intentionally NOT updated (per AC1's historical-files carve-out)

The acceptance criterion explicitly says *"excluding `.git/` and any
historical eval/audit files that name it as a then-current path"* —
these are audit-trail records of what the audit said and what the
prompts asked for, at the moment they were authored:

- `notes/skills-audit-2026-05-07/findings-v2.md` (lines 119, 211) — the audit recommendation as authored 2026-05-07
- `notes/skills-audit-2026-05-07/verification-openai_gpt-5.5.md` (lines 97, 203) — third-party verification snapshot
- `notes/eval-issue-084.md` (Phase 2's content, line 222 — superseded by this file)
- `prompts/issue-084-phase2-body-slimming.md` (line 43) — Phase 2 prompt's scope-exclusion reference
- `prompts/issue-084-phase3-sidecar-consistency.md` — this prompt; the `examples.md` mentions describe what the rename does
- `design/state.md` (line 53) — the prep-step continue-here paragraph; auto-repointed by `/pr-review-packager`

Changing these would rewrite the historical record. Leaving them as-is
is the right call.

### Documentation of the orchestration-only exception (Phase 3 requirement #2 / Option B)

**`docs/skills.md`** — new subsection at end of §5 (Closing milestones):

```markdown
### Skills without a worked-example sidecar

`/complete-milestone` and `/milestone-summary` are the only two
skills in the cohort that ship without their own `example.md`. Both
are thin routing-orchestration layers: `/complete-milestone` chains
`/audit-milestone`, `/milestone-summary`, and optionally `/release`;
`/milestone-summary` reads `git log`, `gh`, and accepted ADRs to
compose one file. The full chain walkthrough lives in
[`skills/audit-milestone/example.md`](../skills/audit-milestone/example.md),
which exercises all three milestone-cluster skills against a phased
example project. The omission is intentional, not drift.
```

**`skills/complete-milestone/SKILL.md`** — Handoff section: existing
`See audit-milestone/example.md` paragraph extended with parenthetical
pointer to `docs/skills.md` §5.

**`skills/milestone-summary/SKILL.md`** — same parenthetical extension
on the existing `audit-milestone/example.md` cross-reference.

## Phase 2 sidecars are not Phase 3 territory (pre-empt review confusion)

Phase 2 added rule-detail sidecars (`claude-issue-executor/{plan-mode,
reference}.md`, `pr-review-packager/reference.md`,
`release/reference.md`, `prepare-issue/reference.md`). These are NOT
worked-example sidecars; they're progressive-disclosure reference
material. Phase 3's "no example.md" policy decision applies only to
worked examples. The new docs/skills.md section is specifically
titled "Skills without a worked-example sidecar" to make the
distinction explicit.

## Commits

```
f08108b  chore(prompts): add issue-084 phase3 prompt + refresh state.md (#84 Phase 3)
2149012  refactor(skills/prd-normalizer): rename examples.md → example.md and update live references (#84 Phase 3)
38679a7  docs(skills): document orchestration-only skills + cross-link from milestone SKILL.md (#84 Phase 3)
[this commit]  chore(eval): record issue #84 Phase 3 verified state + eval summary (#84 Phase 3)
```

No ADR drives this work — same as Phases 1 and 2. All commit messages cite `(#84 Phase 3)` only.

## Verification performed

| AC | Verification | Result |
|---|---|---|
| 1. `skills/prd-normalizer/example.md` exists; `examples.md` does not | `ls skills/prd-normalizer/example*.md` | only `example.md` ✓ |
| 2. Live references to old plural updated | `grep -rn --exclude-dir=.git --exclude-dir=notes --exclude-dir=prompts 'prd-normalizer/examples.md' .` | only the `design/state.md` continue-here paragraph (will be auto-repointed by `/pr-review-packager` post-PR) ✓ |
| 3 (Option A) | — | (skipped; chose B) |
| 4 (Option B) | `grep` for the new docs section + cross-links | docs/skills.md has the section; both SKILL.md cross-links point at the correct anchor `#skills-without-a-worked-example-sidecar` ✓ |
| 5. Cohort budget pass survives | `python3 audit.py` then per-row scan | all 19 under 500L AND 5k tokens; complete-milestone 247L/2,804T, milestone-summary 223L/2,524T (parenthetical cross-links added ~3-5L each, well within budget headroom) ✓ |
| 6. check-plan ADR parser sane | `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` | `result: pass` ✓ |
| 7. v2-rubric still passes for all 19 | `awk -F, 'NR>1 && (\$2!="yes" \|\| \$3!="yes" \|\| \$4!="yes" \|\| \$5!="yes")' skills-audit-judgment-v2.csv` | empty ✓ |

## Follow-ups

### `### design-questions` block — OMITTED

Phase 3 is mechanical/policy refactor with no cross-issue design coupling. Per ADR-040's when-NOT-to-populate rule (§6 of the workflow guide), the block is omitted — not emitted as `design-questions: []`.

### Post-merge bookkeeping (entry #9 final flip)

At PR merge time, `notes/refactoring-ideas.md` entry #9 flips to
**fully shipped** for the first time across the three phases:

```
**Status:** shipped-#86, #87, #<PR>  (or shipped-#PR-final, depending on convention preference)
**Captured:** 2026-05-06
**Filed:** #84 (2026-05-07)
**Shipped (Phase 1):** #86 (2026-05-07)
**Shipped (Phase 2):** #87 (2026-05-08)
**Shipped (Phase 3):** #<PR> (2026-05-08)
```

Issue #84 closes when PR for Phase 3 merges. Mirrors post-#86 commit
`242ccba` and post-#87 commit `93caa7f` patterns. Suggested approach:
move entry #9 from `## Filed` to a new `## Shipped` section if the
file's structure has one, or leave under Filed with the full
shipped-history block. The user picks the final convention.

### CSV re-score for Phase 3 — OMITTED

Phase 3 didn't modify any SKILL.md frontmatter description (Phase 1
territory) or any SKILL.md body that would affect the rubric scores
(Phase 2 territory). The two SKILL.md edits in commit 3 were 4-line
parenthetical cross-link additions to existing sentences in the
Handoff section — irrelevant to the v2 rubric (which scores
descriptions, not Handoff content). Skipping the CSV re-score is
appropriate; the existing scores from Phase 1 + Phase 2 annotations
remain accurate.

## Commands to reproduce the verification

```bash
# 1. Confirm the rename succeeded.
ls skills/prd-normalizer/example*.md

# 2. Confirm live refs are clean (only state.md continue-here remains, which is fine).
grep -rn --exclude-dir=.git --exclude-dir=notes --exclude-dir=prompts \
  'prd-normalizer/examples.md' .

# 3. Confirm docs/skills.md has the section.
grep -n "Skills without a worked-example sidecar" docs/skills.md

# 4. Confirm SKILL.md cross-links resolve to the right anchor.
grep -n "docs/skills.md#skills-without-a-worked-example-sidecar" \
  skills/complete-milestone/SKILL.md skills/milestone-summary/SKILL.md

# 5. Confirm cohort budget pass survives.
python3 notes/skills-audit-2026-05-07/audit.py
python3 -c "
import csv
with open('notes/skills-audit-2026-05-07/skills-audit.csv') as f:
    rows = list(csv.DictReader(f))
over = [r['skill'] for r in rows if r['over_500_lines']=='1' or r['over_5k_tokens_est']=='1']
print('over budget:', over or 'NONE')
"

# 6. Confirm v2-rubric still green.
awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' \
  notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv

# 7. Confirm check-plan ADR parser sane.
bin/check-plan --criteria-set adr \
  --input design/adr/adr-046-ai-pr-review-module.md --format json
```

## Next step

```
/pr-review-packager
```

The PR body should:

- Cite `notes/refactoring-ideas.md` entry #9 (origin) and
  `notes/skills-audit-2026-05-07/findings-v2.md` Finding #3 (Phase 3 work plan).
- State that this PR ships **Phase 3 only** but **closes issue #84**
  (the final phase of three).
- Use `Closes #84` (NOT `Refs #84`) — Phase 3 is the last phase, so
  this PR genuinely closes the issue. Departure from Phase 1's and
  Phase 2's `Refs #84` pattern, intentional.
- Note the cohort-consistency closeout: 17/17 sidecar-bearing skills
  use the singular `example.md`, and the no-sidecar pair's omission
  is now documented.
- Mention the headline Option B decision and why (cross-reference
  ambiguity avoidance, orchestration-shape skills, Anthropic's
  "examples are not required" stance).
