# Skill metadata, permission & handoff drift audit — M0-2

**Date:** 2026-06-05
**Branch:** `m0-baseline-health-and-drift`
**Issue:** M0-2 (Audit skill metadata, permission, and handoff drift)
**Goal:** Before the M2 machine-readable contract layer (`kit.json`) is
built, confirm the prose source materials don't already disagree about
skill names, permission categories, handoff order, or outputs.

## Method

- Frontmatter (`name`, `permission-category`) extracted from each
  `skills/*/SKILL.md` with a small Python pass.
- Handoff (`## Handoff`) and output (`## Output` / `## Outputs`) sections
  parsed for presence and next-skill references.
- Documented permission labels and workflow order extracted from
  `docs/skills.md` (the per-skill reference, each heading carries a
  `(cat-N)` label) and `docs/workflow-guide.md`.
- Deterministic metrics cross-checked against the existing harness:
  `python3 notes/skills-audit-2026-05-07/audit.py` (19 rows, all within
  budget — no skill over the 500-line / 5k-token body caps, all
  `fm_name_matches_dir=1`).

## Audit table — all 19 skills

| Skill (dir) | fm `name` | Perm | Doc label (skills.md) | Handoff | Output heading | Next skill(s) in handoff |
|---|---|---|---|---|---|---|
| adr-writer | adr-writer | 1 | cat-1 | yes | `## Output` | (terminal → user accepts; feeds executor later) |
| audit-milestone | audit-milestone | 1 | cat-1 | yes | `## Output` | milestone-summary, complete-milestone, release |
| changelog | changelog | 1 | cat-1 | yes | `## Output` | release |
| check-plan | check-plan | 1 | cat-1 | yes | `## Output` | (leaf — advisory) |
| clarify | clarify | 1 | cat-1 (opt-in) | yes | `## Output` | adr-writer |
| claude-issue-executor | claude-issue-executor | 2 | cat-2 | yes | `## Outputs` | pr-review-packager |
| complete-milestone | complete-milestone | 3 | cat-3 | yes | inline (no heading) | release (chained), then external |
| idea-to-prd | idea-to-prd | 1 | cat-1 | yes | `## Output` | prd-normalizer |
| issue-planner | issue-planner | 3 | cat-3 | yes | `## Outputs` | prepare-issue, workflow-docs |
| milestone-summary | milestone-summary | 1 | cat-1 | yes | `## Output` | complete-milestone, release |
| pause | pause | 1 | cat-1 | yes | `## Output` | resume |
| planning | planning | 1 | cat-1 (opt-in) | yes | `## Output` | adr-writer, issue-planner |
| pr-review-packager | pr-review-packager | 3 | cat-3 | yes | `## Output` | (terminal — human review/merge) |
| prd-normalizer | prd-normalizer | 1 | cat-1 | yes | `## Output` | prd-to-mvp, adr-writer |
| prd-to-mvp | prd-to-mvp | 1 | cat-1 | yes | `## Outputs` | adr-writer |
| prepare-issue | prepare-issue | 1 | cat-1 | yes | `## Output` | claude-issue-executor |
| release | release | 3 | cat-3 | yes | inline (no heading) | (terminal — delivery chain end) |
| resume | resume | 1 | cat-1 | yes | `## Output` | prepare-issue (or open PR) |
| workflow-docs | workflow-docs | 1 | cat-1 | yes | `## Outputs` | (terminal — docs generation) |

### Implied outputs (per skill, from Output/Outputs body)

| Skill | Implied output artefact(s) |
|---|---|
| idea-to-prd | `design/prd.md` (standard PRD draft) |
| prd-normalizer | `design/prd-normalized.md` |
| prd-to-mvp | `design/mvp.md`, `design/build-out-plan.md` (+ "Decisions needing ADRs" list) |
| planning | `design/planning.md` |
| clarify | `design/decisions.md` |
| adr-writer | `design/adr/adr-NNN-*.md` (status `proposed`) |
| check-plan | advisory report (stdout / JSON); no file write |
| issue-planner | GitHub issues + (optional) Project board |
| prepare-issue | `prompts/issue-NNN-*.md` |
| claude-issue-executor | implementation branch + commits |
| pr-review-packager | GitHub PR (via `gh pr create`) |
| audit-milestone | advisory pass/fail report |
| milestone-summary | `design/milestones/N-summary.md` |
| complete-milestone | closed GitHub milestone; archived `design/state.md` |
| changelog | rendered changelog markdown (stdout / Release body) |
| release | git tag + `gh release create` |
| pause | refreshed `design/state.md` (+ optional `notes/handoff-*.md`) |
| resume | session summary (read-only) |
| workflow-docs | `README.md`, `design/ai-summary.md` |

