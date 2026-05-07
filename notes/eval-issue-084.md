# Eval — issue #84 Phase 1: rewrite SKILL.md descriptions to canonical Use-when shape

**Branch:** `issue-084-phase1-skills-descriptions`
**Status:** verified (Phase 1 only — Phase 2 and Phase 3 deferred)
**Date:** 2026-05-07

## Scope

This session ships **Phase 1 only** of issue #84. Per the issue body's "Phases are independent. Each phase ships as its own PR" rule:

| Phase | Status | Next session |
|---|---|---|
| **1 — Description rewrites** | shipped here | this PR |
| 2 — Body slimming for over-budget skills | **deferred** | separate session, separate PR |
| 3 — Sidecar consistency (`examples.md` → `example.md`, complete-milestone / milestone-summary policy) | **deferred** | separate session, separate PR |

## What changed

### `skills/*/SKILL.md` (19 files)

All 19 frontmatter `description:` fields rewritten to follow Anthropic's canonical `[what it does]. Use when [trigger].` template. Five adjacent-skill clusters got boundary clauses:

| Cluster | Skills | Boundary |
|---|---|---|
| Implementation handoff | `prepare-issue` ↔ `claude-issue-executor` | preparation vs execution |
| Session handoff | `pause` ↔ `resume` | end-of-session vs start-of-session |
| Pre-ADR pipeline | `planning` ↔ `clarify` ↔ `adr-writer` | broader context vs specific questions vs commit decision |
| Release pipeline | `changelog` ↔ `release` | notes-only vs tag-and-publish |
| Milestone lifecycle | `audit-milestone` ↔ `complete-milestone` ↔ `milestone-summary` | verify before close vs close vs retrospective after close |

### YAML quirk fix in `skills/pr-review-packager/SKILL.md`

The pre-existing description used `Closes #N`, which YAML parsers interpret as a comment marker after whitespace, silently truncating the description value at parse time to *"Draft a pull-request body from templates/pr-template.md, auto-fill Closes"*. Reworded to `Closes line` so the full description renders. Bug existed before this PR; fix bundled into the rewrite for the affected file.

### `notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv`

All 19 rows re-scored to `has_what=yes, has_when=yes, has_triggers=yes, third_person=yes` per methodology-v2.md §4.1. The `change_from_v1` and `note` columns updated to record what Phase 1 did per skill.

