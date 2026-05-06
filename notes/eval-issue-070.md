# Evaluation summary — Issue #70 (ADR-041)

## What changed

- **`docs/workflow-guide.md`** — added new top-level **§7 "Auto-mode permission contract (ADR-041)"** as the canonical source of truth (160 lines). Subsections: introductory framing, the three categories with examples, exhaustive per-skill classification table (19 skills), category-2 instance (`/claude-issue-executor` + ADR-039 alignment-review obligation), category-3 instance (`/pr-review-packager` confirmed-yes pattern), `--no-prompt` interaction (ADR-038), schema-drift enforcement (deferred to #72/ADR-034), pointers.
- **`skills/claude-issue-executor/SKILL.md`** — added `permission-category: 2` front-matter line; added §7 cross-reference at the top of *Plan-mode rhythm*; inserted new `### Auto-mode behaviour (per ADR-041)` subsection between *Hybrid path* and *Alignment-review obligation* codifying the ask-once rule (yes / no / decide-from-scope) with mandatory written acknowledgement on the "no" branch; expanded *Alignment-review obligation* to cover §7 ↔ checklist sync.
- **`skills/pr-review-packager/SKILL.md`** — added `permission-category: 3` front-matter line; inserted new top-level section **`## Auto-mode permission category (per ADR-041)`** between *What this skill does not do* and *Inputs*, codifying the existing confirmed-yes pattern (steps 12–13) as the canonical category-3 behaviour: explicit `yes` required regardless of mode.
- **17 other shipped `skills/*/SKILL.md`** — added `permission-category: <N>` front-matter line. Categories: 14 cat-1 (adr-writer, audit-milestone, changelog, check-plan, clarify, idea-to-prd, milestone-summary, pause, planning, prd-normalizer, prd-to-mvp, prepare-issue, resume, workflow-docs); 3 cat-3 (complete-milestone, issue-planner, release).
- **`prompts/issue-070-auto-mode-permission-contract.md`** — committed as commit 0 on the feature branch (matches the `c81a9d0` precedent for issue #69).

## Commits

```
3779ad2  docs(prompts): add prompt for issue #70 (ADR-041, #70)
b7c3f50  feat(docs): add auto-mode permission contract to workflow guide (ADR-041, #70)
6cd2778  feat(skills): instance contract in claude-issue-executor (ADR-041, #70)
71eadf5  feat(skills): codify category-3 confirmed-yes in pr-review-packager (ADR-041, #70)
ab64982  chore(skills): add permission-category front-matter to all shipped skills (ADR-041, #70)
```

Branch: `auto-mode-permission-contract` off `main`. Five commits total. Each commit message references both the governing ADR (`ADR-041`) and the issue number (`#70`). The front-matter sweep is split into its own commit (5) so the contract-content commits (2/3/4) stay reviewable without 17-file noise.

## Verification performed

Markdown-only kit, no test runner. Verification is read-back checks against the 5 acceptance criteria from the prompt and the AC4 standard mirror from ADR-040.

- **AC1** (contract appears in `docs/workflow-guide.md` as single source of truth, three categories named, every shipped operation classified) — `grep -n "^## 7\." docs/workflow-guide.md` matches `## 7. Auto-mode permission contract (ADR-041)` at line 618. §7 read end-to-end: all six subsections present (categories, classification table, cat-2 instance, cat-3 instance, `--no-prompt` interaction, schema-drift enforcement). The classification table names all 19 shipped skills with their gating operations.
- **AC2** (every shipped skill's SKILL.md front-matter declares its permission category) — `grep -L "^permission-category:" skills/*/SKILL.md` returns empty (all 19 files pass). Spot-checked 4 skills (claude-issue-executor, pr-review-packager, release, prepare-issue) — all have the line at the expected position with the expected category and rationale comment.
- **AC3** (`claude-issue-executor` under auto-mode asks the plan-mode question at session start; "no" requires written acknowledgement) — `grep -n "Auto-mode behaviour" skills/claude-issue-executor/SKILL.md` matches at line 301. The subsection prescribes the literal ask-once question text and the literal acknowledgement text required on the "no" branch, including the *"before any mutating edit"* timing constraint.
- **AC4** (`pr-review-packager` continues to require explicit `yes` for category-3 operations regardless of mode — codified, not just observed) — `grep -n "Auto-mode permission category" skills/pr-review-packager/SKILL.md` matches at line 68. The new section explicitly cites steps 12–13 of the existing execution protocol as the canonical implementation, with a no-regression clause: *"If a future change ever proposes silencing the explicit-yes gate under auto-mode, it must be rejected at PR review as a cat-3 violation."*
- **AC5** (a new skill author has one document to consult when adding a strict-mode gate) — §7 is that document. The Pointers subsection cross-references the two skill-spec instances and the related ADRs (038, 039, 040, 041). Skill SKILL.md files cite §7 as canonical.

**AC4-mirror inspection (from ADR-040 standard).** Three hypothetical new skill operations applied mentally:

- `/lint-skills` (would lint local SKILL.md files) → cat-1 (substitutable; no public state change, no hard-to-reverse blast radius). Clear placement.
- `/auto-merge-pr` (hypothetical) → cat-3 (PR merge is hard-to-reverse and public). Clear placement.
- `/refactor-imports` (bulk file edits across the repo with no public-state writes) → cat-2 (significant-task plan-mode required; reversible-locally but blast radius beyond a single small fix). Clear placement.

All three placed without operator judgment. The category boundaries (public vs local; reversible vs not; explicit-gate-required vs operator-acknowledged-bypass-possible vs no-gate-needed) are concrete.

**Inline integrity checks (re-run the verification block from the plan):**

```
1. grep -L "^permission-category:" skills/*/SKILL.md       → empty (PASS)
2. grep -n "^## 7\." docs/workflow-guide.md                 → line 618 (PASS)
3. all 19 skills named in §7                                → 19 OK / 0 MISSING (PASS)
4. ADR-039 cross-reference present in §7                    → 4+ matches in §7 (PASS)
5. claude-issue-executor "Auto-mode behaviour" subsection   → line 301 (PASS)
6. pr-review-packager "Auto-mode permission category"       → line 68 (PASS)
```

## Follow-ups

- **Schema-drift enforcement is PR-review-only.** §7's classification table and per-skill front-matter values can drift if a future PR adds a category-3 operation under auto-mode without updating both surfaces. Long-term home for enforcement is the ADR-034 plan-checker structural-rule framework once issue #72 / ADR-043 lands. Captured both inline in §7 and here so a future reader does not re-litigate. (This is the same structural-rule framework that ADR-040's §6 schema-drift check is queued behind — both checks land together.)
- **Front-matter rationale comments.** Each `permission-category` line includes a brief rationale comment (e.g. *"# substitutable — drafts ADRs locally; user accepts manually, per workflow-guide §7"*). The comment is a reader's-aid; the canonical truth is §7. If §7's table evolves and a per-skill comment becomes inconsistent, PR review must catch it. Considered building this into the front-matter as a structured field rather than a YAML comment, but the comment form has the right tradeoff: visible at-glance in front-matter, not load-bearing for any tooling.
- **`Design/state.md` is absent in this repo.** Per ADR-035, the executor's session protocol step 11 updates `state:in-flight` if the file exists; absent, skip silently. This kit repo has not adopted ADR-035 internally (the kit *ships* state.md as a target-project artefact). No drift; flagged here for completeness so the alignment check below can mark the step as N/A rather than missed.

No `### design-questions` block emitted. Two design questions surfaced during this session (the future-proofing note for non-trivial bypass paths, and the schema-drift deferral) — neither qualifies under the §6 when-to-populate rule:

- The future-proofing note describes a hypothetical future skill or mode; no specific filed-or-planned issue depends on the answer (excluder #2 — no upcoming dependent issue). Captured in §7 itself and in *Follow-ups* above; will resurface as a real design question if/when such a mode is filed.
- The schema-drift deferral is already documented in ADR-040 (`Maintain` paragraph) and ADR-041 itself (`Maintain` paragraph) and mirrored in §7 and §6. Not net-new — excluder #4 (already covered by an ADR).

Per §6's borderline rule: when in doubt, omit. Both omitted.

## Commands the user should run

```bash
# Inspect the branch
git log main..HEAD --oneline
git diff main..HEAD --stat

# Read §7 of the workflow guide
sed -n '618,$p' docs/workflow-guide.md

# Confirm every shipped SKILL.md has a permission-category line
grep "^permission-category:" skills/*/SKILL.md

# Confirm the cat-2 ask-once rule in claude-issue-executor
sed -n '301,360p' skills/claude-issue-executor/SKILL.md

# Confirm the cat-3 codification in pr-review-packager
sed -n '68,95p' skills/pr-review-packager/SKILL.md

# Apply the AC4 mirror — read the three categories and check placement of three hypothetical operations
sed -n '/^### The three categories/,/^### Per-skill classification/p' docs/workflow-guide.md

# Read this eval summary back
cat notes/eval-issue-070.md
```

## Next step

`/pr-review-packager` to draft a PR from the `auto-mode-permission-contract` branch. The packager (now declaring itself category 3 in front-matter — meta-dogfooding) will require explicit `yes` before opening the PR, regardless of session mode. No `### design-questions` block in this eval, so no `## Notes for #N` sections will be emitted in the PR body.

The branch is not yet pushed; the user should `git push -u origin auto-mode-permission-contract` before invoking the packager.

## Alignment check

- [x] The plan was proposed and explicitly approved before any edits (plan mode entered, plan file written to `/Users/olivermorgan/.claude/plans/dynamic-frolicking-willow.md`, user approved via ExitPlanMode).
- [x] A feature branch was created from `main` (`auto-mode-permission-contract`); no commits to `main`.
- [x] Every commit message includes `ADR-041` and `#70`.
- [x] Tests are not applicable (markdown-only kit); verification is read-back per the prompt's evaluation section.
- [x] An evaluation summary was printed and persisted to `notes/eval-issue-070.md` (per ADR-040).
- [x] The session raised no cross-issue design questions matching §6's when-to-populate rule; the `### design-questions` block was omitted (per ADR-040 *Empty case*). Reasoning recorded in *Follow-ups*.
- [x] `/pr-review-packager` is suggested, not auto-invoked.
- [x] `Design/state.md` step skipped silently (file absent in kit repo, per ADR-035).
