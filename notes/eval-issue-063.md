# Evaluation summary — Issue #63 (no ADR)

## What changed

- **`skills/pr-review-packager/SKILL.md`** — added `infra` to four
  spots so kit-shape commits with `infra(scope):` prefix categorize
  under their own group rather than landing in `other`:
  - the conventional-commit regex (line 364, § *Change-summary
    derivation* step 1)
  - the group-output order (line 374, § *Change-summary derivation*
    step 3)
  - the prose verb listing in § *Execution protocol* step 8 (line
    216)
  - the example subheading list in § step 5 (line 380, adds
    `**Infra**` to the example list)
- **`prompts/issue-063-add-infra-verb-to-pr-review-packager.md`** —
  committed as commit 0 on the feature branch.

Each spec-text site carries a brief inline note explaining the
kit-label-set alignment with `templates/claude-md-template.md` —
the rationale travels with the code so future edits don't strip
`infra` thinking it's a stray.

## Commits

```
5408600  fix(skills): add infra verb to pr-review-packager classifier (#63)
7e5a54a  docs(prompts): add prompt for issue #63 (#63)
```

Branch: `add-infra-verb-to-pr-review-packager` off `main`. Two
implementation commits + this eval. No ADR token in commit messages
because the issue is a spec-consistency bug fix with no governing
ADR — `(#63)` only, per the prompt's explicit instruction.

## Verification performed

Markdown-only kit, no test runner. Verification is read-back checks
plus a manual walk-through against three synthetic commit subjects
(mirroring the prompt's *Evaluation & testing* section).

**Read-back checks (all pass):**

```
1. grep -n "infra" skills/pr-review-packager/SKILL.md
   → 5 matches: lines 216, 218, 364, 367, 374
   (3 edit sites × 1–2 lines each due to inline rationale prose)
2. grep -n "Infra" skills/pr-review-packager/SKILL.md
   → 1 match: line 380 (subheading example list updated)
3. grep -n "infra" templates/claude-md-template.md
   → 1 match: line 161 (canonical label set still includes infra)
```

**Walk-through verification (manual)** — apply the post-fix
change-summary derivation rules to three synthetic commit subjects:

| Commit subject | Regex match | Prefix → group | Bullet text | Result |
|---|---|---|---|---|
| `infra(papers): add smoke-test example` | yes | `infra` → **Infra** | `add smoke-test example` | ✅ new behaviour |
| `feat(skills): add foo (#10)` | yes | `feat` → **Features** | `add foo` (suffix stripped) | ✅ regression check |
| `something-weird: blah` | no | (none) → **Other** | `something-weird: blah` | ✅ regression check |

All three placements match the documented rules. Step-2 trailing-
suffix stripping applies uniformly across new and old groups.

## Follow-ups

- **`bin/check-plan` PROMPT-C2 / PROMPT-C6 bug surfaced via
  dogfooding.** During this issue's `prepare-issue` step, the eval
  lib (`bin/lib/check-plan-eval.sh`, shipped on #72) flagged
  PROMPT-C2 fail when the prompt used the canonical single-line
  `ADR: none — <reason>` form documented in
  `prompts/_template.md`. The eval lib only recognises the multi-
  line `- File: none — <reason>` shape inside an `ADR:` block; the
  single-line form fails both PROMPT-C2 (because the regex doesn't
  match) and would fail PROMPT-C6 (because the `ADR:` heading line
  goes missing when the section is replaced wholesale per the
  template's HTML-comment guidance). Worked around in this issue's
  prompt by using the multi-line `- File: none — <reason>` shape.
  Should be filed as a follow-up bug-fix issue against
  `bin/lib/check-plan-eval.sh`. The fix is small (relax the
  PROMPT-C6 section-presence check to accept either `ADR:` exact
  line OR `ADR: <anything starting with non-blank>`, and add a
  fourth case to PROMPT-C2's regex matching the single-line form),
  but it is a real spec-vs-runtime gap in the new kit script. The
  v3.3.0 baseline eval's same class of finding.
- **No `### design-questions` block.** This issue is a narrow
  spec-consistency fix; no upcoming filed-or-planned issue
  depends on its outcome. #61 (changelog parser) is a different
  fix on a different surface — no shared constraint. Per ADR-040
  *Empty case*, the block is omitted.

## Commands the user should run

```bash
# Inspect the branch
git log main..HEAD --oneline
git diff main..HEAD --stat

# Confirm the four edit sites
grep -n "infra" skills/pr-review-packager/SKILL.md
grep -n "Infra" skills/pr-review-packager/SKILL.md

# Regression: kit's CLAUDE.md template still advertises infra
grep -n "infra" templates/claude-md-template.md

# Manually apply the change-summary rules — confirm the three
# synthetic commit subjects produce Infra / Features / Other
sed -n '/^## Change-summary derivation/,/^## /p' \
    skills/pr-review-packager/SKILL.md | head -30

# Read this eval summary back
cat notes/eval-issue-063.md
```

## Next step

`/pr-review-packager` to draft a PR from the
`add-infra-verb-to-pr-review-packager` branch. The packager (cat-3
per workflow-guide §7) will require explicit `yes` before opening
the PR. No `### design-questions` block in this eval, so no
`## Notes for #M` sections will be emitted.

The branch is not yet pushed; the user should run `git push -u
origin add-infra-verb-to-pr-review-packager` before invoking the
packager.

## Alignment check

- [x] The plan was proposed and explicitly approved before any edits (plan mode entered, plan file written, user approved via ExitPlanMode).
- [x] A feature branch was created from `main` (`add-infra-verb-to-pr-review-packager`); no commits to `main`.
- [x] Every commit message includes `#63`. ADR token is intentionally absent because this issue has no governing ADR; the prompt explicitly instructed `(#63)` only.
- [x] Tests are not applicable to this kit (markdown + bash, no unit-test runner). Verification is read-back checks and a walk-through, documented above.
- [x] An evaluation summary was printed and persisted to `notes/eval-issue-063.md` (per ADR-040).
- [x] The session raised no cross-issue design questions matching §6's when-to-populate rule; the `### design-questions` block was omitted (per ADR-040 *Empty case*). Reasoning recorded in *Follow-ups*.
- [x] `/pr-review-packager` is suggested, not auto-invoked.
- [x] `Design/state.md` step skipped silently (file absent in kit repo, per ADR-035).
