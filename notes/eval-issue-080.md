# Evaluation summary — Issue #80

**Issue:** [#80 — Rename `Design/` → `design/` kit-wide for root-directory casing consistency](https://github.com/olivermorgan2/workflow-generator/issues/80)
**Branch:** `rename-design-directory-lowercase`
**ADRs:** ADR-045 (supersedes ADR-005 on casing only); ADR-044 (provides mechanical-rewrite authority); ADR-005 (superseded by ADR-045)

## What changed

- **Directory rename**: `Design/` → `design/` via two-step `git mv` through `_design_tmp` intermediate (required on macOS APFS / case-insensitive FS where naïve `git mv Design design` fails).
- **Path-string substitution**: `1,186 → 0` `Design/` occurrences in tracked files. 14 deliberately-restored editorial `Design/` references remain in ADR-044/045 prose where the literal old name is the subject of the rename, plus the CHANGELOG migration snippet which references the old name.
- **ADR status changes**:
  - ADR-005: `accepted` → `superseded by ADR-045` (status-line edit only — substantive decision stands).
  - ADR-045: `proposed` → `accepted`.
- **ADR-044/045 editorial restoration**: the bulk sed corrupted both ADRs because their prose describes the rename literally (e.g. "rename Design/ → design/"). Both files were editorially restored — title, option labels, migration snippet rewritten with the working two-step variant. Pre-merge edit, permitted under ADR-044's own criterion 2 (no sentence meaning changes — the bulk rewrite *had* changed sentence meaning for these two files).
- **CHANGELOG**: 31 historical navigation links rewritten (mechanical, navigation accuracy); v4.0.0 (UNRELEASED) entry added documenting the rename, ADR-044, and the migration snippet.
- **Example projects**: `examples/projects/{kb-lookup, phased-podcast-pipeline, slug-utils}/Design` directories also two-step-renamed for consistency (12 files, 3 projects).
- **Session artefacts**: prompt and eval summary committed.

## Commits (13 in order)

| # | SHA | Message |
|---|-----|---------|
| 1 | `8e1b0b8` | `chore(rename): step 1 of two-step Design → design rename (ADR-044, ADR-045, #80)` |
| 2 | `20e310d` | `chore(rename): step 2 of two-step Design → design rename (ADR-044, ADR-045, #80)` |
| 3 | `694a58e` | `refactor(adr): rewrite Design/ → design/ inside ADR bodies (ADR-044, ADR-045, #80)` |
| 4 | `63c9ef0` | `refactor(bin): update Design/ → design/ in scripts (ADR-044, ADR-045, #80)` |
| 5 | `1fb5a15` | `refactor(root): rewrite Design/ → design/ in root files (ADR-044, ADR-045, #80)` |
| 6 | `d133739` | `refactor(docs): rewrite Design/ → design/ in user-facing docs and install templates (ADR-044, ADR-045, #80)` |
| 7 | `de2c112` | `refactor(skills): rewrite Design/ → design/ in skill files (ADR-044, ADR-045, #80)` |
| 8 | `ed6a09b` | `refactor(examples): rewrite Design/ → design/ in examples and CI configs (ADR-044, ADR-045, #80)` |
| 9 | `71049bc` | `refactor(archive): rewrite Design/ → design/ in archived materials (ADR-044, ADR-045, #80)` |
| 10 | `5808f19` | `refactor(notes): rewrite Design/ → design/ in notes and prompts (ADR-044, ADR-045, #80)` |
| 11 | `9060fda` | `feat(adr): supersede ADR-005 with ADR-045 on Design/ casing (ADR-044, ADR-045, #80)` |
| 12 | `1be0ebe` | `docs(changelog): document Design/ → design/ rename and migration (ADR-044, ADR-045, #80)` |
| 13 | TBD | `chore(examples): rename example-project Design/ → design/ for kit consistency (ADR-044, ADR-045, #80)` |
| 14 | TBD | `chore(session): record #80 verified state and eval summary (ADR-044, ADR-045, #80)` |

(Commits 13 and 14 are this commit and the orchestration commit; SHAs assigned at commit time.)

## Verification performed

| # | Command | Result |
|---|---------|--------|
| V1 | `git ls-files \| grep -E '^Design/' \| wc -l` | **0** ✓ |
| V2 | `find . -type d -name Design` | **empty** ✓ (after commit 13 fixed example projects) |
| V3 | `git grep -l 'Design/'` | **3 files** (CHANGELOG.md, design/adr/adr-044/045 — all deliberately retained in editorial prose) |
| V4 | `bin/sync-adr-index --check` | **EXIT=0**, "index is in sync" ✓ |
| V5 | `bin/check-state-cap` | **EXIT=0** ✓ |
| V6 | `grep -rln 'Design/' examples/projects/` | **0** ✓ |
| Bonus | `bin/check-plan --criteria-set adr` against all 45 ADRs | **24/45 pass**; 21 pre-existing failures on older ADRs (C4 — Decision body doesn't name an Option label) — verified unchanged from main pre-rewrite, no regressions introduced |

The kit is docs-only; no test runner. Verification is grep / find / bin/check-plan.

## Follow-ups

- **PR description requirements per ADR-044 Consequences** — `/pr-review-packager` will draft. The PR body must include: (a) "This PR invokes ADR-044's mechanical-rewrite exception"; (b) exact transformation rule `Design/ → design/`; (c) runnable command (the two-step variant from CHANGELOG entry); (d) affected ADR numbers (16 accepted: 005, 008, 018, 022, 023, 024, 025, 026, 027, 028, 031, 032, 033, 035, 037, 042; plus ADR-044 and ADR-045 in `design/adr/`); (e) occurrence count `1,186 → 0`.
- **Refactoring-ideas entry #7** can be marked `shipped` after this PR merges.
- **Pre-existing ADR-C4 failures (21 ADRs)** are surfaced for visibility but **out of scope** for this PR. They predate the C4 criterion. A separate issue could retroactively add Decision-references-Option-label patches to the older ADRs (mechanical edit, would qualify under ADR-044). Capture as a feature-ideas entry if relevant.
- **Example-project consistency caught at verification** — the bulk sed rewrote example file *contents* but missed the directory names. Fixed in commit 13. Worth noting for future kit-wide renames: the two-step `git mv` step must be applied recursively to every nested directory matching the pattern, not just the top-level one. Could be a small bin/-helper opportunity.

No `### design-questions` block — this issue raises no cross-issue carry-forward (the rename ships in this PR; no follow-up issue depends on a design question raised here).

## Commands the user should run

```bash
# 1. Inspect the diff vs main
git -C /Users/olivermorgan/Documents/Oliver/workflow-generator log main..HEAD --stat | head -50

# 2. Confirm the rename
git -C /Users/olivermorgan/Documents/Oliver/workflow-generator ls-files | grep -E '^Design/' | wc -l   # → 0
find /Users/olivermorgan/Documents/Oliver/workflow-generator -type d -name Design                      # → empty

# 3. Re-run verification commands
cd /Users/olivermorgan/Documents/Oliver/workflow-generator
bin/sync-adr-index --check
bin/check-state-cap
bin/check-plan --criteria-set adr --input design/adr/adr-005-documentation-and-template-architecture.md
bin/check-plan --criteria-set adr --input design/adr/adr-044-mechanical-rewrite-immutability-exception.md
bin/check-plan --criteria-set adr --input design/adr/adr-045-rename-design-directory-lowercase.md

# 4. Visual sanity-check the editorial Design/ references that were intentionally retained
git -C /Users/olivermorgan/Documents/Oliver/workflow-generator grep 'Design/'
```

## Next step

`/pr-review-packager` to package the PR. The packager's category-3 contract requires explicit `yes` before `gh pr create` — the user reviews the rendered PR body in chat first.

After PR merges:
1. Switch to main, pull.
2. Mark `notes/refactoring-ideas.md` entry #7 as `shipped` (move to Filed section with PR number).
3. Run `/release` to cut v4.0.0.