## Workflow order: docs vs. handoffs

The documented happy-path order in `docs/skills.md` and
`docs/workflow-guide.md` is:

```
idea-to-prd → prd-normalizer → prd-to-mvp → (planning/clarify) →
adr-writer → (check-plan) → issue-planner → prepare-issue →
claude-issue-executor → pr-review-packager →
audit-milestone → milestone-summary → complete-milestone → release
```

Every SKILL.md `## Handoff` next-step pointer is **consistent** with this
order:

- `idea-to-prd` → `prd-normalizer` ✓
- `prd-normalizer` → `prd-to-mvp` / `adr-writer` ✓
- `prd-to-mvp` → `adr-writer` (via "Decisions needing ADRs") ✓
- `planning` / `clarify` → `adr-writer` ✓
- `issue-planner` → `prepare-issue` (+ `workflow-docs`) ✓
- `prepare-issue` → `claude-issue-executor` ✓
- `claude-issue-executor` → `pr-review-packager` ✓
- `audit-milestone` → `milestone-summary` → `complete-milestone` → `release` ✓

No ordering contradiction was found between any handoff and the docs.

## Drift classification

### Blocking (must resolve before M2): **none**

Names, directories, permission categories, and handoff order are fully
self-consistent. There is no contradiction that would corrupt a generated
`kit.json`. The kit is in good shape to seed the machine-readable layer.

### Low-risk fix (small, safe, optional): 2

| ID | Finding | Why low-risk |
|---|---|---|
| LR-1 | **Output-heading inconsistency.** 17/19 skills expose a `## Output` or `## Outputs` heading; `complete-milestone` and `release` describe their outputs inline with no dedicated heading. | Cosmetic/structural only — outputs are documented, just not under a parseable heading. Becomes mildly relevant when M2 Issue 7 adds structured `outputs:` frontmatter, since a uniform heading eases extraction. Defer to that issue or fix opportunistically. |
| LR-2 | **`## Output` vs `## Outputs` singular/plural split.** Both spellings are in use (13 singular, 4 plural). | Pure naming inconsistency. A future structured-frontmatter pass (M2 Issue 7) supersedes prose-heading parsing anyway, so not worth a standalone churn PR now. |

Neither LR item is fixed in this M0 PR — both are best handled inside the
M2 frontmatter work (Issue 7) that will normalise output representation
regardless, rather than as isolated edits that the same code touches
again weeks later.

### Deferred (doc freshness; not a contract problem): 1 cluster

- **DF-1: Stale parenthetical issue/ADR framing in handoff & intro prose.**
  Several skills carry "this was built in / will be built in" parentheticals
  that have since shipped:
  - `changelog`: "Run `/release` (future issue #19)" — `/release` exists.
  - `idea-to-prd`: "`prd-normalizer` (Issue #6)", "`prd-to-mvp` (Issue #7)".
  - `issue-planner`: "(Issue #7)", "`prepare-issue` (Issue #15)",
    "`workflow-docs` (Issue #20)".
  - `prepare-issue`: "(once ADR-014 lands)" — ADR-014 is accepted.

  These are historical breadcrumbs, not contract drift — they don't affect
  names, permissions, or order. They belong to the major-release-boundary
  freshness refresh already tracked as `notes/refactoring-ideas.md` entry
  #6. Recorded here; **deliberately not fixed in M0** to keep this audit
  inspect-only and avoid scope creep into a kit-wide prose sweep.

## Cross-check with existing harness

`audit.py` (the 2026-05-07 harness) regenerated clean: 19 rows,
`fm_name_valid=1` and `fm_name_matches_dir=1` for all, no body over the
500-line or ~5k-token budget, no first-person/second-person violations in
descriptions. This audit adds the permission/handoff/output dimension on
top of that deterministic baseline and reaches the same verdict: the
cohort is consistent.

## Verdict

**No blocking drift.** The skill cohort is ready to seed the M2
machine-readable contract. Two cosmetic output-heading inconsistencies
(LR-1, LR-2) are best folded into the M2 frontmatter work; one
doc-freshness cluster (DF-1) is deferred to the existing freshness
backlog. Nothing here blocks roadmap progress.
