# Evaluation summary — Issue #69 (ADR-040)

## What changed

- **`docs/workflow-guide.md`** — added new top-level **§6 "Cross-skill carry-forward (ADR-040)"** as the canonical schema source of truth (159 lines), plus three one-line forward-references at the end of §2.d, §2.e, §2.f.
- **`skills/claude-issue-executor/SKILL.md`** — added ADR-040 link; added `notes/eval-issue-NNN.md` to the Outputs section as a session artefact; expanded session-protocol step 12 to write the eval file; added structured `### design-questions` subsection under Evaluation summary citing §6; added alignment-check item.
- **`skills/pr-review-packager/SKILL.md`** — added ADR-040 link; added 5th data source (eval-summary file); added new step 6.5 to scan for `### design-questions`; updated step 11 (template fill) to append `## Notes for #M` sections grouped by `target-issue`; added self-check item.
- **`skills/prepare-issue/SKILL.md`** — added ADR-040 link; added `--pr-scan-limit` flag (default 30); added 4th data source (recently-merged PRs); added step 6.5 to scan for `## Notes for #<NNN>`; updated template-filling rules to insert `## Design questions carried forward from PR #M` before `Requirements`; added 3 edge cases; added self-check item.
- **`skills/pr-review-packager/example.md`** — added new variant **§7 "Design-questions round-trip (per ADR-040)"** (155 lines) with a worked synthetic two-issue pair (#100/#101) showing all three on-disk artefacts back-to-back: eval file → PR body → generated prompt.
- **`prompts/issue-069-cross-skill-design-question-carry-forward.md`** — committed to `main` (commit 0) before branching; pairs with the existing `prompts/` convention.

## Commits

```
c81a9d0  docs(prompts): add prompt for issue #69 (ADR-040, #69)                                 [main]
be221e8  docs(workflow-guide): add cross-skill design-questions schema (ADR-040, #69)
256210e  feat(skills): emit design-questions in eval summary (ADR-040, #69)
747b418  feat(skills): emit Notes for #N sections in PR body (ADR-040, #69)
3575acd  feat(skills): scan merged PRs for carried-forward design-questions (ADR-040, #69)
d479bcc  docs(skills): add design-questions round-trip example (ADR-040, #69)
```

Branch: `cross-skill-design-question-carry-forward` off `main`. Five commits on the branch (excluding the prompt commit on main). Each commit format `<verb>(<scope>): <subject> (ADR-040, #69)`.

## Verification performed

Markdown-only kit, no test runner — verification is read-back checks against the 5 acceptance criteria from the prompt:

- **AC1** (schema in `docs/workflow-guide.md` as named, versioned section) — `grep -n "^## 6\." docs/workflow-guide.md` → matches `## 6. Cross-skill carry-forward (ADR-040)` at line 481. `grep -n "version 1" docs/workflow-guide.md` → matches the `Canonical schema (version 1)` heading at line 492 and the lockstep-update obligation at line 590. §6 read end-to-end: all 8 components present (rationale, schema, when-to-populate, when-NOT-to-populate, file/section names, schema versioning, --no-prompt interaction, pointers).
- **AC2** (skill specs reference §6 without restating) — `grep -n "workflow-guide.md#6\|workflow-guide.md §6"` finds 9 hits across the three skill specs (3 in each). Each `### design-questions`-style subsection cites §6 as the canonical source and provides only a reader's-aid example, not a duplicate spec.
- **AC3** (worked example end-to-end) — `skills/pr-review-packager/example.md` §7 "Design-questions round-trip (per ADR-040)" shows a synthetic #100/#101 pair with three on-disk excerpts (eval file, PR body, generated prompt) back-to-back. Producer → preserver → consumer trace is one read.
- **AC4** (when-NOT-to-populate rule concrete enough to route without operator judgment) — §6 lists 4 explicit excluder cases (self-resolved, no upcoming dependent issue, tactics-not-architecture, already-covered-by-ADR) plus a borderline-tiebreaker. Mentally applied to issues #56 (clear no — self-contained feature, excluder 1), #57 (clear no — no dependent issue at the time, excluder 2), #58 (clear yes — load-bearing carry-forward question, target ADR-040). Rule produces a yes/no on each without further author input.
- **AC5** (`bin/sync-adr-index --check` clean) — exit 0, message `sync-adr-index: index is in sync`. `git diff main..HEAD --stat -- 'Design/adr/**'` is empty (no ADR file edits in this issue).

Smoke checks beyond the ACs:
- Three forward-refs at lines 165, 232, 255 of `docs/workflow-guide.md` all named correctly (`Cross-issue carry-forward`, `Carry-forward output`, `Carry-forward propagation`) and point to §6.
- `git log main..HEAD --oneline` shows 5 commits in the correct order with the correct format.
- Working tree clean after the eval file is committed.

## Follow-ups

- **Schema-drift fragility (acknowledged).** Three SKILL.md files now share a load-bearing structured-data contract referenced from one workflow-guide section. There is no machine-checkable enforcement that they stay aligned — drift is caught at PR-review time only. Long-term home for enforcement is the ADR-034 plan-checker once ADR-043 (issue #72) lands a generic structural-rule framework. Mentioned in §6 itself; recorded here so a future reader does not re-open the question.
- **PR-scan default of 30 is a heuristic.** Repos with very high or very low PR cadence may want to override via `--pr-scan-limit`. Defer making the default repo-shape-aware (e.g. detect median merge cadence) until cadence variance becomes a problem in practice.
- **`notes/` as home for the eval-summary file.** Chosen for proximity to the existing `prompts/issue-NNN-*.md` convention. Flag for retrospective at v3.4.0 milestone close — if `notes/` accumulates many `eval-issue-*.md` files, consider promoting to a dedicated `Design/evals/` folder.
- **ADR-038 alignment-review re-trigger.** The audit at `notes/adr-038-alignment-review.md` reviews the prompt's content boundary. ADR-040 introduces a new prompt subsection (`## Design questions carried forward from PR #M`), but the new subsection is **populated at fill-time by `prepare-issue`** rather than added to `prompts/_template.md` itself. The audit's "future trigger" clause fires only on template additions, so the trigger does not fire here. Documented now to forestall re-litigation.

### design-questions

```yaml
- title: Schema-evolution governance for design-questions
  target-issue: "#70"
  context: |
    The ADR-040 schema is documented as version 1 in
    docs/workflow-guide.md §6, with a lockstep-update obligation
    that says "when the schema evolves, update §6 first then
    update the three SKILL.md cross-references in the same change."
    No machine-checkable enforcement exists — drift between the
    canonical §6 schema and any one SKILL.md cross-reference
    silently breaks the carry-forward loop. Issue #70 implements
    ADR-041 (auto-mode permission contract) which lands kit-wide
    classification machinery; consider whether that work should
    also include a sibling drift-checker (e.g. a CI step or a
    bin/check-design-questions-schema-drift script), or whether
    the long-term home is the ADR-034 plan-checker once #72 lands
    a generic structural-rule framework. Decide before #70 starts
    so the scope is explicit.

- title: Notes for #N section grammar
  target-issue: "#72"
  context: |
    Issue #69 ships the kit-canonical PR-body section header
    `## Notes for #<N>` as the anchor that prepare-issue scans
    for via grep. Issue #72 implements ADR-043 (programmatic
    /check-plan) which may define a formal grammar for PR-body
    sections that downstream skills consume. If #72's grammar
    rules end up listing canonical section headers (it would be
    a natural place for ADR-references checks already present in
    pr-review-packager), the `## Notes for #<N>` shape should be
    added so the prepare-issue scanner can lean on a parser rather
    than ad-hoc grep. The downside of grep is fragility around
    minor markdown variations (extra whitespace, alternate hash
    counts); a parser closes that gap.

- title: --no-prompt interaction with carry-forward
  target-issue: "#70"
  context: |
    ADR-040 (and §6 of the workflow guide) document that
    --no-prompt skips prepare-issue and therefore the carry-forward
    consumer step. This is acceptable because the trivial-issue
    criteria (single typo, dependency bump, ADR status flip) by
    definition do not raise cross-issue design questions. ADR-041
    (issue #70) generalises auto-mode behaviour into a kit-wide
    permission contract with three categories (substitutable,
    operator-acknowledged-bypass, non-substitutable). If ADR-041's
    auto-mode introduces new bypass code paths for non-trivial
    reasons (e.g. CI-driven implementations, bulk migrations), the
    --no-prompt-skips-carry-forward exemption needs revisiting:
    bypassing carry-forward silently on a non-trivial issue would
    re-open the gap ADR-040 was written to close. Decide whether
    ADR-041's permission categories cover this case explicitly, or
    whether a follow-up ADR amendment is needed.
```

## Commands the user should run

```bash
# Inspect the branch
git log main..HEAD --oneline
git diff main..HEAD --stat

# Read §6 of the workflow guide
sed -n '481,617p' docs/workflow-guide.md

# Confirm cross-references in the three skill specs
grep -n "workflow-guide.md#6\|workflow-guide.md §6" \
  skills/claude-issue-executor/SKILL.md \
  skills/pr-review-packager/SKILL.md \
  skills/prepare-issue/SKILL.md

# Read the round-trip example
sed -n '213,367p' skills/pr-review-packager/example.md

# Verify ADR index is clean
bin/sync-adr-index --check
git diff main..HEAD --stat -- 'Design/adr/**'

# Read this eval summary back
cat notes/eval-issue-069.md
```

## Next step

`/pr-review-packager` to draft a PR from the `cross-skill-design-question-carry-forward` branch. The packager will read this file and emit `## Notes for #70` and `## Notes for #72` sections in the PR body (the bootstrap of the very chain this issue ships — it gets to dogfood itself). The carry-forward then survives in PR history and reaches `prepare-issue 70` and `prepare-issue 72` deterministically.

The branch is not yet pushed; the user should `git push -u origin cross-skill-design-question-carry-forward` before invoking the packager.

## Alignment check

- [x] The plan was proposed and explicitly approved before any edits.
- [x] A feature branch was created from `main` (the prompt was committed to main first as commit 0; the 5 implementation commits are on the feature branch).
- [x] Every commit message includes `ADR-040` and `#69`.
- [x] Tests are not applicable (markdown-only kit); verification is read-back per the prompt's evaluation section.
- [x] An evaluation summary was printed and persisted to this file (per ADR-040 — dogfooded).
- [x] The session raised cross-issue design questions; a `### design-questions` block was added above with three entries targeting #70 (×2) and #72.
- [x] `/pr-review-packager` is suggested, not auto-invoked.
