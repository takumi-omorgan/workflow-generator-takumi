# Eval — issue #83: Prune parenthetical ADR attributions from SKILL.md bodies

**Branch:** `issue-083-prune-adr-attributions`
**Status:** verified
**Date:** 2026-05-07

## What changed

### CLAUDE.md (1 file)

Added one bullet to "Working rules" — the doctrinal statement that
backs the prune work:

> SKILL.md bodies should not include parenthetical ADR attributions
> (`(per ADR-NNN)`, `(ADR-NNN)`) for traceability alone. Cite an ADR
> only when the reader needs the link to do the task — in which case
> use a markdown link in body text, not an inline parenthetical.

### `skills/*/SKILL.md` (17 files)

71 high-confidence + 5 medium-confidence type-3 attribution candidates
pruned across 17 of 19 SKILL.md files (`milestone-summary` and
`resume` were already clean per the audit). Verb/clause reformatting
preserved a small number of body markdown links where they remain
load-bearing as type-1 canonical anchors. Type-2 schema-name phrases
(`ADR-038's checklist`, `ADR-038's content-boundary review`,
`category-2 rule`) verified preserved.

### `prompts/issue-083-prune-adr-attributions.md` (new)

Filled prompt rendered from issue #83's body via `/prepare-issue 83`.
Passed `bin/check-plan --criteria-set prompt` on all four
deterministic criteria (C1, C2, C3, C6) plus C5 scope-cap warning.

### `design/state.md`

`state:in-flight` zone advanced from `none` → `Issue #83 / Status:
prepared` (Phase A) → `Status: verified` (Phase C). `state:continue-here`
zone updated to point at the executor session on this branch.

## Commits

```
62c5446  chore(prompts):  add issue-083 prompt + refresh state.md (#83)
af7d960  docs(claude-md): add SKILL.md ADR-attribution style rule (#83)
ef3c0ce  refactor(skills): prune ADR attributions in claude-issue-executor (#83)
ba34837  refactor(skills): prune ADR attributions in prepare-issue + adr-writer (#83)
9f8f735  refactor(skills): prune ADR attributions in mid-density skills (#83)
7f0bea4  refactor(skills): prune ADR attributions in remaining 10 skills (#83)
```

## Verification performed

| Check | Result |
|---|---|
| `python3 notes/skills-audit-2026-05-07/adr-audit.py` final count | **3 high-conf + 1 medium-conf** (≤ 5 acceptance budget) |
| `bin/check-plan --criteria-set prompt --input prompts/issue-083-*.md` | pass (all four deterministic criteria) |
| `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md` | pass (smoke test — eval module intact after prune) |
| Type-2 schema-name spot-check (`grep "ADR-038's"` in skills/) | 3 preserved occurrences in `claude-issue-executor` ✓ |
| Markdown link integrity (canonical anchors at top of each SKILL.md) | preserved across all 17 files |

### Remaining audit hits (deliberately kept; under acceptance budget)

3 high-confidence + 1 medium-confidence audit hits remain — all are
non-attribution-style:

| Skill | Line | Pattern | Reason kept |
|---|---|---|---|
| `changelog` | L267 | `(ADR-013)` | Inside backticks demonstrating a literal commit-message example |
| `issue-planner` | L171 | `(ADR-007)` | Inside backticks demonstrating the kit's example issue-title shape |
| `prepare-issue` | L63 | `per ADR-034` | Inside an HTML-comment string showing the literal breadcrumb format the skill emits |
| `prepare-issue` (medium) | L11 | `see ADR-013` | Type-1 canonical anchor (markdown link) at top of file |

### Reformat decisions (deliberate drill-downs)

Three places where the audit-flagged attribution was reformatted
rather than deleted — preserves a body markdown link to the
canonical ADR for the section while dropping the attribution voice:

| Skill | Old | New |
|---|---|---|
| `claude-issue-executor` (Plan-mode rhythm section) | "The rules below implement [ADR-039]..." | "The rules below come from [ADR-039]..." |
| `issue-planner` (intro paragraph) | "This skill implements [ADR-011] (...) and [ADR-012] (...)" | "This skill comes from [ADR-011] (...) and [ADR-012] (...)" |
| `release` (intro paragraph) | "This skill implements [ADR-017]." | "This skill comes from [ADR-017]." |

## Follow-ups

The `notes/refactoring-ideas.md` entry #2 already shows
`Status: filed-#83` with a `Filed: #83 (2026-05-07)` line — no
notepad change is needed in this PR. After PR merge, the entry's
status will roll forward to `shipped-#<PR-number>` per the kit's
existing convention.

Pairs with — but does not block — entry #9 / issue #84 (broader
SKILL.md style audit). #83 was scoped specifically to the type-3
attribution noise bucket; the cohort-wide structural / length /
sidecar audit remains scoped to #84.

## Commands to reproduce the verification

```bash
# 1. Audit count: should report 3 high-conf + 1 medium-conf, all
#    flagged as deliberate keeps.
python3 notes/skills-audit-2026-05-07/adr-audit.py

# 2. Type-2 schema-name preservation: should return 3 hits in
#    claude-issue-executor.
grep -rEn "ADR-038's" skills/

# 3. Smoke check the check-plan eval module on an existing ADR.
bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json

# 4. Voice spot-check: open the highest-density skill before/after.
git diff main..HEAD -- skills/claude-issue-executor/SKILL.md
```

## Next step

`/pr-review-packager` to draft a PR from this branch. The PR body
should cite `notes/refactoring-ideas.md` entry #2 as the origin
and link `notes/skills-audit-2026-05-07/adr-attributions.md` as
the per-match work plan.
