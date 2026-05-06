# Eval — issue #71: Project-shape detection in `/release` (ADR-042)

**Branch:** `project-shape-detection-in-release`
**Driver:** `/claude-issue-executor` (chat-plan-gate run with operator-acknowledged plan-mode bypass per workflow-guide §7 cat-2)
**Prompt:** `prompts/issue-071-project-shape-detection-in-release.md`
**ADR:** [ADR-042 — Project-shape detection in `/release` for non-product projects](../Design/adr/adr-042-project-shape-detection-in-release.md)
**Date:** 2026-05-06

## What changed

**Spec surface for `/release` (3 commits on `skills/release/SKILL.md`):**

- New `## Project-shape detection` section between Prerequisites check and Preceding-tag detection. Documents the four detection signals (PRD-language, build-strategy, success-criteria-shape, package-manifest), the ≥2 threshold, the resulting `shape` value (`product` | `workflow`), and the missing-PRD/build-out fallback. Declared the single source of truth for the signal list.
- New `### Overrides` sub-section explaining `--force-product-shape` and `--force-workflow-shape` flags (mutually exclusive; override visibility surfaced in the release plan).
- New `--force-product-shape` and `--force-workflow-shape` entries in the Invocation flags table, with usage block updated to show the mutually-exclusive group.
- Release flow renumbered to 1–10 with new step 2: "Run project-shape detection." Step 7 (was 6, "Assemble the release plan") gains a `Project shape:` bullet and inline rendering of the workflow-shape clarifier banner when `shape = workflow`.
- Execution sequence pseudo-code updated to prepend the clarifier banner to the temp file consumed by `git tag -a` and `gh release create` (workflow-shape only; product-shape unchanged).
- Dry-run mode updated: now runs steps 1–7 (was 1–6) so the dry-run preview shows whether the clarifier would have been emitted.
- Five new edge-case rows: mutually-exclusive flag rejection, zero-signal default to product, override-conflicts-with-detection in both directions, missing PRD + build-out fallback.
- Two new self-check items: detection ran and reported in the plan; clarifier rendered and prepended for `shape = workflow`.

**Worked example for `/release` (1 commit on `skills/release/example.md`):**

- New `## Workflow-shape variant — research-shaped project, first release` walkthrough, parallel to the existing product-shape Pace Drift walkthrough. Project: `lit-review-2026` (markdown-only research repo). All four signals fire; demonstrates detection scoring, plan rendering with clarifier banner, annotated tag content, and final report.
- New `## Override variants` section with three subsections: `--force-workflow-shape` on a sub-threshold project, `--force-product-shape` on a tripped-detection project, and the mutually-exclusive abort.

**Workflow-guide cross-reference (1 commit on `docs/workflow-guide.md`):**

- New paragraph in `### 2.i Tagged release` introducing project-shape detection at one-paragraph context and pointing at `skills/release/SKILL.md § Project-shape detection` as the canonical signal list. Single-source-of-truth pattern: workflow guide names the feature, links back, does not duplicate the four-signal table.

**Issue input artefact (1 file added in commit 1):**

- `prompts/issue-071-project-shape-detection-in-release.md` — input artefact written by `/prepare-issue 71` in the prior session phase. Lands on the feature branch as part of commit 1 per the kit's established pattern (PRs #74, #75, #76).

## Commits

| # | SHA | Subject |
|---|---|---|
| 1 | `08fd5e0` | `feat(release): document project-shape detection signals and threshold (ADR-042, #71)` |
| 2 | `9ea42e1` | `feat(release): add --force-product-shape and --force-workflow-shape override flags (ADR-042, #71)` |
| 3 | `5397e32` | `feat(release): emit workflow-shaped clarifier for non-product projects (ADR-042, #71)` |
| 4 | `b9c8d4e` | `docs(release): add worked workflow-shape example (ADR-042, #71)` |
| 5 | `751c051` | `docs(workflow-guide): cross-reference project-shape detection signals (ADR-042, #71)` |

Total diff: **+474 / -11** across 4 files. Each commit one logical change with the canonical `(ADR-042, #71)` audit-trail suffix in the subject.

**Pre-implementation prelude (separate `notes:` direct-to-main commit on `main`, not on this branch):**

- `e98796e notes: refresh README to match post-archive structure; capture notes/ folder cleanup follow-up` — `notes/README.md` refresh + new `notes/bug-fixes.md` entry. Unrelated to ADR-042; bundled per the kit's `notes:` direct-to-main convention so the feature branch stays scoped.

## Verification performed