This file was previously untracked alongside the rest of the audit harness; this commit starts tracking it (per the issue body's acceptance criterion: *"commit the new scores"*). The rest of the harness directory (`audit.py`, `findings-v2.md`, `methodology-v2.md`, `verification-openai_gpt-5.5.md`, etc.) remains untracked — that tracking decision is separate from Phase 1.

## Commits

```
b5027dd  chore(prompts):  add issue-084 prompt + refresh state.md (#84)
15aefbb  refactor(skills): rewrite 19 descriptions to canonical Use-when shape + 5 cluster boundary clauses (#84)
ecb1528  chore(notes):    re-score skills-audit-judgment-v2.csv after Phase 1 rewrites (#84)
[this commit]  chore(eval):     record issue-084 phase-1 verified state + eval summary (#84)
```

## Verification performed

| Check | Result |
|---|---|
| `python3 notes/skills-audit-2026-05-07/audit.py` | 19 rows written; no errors |
| `desc_chars` (mechanical, audit.py) | min=137, max=344 — all 19 ≤ 1024 ✓ |
| `desc_over_1024` (mechanical) | 0 for all 19 ✓ |
| `desc_first_person` / `desc_second_person` (mechanical) | 0 for all 19 — third-person preserved ✓ |
| `desc_has_when_marker` (mechanical) | **1 for all 19** — every description contains "Use when" ✓ |
| `awk -F, 'NR>1 && ($2!="yes"\|\|$3!="yes"\|\|$4!="yes"\|\|$5!="yes")' skills-audit-judgment-v2.csv` | empty — all 19 rows pass all four rubric fields ✓ |
| `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` | `result: pass` — eval module intact after rewrite ✓ |
| Live skill list smoke check | the harness's loaded skill list shows all 19 with the new descriptions including the `pr-review-packager` Use-when clause that was previously truncated by the YAML bug ✓ |

The mechanical `desc_has_when_marker` check is independent confirmation of the rewrite — `audit.py` reads the YAML-parsed description and tests for "Use when" presence in body text. Combined with the human-judged CSV re-score (all four rubric fields → yes), Phase 1 meets every acceptance criterion in the issue body.

## Reformat decisions worth flagging in the PR body

Three skills had their type-1 anchor verb shifted to a less attribution-shaped wording during the rewrite (matches the precedent set in #83):

- `claude-issue-executor`, `issue-planner`, `release` — kept their canonical-anchor markdown links to ADR-014/011/012/017 in the introductory body paragraph; only the *frontmatter description* changed in this commit.

The body markdown links to ADRs are unchanged. The description rewrite is exclusively in the frontmatter; SKILL.md bodies are not touched (Phase 2 territory).

## Follow-ups

### `### design-questions` block — OMITTED

Phase 1 is mechanical voice/metadata refactor with no cross-issue design coupling. Per ADR-040's when-NOT-to-populate rule (§6 of the workflow guide), the block is omitted — not emitted as `design-questions: []`.

### `notes/refactoring-ideas.md` entry #9 status update

At PR merge time, entry #9 needs a status flip — but this is a *partial* shipped state since #84 has three phases. Suggested format:

```
**Status:** filed-#84 (Phase 1 shipped in #<PR>)
**Captured:** 2026-05-06
**Filed:** #84 (2026-05-07)
**Shipped (Phase 1):** #<PR> (2026-05-07)
```

Don't fully flip to `shipped-#PR` until all three phases ship. This is post-merge bookkeeping, not part of the executor session — handle in a direct-to-main commit alongside the PR merge.

### Phase 2 + Phase 3 sequencing

Per the issue body, Phase 2 is the higher-leverage next step: bring four over-budget skills (`claude-issue-executor` 586L/6.7k tokens, `pr-review-packager` 471L, `release` 474L, `prepare-issue` 405L) under Anthropic's 500L / 5k-token L2 budget by lifting content into one-level-deep sidecars. Phase 3 (sidecar consistency) is the smallest of the three and can ship in any order.

### Audit-harness tracking decision

The audit-harness directory (`notes/skills-audit-2026-05-07/`) is referenced multiple times in this PR body and the eval, but only the CSV is currently tracked. Tracking the rest (`audit.py`, `findings-v2.md`, `methodology-v2.md`, `verification-openai_gpt-5.5.md`, etc.) would make those references resolve in PR review and on GitHub. Worth deciding before Phase 2 — its acceptance criterion will also reference `audit.py`, so consistent tracking matters. Not in Phase 1's scope.

## Commands to reproduce the verification

```bash
# 1. Mechanical audit — should report 19 rows, all clean.
python3 notes/skills-audit-2026-05-07/audit.py

# 2. Inspect the auto-generated audit CSV's description-related columns.
python3 -c "
import csv
with open('notes/skills-audit-2026-05-07/skills-audit.csv') as f:
    rows = list(csv.DictReader(f))
for c in ['desc_chars', 'desc_over_1024', 'desc_first_person', 'desc_second_person', 'desc_has_when_marker']:
    vals = [int(r[c]) for r in rows]
    print(f'{c}: min={min(vals)} max={max(vals)}')
"

# 3. Human-judged rubric — empty output means all 19 rows pass.
awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' \
  notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv

# 4. Smoke test — check-plan eval module still loads.
bin/check-plan --criteria-set adr \
  --input design/adr/adr-046-ai-pr-review-module.md --format json

# 5. Voice spot-check — head a few skills before/after.
for f in skills/{adr-writer,prepare-issue,claude-issue-executor,release,pr-review-packager}/SKILL.md; do
  echo "=== $f ==="; head -5 "$f"
done
```

## Next step

```
/pr-review-packager
```

The PR body should:

- Cite `notes/refactoring-ideas.md` entry #9 (origin) and `notes/skills-audit-2026-05-07/findings-v2.md` (work plan).
- State that this PR ships **Phase 1 only**; Phase 2 and Phase 3 are separate sessions.
- Mention the YAML-comment-truncation bug fix in pr-review-packager's description as a side benefit.
- Note that `audit-harness tracking` (the rest of the directory) is a separate decision not made by this PR.
