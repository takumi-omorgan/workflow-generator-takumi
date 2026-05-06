# Evaluation summary — Issue #72 (ADR-043)

## Scope note (narrow, not broad)

The plan was originally approved as **broad** (all 5 skills, including
3 new criteria sets for changelog / milestone-summary / pr-body). After
the dispatcher was written and writing of the eval lib began, an honest
re-assessment surfaced that authoring 3 net-new criteria sets in pure
bash without proper test fixtures was a meaningful risk: the migrated
skills would then trust evaluators that hadn't been verified against
real failure modes.

The user redirected to **narrow scope** (option 2): ship the
infrastructure plus migration of the 2 skills with explicit
`/check-plan` chain points today (`adr-writer`, `prepare-issue`).
The 3 new criteria sets are reserved-but-not-yet-implemented in the
dispatcher (rejected with exit 2 and a clear message) and become
follow-up issues. This eval reflects the narrow shipped scope.

## What changed

- **`bin/check-plan`** — new ~250-line bash script. Programmatic
  equivalent of `/check-plan` per ADR-043. Flag-parses
  `--criteria-set`, `--input`, `--format`, `--non-interactive`. Reads
  the input from a path or stdin (via tempfile). Sources
  `bin/lib/check-plan-eval.sh` and dispatches on `--criteria-set`.
  Renders text or JSON. Computes exit code from records. Has a
  cleanup trap that explicitly returns 0 (early bug — see *Bugs
  fixed during implementation*).
- **`bin/lib/check-plan-eval.sh`** — new ~370-line bash module. Two
  evaluator functions (`eval_adr_criteria`, `eval_prompt_criteria`)
  implementing the ADR-C1..C6 and PROMPT-C1..C6 criteria from
  `skills/check-plan/criteria.md`. Each emits TSV records to
  stdout that the dispatcher converts to text or JSON.
- **`skills/check-plan/SKILL.md`** — adds a *Two surfaces, one source
  of truth* subsection explaining the bin/-vs-slash-command split.
  Rewrites execution-protocol steps 3–4 to delegate to
  `bin/check-plan` rather than describing inline criteria
  evaluation. Updates *How chained mode works* to reference
  `bin/check-plan` directly.
- **`skills/check-plan/example.md`** — adds section 4 *Two surfaces,
  one source of truth (per ADR-043)* showing both surfaces produce
  identical pass/fail output for the same input, plus the JSON
  shape consumed by chained skills, the stdin pattern, and the
  reserved-criteria-set rejection.
- **`skills/adr-writer/SKILL.md`** — step 7 *Pre-write check*
  migrates from "invoke /check-plan" to "pipe rendered ADR into
  bin/check-plan --criteria-set adr --input - --format json" with
  a paragraph explaining the surface choice per ADR-043.
- **`skills/prepare-issue/SKILL.md`** — step 10 same migration for
  the prompt criteria set.
- **`docs/workflow-guide.md`** — adds `bin/check-plan` to §7's
  per-skill classification table as a cat-1 (substitutable)
  operation.
- **`prompts/issue-072-bin-check-plan-programmatic-surface.md`** —
  committed as commit 0 on the feature branch.

## Commits

```
f7b4652  docs(workflow-guide): list bin/check-plan as cat-1 in §7 (ADR-041, ADR-043, #72)
bb38b77  refactor(skills): migrate adr-writer + prepare-issue chain points to bin/check-plan (ADR-043, #72)
419cd0e  refactor(skills): delegate check-plan slash-command to bin/check-plan (ADR-043, #72)
153b407  feat(bin): add bin/check-plan programmatic surface (ADR-043, #72)
8115691  docs(prompts): add prompt for issue #72 (ADR-043, #72)
```

Branch: `bin-check-plan-programmatic-surface` off `main`. Five commits
total. Each commit message references both the governing ADR (`ADR-043`)
and the issue number (`#72`); commit 5 also references `ADR-041` because
it updates the §7 permission-contract table.