- **Commit-message audit:** `git log --oneline main..HEAD` returns 5 commits, each with `(ADR-042, #71)` suffix. ✓
- **Scope audit:** `git diff --stat main..HEAD` reports 4 files: `skills/release/SKILL.md`, `skills/release/example.md`, `docs/workflow-guide.md`, `prompts/issue-071-project-shape-detection-in-release.md`. Matches plan exactly. No `templates/`, `bin/`, ADR, or other-skill changes. ✓
- **`bin/check-plan --criteria-set adr` regression** (against `Design/adr/adr-042-project-shape-detection-in-release.md`): 5 PASS + 1 WARN. The single WARN is `ADR-C6` (semantic-conflict check deferred to v2 of the eval lib per ADR-034) — not a regression, present on every ADR. ✓
- **`bin/check-plan --criteria-set prompt` regression** (against `prompts/issue-071-project-shape-detection-in-release.md`): 5/5 PASS (PROMPT-C1, C2, C3, C5, C6). Same gate that ran in the `/prepare-issue` phase. ✓
- **No tests run** — kit is markdown spec-only (no `package.json` test script, no `pytest.ini`, no `go.mod`). Per the executor skill's test-alongside detection rules, this is the documented expected behaviour for a prose-only skill.
- **Acceptance-criteria audit (5/5 mapped to specific content):**

  | AC | Where it's met |
  |---|---|
  | **AC1** — `/release` on a project matching ≥2 non-product signals emits the workflow-shaped clarifier without operator action | `skills/release/SKILL.md` § Project-shape detection (Detection signals + Threshold + Outcome) + Release flow steps 2 and 7 + Execution sequence step 1 (clarifier prepend block). Worked example: `skills/release/example.md` § Workflow-shape variant (4/4 signals fire; clarifier rendered in step 6 plan; appears in final release body). |
  | **AC2** — `/release --force-product-shape` overrides detection and produces standard product framing | `skills/release/SKILL.md` Invocation flag entry + § Project-shape detection / Overrides + Edge cases row "scores ≥2 but operator passed --force-product-shape". Worked example: `skills/release/example.md` § Override variants → `--force-product-shape on a project that tripped detection`. |
  | **AC3** — `/release --force-workflow-shape` opts into workflow framing on a project that did not trip detection | `skills/release/SKILL.md` Invocation flag entry + § Project-shape detection / Overrides + Edge cases row "scores 0 or 1 but operator passed --force-workflow-shape". Worked example: `skills/release/example.md` § Override variants → `--force-workflow-shape on a project that did not trip detection`. |
  | **AC4** — The signal list in SKILL.md is exhaustive and matches the workflow-guide cross-reference (no drift) | `skills/release/SKILL.md` § Project-shape detection / Detection signals lists 4 signals verbatim from ADR-042 Decision (declared single source of truth). `docs/workflow-guide.md` § 2.i adds a one-paragraph introduction that points at SKILL.md as canonical and explicitly avoids maintaining a parallel list. |
  | **AC5** — A worked example demonstrates each path (product, auto-detected workflow, both override flags) | `skills/release/example.md` covers all four paths: existing Pace Drift walkthrough = product; new lit-review-2026 walkthrough = auto-detected workflow; Override variants = both `--force-*` flags + mutually-exclusive abort. |

- **Manual markdown read** of all four touched files: heading hierarchy intact, tables render correctly, fenced code blocks balanced, blockquote rendering of clarifier banner consistent with ADR-042 Decision.

## Follow-ups

None blocking for upcoming filed issues. ADR-042 enumerates three deferred items in its Consequences section, none of which surfaced as concrete blockers during this implementation:

1. **Extending detection to `/changelog` and `/audit-milestone`** — out of scope per ADR-042; revisit if leakage shows up in future evals.
2. **Date-based snapshot tags (e.g. `2026.05` instead of `0.1.0`) for non-product projects** — deferred per ADR-042; the version-number convention stays semver-shaped with the clarifier banner doing the framing work. No change.
3. **Reusing detection across skills via a shared helper** — explicitly "left to the implementing issue if the pattern repeats" per ADR-042. This is the first instance; pattern has not repeated. If `/changelog` or `/audit-milestone` later grow detection, that issue can revisit shared-helper extraction.

(The `### design-questions` block per ADR-040 is omitted: per §6 of the workflow guide, populate only when *all three* hold — the question concerns a load-bearing constraint, a specific filed upcoming issue depends on the answer, and this issue's commits do not fully resolve it. None of the deferred items in ADR-042 have filed issues that depend on them; they live as ADR-level deferrals, not cross-issue carry-forwards.)

## Commands to reproduce verification

```bash
# 1. Confirm the 5 issue-071 commits with proper audit-trail suffixes.
git log --oneline main..HEAD

# 2. Confirm the planned 4 files are touched and only those.
git diff --stat main..HEAD

# 3. Re-run the check-plan regressions.
bin/check-plan --criteria-set adr --input Design/adr/adr-042-project-shape-detection-in-release.md
bin/check-plan --criteria-set prompt --input prompts/issue-071-project-shape-detection-in-release.md

# 4. Read the modified surfaces end-to-end.
$EDITOR skills/release/SKILL.md          # focus on § Project-shape detection, Invocation flags, Release flow steps 2 and 7, Execution sequence step 1, Edge cases, Self-check
$EDITOR skills/release/example.md        # focus on § Workflow-shape variant + § Override variants
$EDITOR docs/workflow-guide.md           # focus on § 2.i (the new project-shape-detection paragraph)
```

## Next step

`/pr-review-packager` to draft a pull request from this branch using the commit history and the governing ADR-042. Do not invoke automatically — preserves the human review checkpoint between implementation and PR publication per ADR-015.