## Verification performed

Markdown + bash kit; no unit-test runner. Verification is end-to-end
smoke tests of the new infrastructure plus read-back checks on spec
migrations. **All 6 checks passed**:

1. **Exit codes**: known-good ADR → 0; known-good prompt → 0; missing
   file → 2; template (with placeholders) → 1 with FAIL records on
   PROMPT-C2 (ADR section unresolved) and PROMPT-C3 (26 placeholders).
2. **JSON validity** (via `python3 -c 'import json; ...'` since `jq`
   isn't installed locally): `{result: pass, criteria-count: 6}` for
   the known-good ADR.
3. **Reserved sets reject cleanly**: `changelog`, `milestone-summary`,
   `pr-body` each return exit 2 with the message *"criteria set X is
   reserved but not yet implemented"*.
4. **Migration check**: `grep -l "bin/check-plan"` finds the token in
   `skills/adr-writer/SKILL.md`, `skills/prepare-issue/SKILL.md`,
   `skills/check-plan/SKILL.md`, and `skills/check-plan/example.md` —
   all 4 expected files.
5. **§7 contract update**: `grep -n "bin/check-plan" docs/workflow-guide.md`
   matches at line 671 inside the cat-1 classification table.
6. **Stdin == file equivalence**: piping the same ADR through stdin
   (`--input -`) produces byte-identical output to passing it as
   `--input <path>`. Single source of truth confirmed.

**ADR equivalence walk-through (manual).** Ran `bin/check-plan
--criteria-set adr --input Design/adr/adr-041-auto-mode-permission-contract.md`
and got 5 PASS + 1 WARN (ADR-C6's deferred semantic-conflict check,
which is documented as not deterministically encodable per ADR-034).
The slash-command surface, when invoked, would now delegate this
exact evaluation to `bin/check-plan` per the rewritten SKILL.md
protocol.

## Bugs fixed during implementation

- **Exit-trap last-command bug.** Initial `cleanup() { [ -n "$TMP" ]
  && [ -f "$TMP" ] && rm -f "$TMP"; }` returned 1 when `TMP_INPUT`
  was empty (the empty-string `[ -n ]` test fails), and bash uses
  the EXIT trap's last-command exit status as the script exit
  status. So the script would print correct PASS/WARN output and
  then exit 1. Fixed by restructuring cleanup as `if-then-fi` plus
  explicit `return 0`.
- **ADR-C5 zero-pad glob bug.** Initial token-resolution glob
  `Design/adr/adr-0*${num}-*.md` was wrong because bash glob's `*`
  isn't anchored — `0*` matches `0` followed by any chars, not
  "zero or more zeros". So `ADR-038` failed to resolve to
  `adr-038-...md`. Fixed by zero-padding the number to 3 digits
  (`printf '%03d'` with base-10 normalisation) and using exact
  glob, with a fallback for other widths.
- **`[ -z ] && continue` and set -e**. Restructured the read-loop
  body to use `if [ -z ]; then continue; fi` — defensive against
  set-e's edge cases inside while-read loops, even though the
  rules technically protect `&&` non-final commands.

These are documented here so a future reader investigating bash
behaviour in this script has the context.

## Follow-ups

- **Three new criteria sets are reserved but not implemented.**
  `changelog`, `milestone-summary`, `pr-body` are rejected at the
  dispatcher with a clear error message. Each becomes a separate
  follow-up issue: implement the eval function, add a section to
  `criteria.md`, wire the chain point into the consuming skill,
  test against real fixtures. Each issue should be motivated by a
  specific quality-gate failure mode rather than authored
  speculatively.
- **The `## Notes for #N` parser deferral** (carry-forward from PR
  #73). Decided in this issue's plan to defer to a separate
  follow-up. The `bin/`-script-invocation precedent set here is
  the actual reusable infrastructure; a parser is a different
  surface shape and deserves its own issue.
- **ADR-040 §6 schema-drift check** is now unblocked. Can land as a
  new criteria set under `bin/check-plan` (or a sibling `bin/`
  script following the same precedent) once someone files an
  issue.
- **ADR-041 §7 permission-contract drift check** — same story.
- **F27 changelog dedup gap (#61)** — when `changelog` criteria
  land, `CHANGELOG-C2` (no duplicate entries) closes part of #61's
  scope. Cross-check at #61 prep time.
- **`bin/check-plan-criteria-drift`** still passes today (it
  checks template-vs-criteria mtime). When new criteria sets are
  added, its allow-list may need updating.
- **`jq` not installed locally.** Verification used `python3 -c
  'import json; ...'` instead. JSON output schema is stable; if
  CI workflows ever run these checks, ensure `jq` (or python) is
  on the path.

No `### design-questions` block emitted. The carry-forward question
this issue inherited (PR-body section grammar / parser) is answered
explicitly in the plan and resolved as *deferred to a separate
issue* — that's a routing decision, not an open design question
affecting an upcoming filed issue. Per ADR-040's *Empty case*, the
block is omitted entirely.

## Commands the user should run

```bash
# Inspect the branch
git log main..HEAD --oneline
git diff main..HEAD --stat

# Run the new programmatic surface against known-good inputs
bin/check-plan --criteria-set adr \
    --input Design/adr/adr-041-auto-mode-permission-contract.md
echo "exit: $?"   # expect 0

bin/check-plan --criteria-set prompt \
    --input prompts/issue-070-auto-mode-permission-contract.md
echo "exit: $?"   # expect 0

# JSON shape (use python if jq is missing)
bin/check-plan --criteria-set adr \
    --input Design/adr/adr-041-*.md --format json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result'], len(d['criteria']))"

# Confirm reserved sets reject cleanly
bin/check-plan --criteria-set changelog --input Design/adr/adr-041-*.md
echo "exit: $?"   # expect 2

# Confirm migration of chain points
grep -n "bin/check-plan" skills/adr-writer/SKILL.md skills/prepare-issue/SKILL.md

# Confirm §7 contract update
grep -n "bin/check-plan" docs/workflow-guide.md

# Read this eval summary back
cat notes/eval-issue-072.md
```

## Next step

`/pr-review-packager` to draft a PR from the
`bin-check-plan-programmatic-surface` branch. The packager (cat-3
per §7) will require explicit `yes` before opening the PR. No
`### design-questions` block in this eval, so no `## Notes for #N`
sections will be emitted.

The branch is not yet pushed; the user should run `git push -u
origin bin-check-plan-programmatic-surface` before invoking the
packager.

## Alignment check

- [x] The plan was proposed and explicitly approved before any edits (plan mode entered, plan written, user approved via ExitPlanMode).
- [x] A feature branch was created from `main` (`bin-check-plan-programmatic-surface`); no commits to `main`.
- [x] Every commit message includes `ADR-043` and `#72`. Commit 5 additionally references `ADR-041` because it updates the §7 permission-contract table.
- [x] Tests are not applicable to this kit (markdown + bash, no unit-test runner). Verification is end-to-end smoke tests of the new infrastructure — documented above.
- [x] An evaluation summary was printed and persisted to `notes/eval-issue-072.md` (per ADR-040).
- [x] The session raised no cross-issue design questions matching §6's when-to-populate rule; the `### design-questions` block was omitted (per ADR-040 *Empty case*). Reasoning recorded in *Follow-ups*.
- [x] `/pr-review-packager` is suggested, not auto-invoked.
- [x] Scope was narrowed mid-session from broad to narrow with an honest re-assessment; the change is documented at the top of this eval and reflected in the dispatcher (reserved-set rejection) and follow-ups list.
- [x] `Design/state.md` step skipped silently (file absent in kit repo, per ADR-035).
