---
name: pr-review-packager
description: Draft a pull-request body from templates/pr-template.md, auto-fill the Closes line and ADR references from branch and commit history, show the draft for approval, then open the PR via gh pr create. Use when packaging a feature branch into a PR after implementation commits land.
permission-category: 3  # non-substitutable — gh pr create is public, hard-to-reverse, per workflow-guide §7
---

# pr-review-packager

Package a feature branch into a well-structured pull request. The skill
reads [`templates/pr-template.md`](../../templates/pr-template.md),
fills in `Closes #N` and ADR references from the branch name and commit
history, derives a change summary from `git log main..HEAD`, shows the
finished body in chat for approval, and only then calls
`gh pr create`.

This skill completes the implementation pipeline:
`/prepare-issue` → `claude-issue-executor` → **`/pr-review-packager`**.
See [ADR-015](../../design/adr/adr-015-pr-review-packager-skill.md) for
the decision record. The skill is also the **preserver** in the
cross-skill design-question carry-forward chain decided in
[ADR-040](../../design/adr/adr-040-cross-skill-design-question-carry-forward.md)
— it reads the executor's `notes/eval-issue-NNN.md` and emits
`## Notes for #N` sections in the PR body so the carry-forward
survives in PR history. See
[`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040)
for the canonical schema.

## When to use this skill

Use when an implementation branch is ready for review and the user
wants to open the PR without hand-filling the template. Typical
invocation:

```
/pr-review-packager
```

Optional pass-through flags are supported and forwarded verbatim to
`gh pr create`:

```
/pr-review-packager --label feature --milestone "MVP" --reviewer @alice
```

The skill is **read-only** with respect to `templates/pr-template.md`
— it consumes the file without editing it.

## What this skill does not do

- Does not edit `templates/pr-template.md`. Ever. It is a read-only
  consumer.
- Does not modify the local branch or rewrite commits. If the commit
  history needs cleaning up, the user does that before invoking the
  skill.
- Does not push the branch. Pushing is the user's responsibility; the
  skill fails cleanly if the upstream branch does not exist yet and
  reports the exact `git push -u origin <branch>` command to run.
- Does not create a draft PR by default. If the user wants one they
  can pass `--draft`.
- Does not review the PR content for correctness (that is `/review`,
  a built-in). It only packages the body.
- Does not run CI, tests, or linters. It only reports what `git log`
  shows.
- Does not open the PR without explicit user approval of the rendered
  body. The approval gate from ADR-015's chosen option (Option B) is
  mandatory.

## Auto-mode permission category

This skill is **category 3** — *non-substitutable* — in the kit-wide
auto-mode permission contract. See
[`docs/workflow-guide.md` §7](../../docs/workflow-guide.md#7-auto-mode-permission-contract-adr-041)
for the canonical contract.

`gh pr create` is public-visibility and hard-to-reverse: a PR opened
in error is visible to collaborators, may trigger CI runs and
notifications, and requires explicit close-or-edit follow-up. This
class of operation is **never** substituted by auto-mode regardless
of mode.

The contract requires: **explicit `yes` from the operator before
`gh pr create` is called, regardless of whether auto-mode is
active**. Steps 12–13 of the execution protocol below already
implement this — the user sees the rendered title and body in chat
and must reply `yes` before the skill calls `gh`. ADR-041 does not
change this behaviour; it codifies the existing convention as a
contract so future maintenance cannot regress it.

If a future change ever proposes silencing the explicit-yes gate
under auto-mode, it must be rejected at PR review as a cat-3
violation. The same rule applies to any other operation the skill
might add that touches public state (e.g. labelling, assigning
reviewers as a side-effect of merge): each must gate behind an
explicit-yes prompt that auto-mode does not satisfy.

## Inputs

- **Required:** none — the skill reads everything it needs from the
  current git worktree, the repo, and `gh`.
- **Optional flags** (passed through to `gh pr create`):
  - `--label <name>` (repeatable)
  - `--milestone <name>`
  - `--reviewer <user-or-team>` (repeatable)
  - `--draft`
  - `--base <branch>` (defaults to `main`)
  - `--assignee <user>` (repeatable)

Flags the skill does **not** forward: anything that would suppress the
body (`--fill`, `--body-file`), anything that would bypass the approval
gate, and anything destructive.

## Output

- A new pull request on GitHub, opened via
  `gh pr create --title "..." --body "..." --base <base> --head <current-branch>`
  plus any pass-through flags.
- A one-line confirmation in chat including the PR URL returned by
  `gh`.

## Data sources and how the skill reads them

The skill consults five sources, in this order:

1. **Current branch and git history.**
   - `git symbolic-ref --short HEAD` → current branch name. A detached
     HEAD aborts the skill (see Edge cases).
   - `git rev-parse --abbrev-ref --symbolic-full-name @{u}` → upstream
     ref, used to confirm the branch has been pushed. If no upstream
     is set, the skill stops with a clear message telling the user to
     run `git push -u origin <branch>` first.
   - `git log <base>..HEAD --format="%H%x09%s"` → commits ahead of
     base, used for the change summary and as a secondary source for
     issue and ADR tokens. `<base>` is `main` unless the user passed
     `--base`.
2. **PR template.** Read `templates/pr-template.md` verbatim. If it is
   missing, abort (see Edge cases).
3. **Issue prompt file** (fallback). Glob `prompts/issue-NNN-*.md` and
   pick the most recently modified file. Useful when the branch name
   does not encode the issue number.
4. **ADR files.** For each `ADR-NNN` token found, glob
   `design/adr/adr-<NNN>-*.md` and resolve the full filename.
5. **Eval-summary file** (optional). Once the issue
   number is resolved (step 6 of the execution protocol), read
   `notes/eval-issue-NNN.md` (zero-padded). Parse the
   `### design-questions` YAML block under `## Follow-ups` if
   present. Group entries by `target-issue`; each unique
   `target-issue` becomes one `## Notes for #M` section in the
   rendered PR body. If the file is absent or has no
   `### design-questions` block, skip silently — most issues have
   no entries. Schema source of truth:
   [`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040).

`gh` is the only allowed tool for creating the PR. Do not call the
REST/GraphQL API directly.

## Execution protocol

Run these steps in order. Stop on the first failure unless otherwise
noted.

1. **Verify working tree.** Run `git status --porcelain`. If it is
   non-empty, warn the user and ask whether to continue — the
   uncommitted changes will not be included in the PR.
2. **Resolve the branch.** Run `git symbolic-ref --short HEAD`. On a
   detached HEAD, abort with:
   `"HEAD is detached. Check out a branch before running /pr-review-packager."`
3. **Confirm base.** The base branch is `main` unless `--base` was
   passed. If the current branch equals the base, abort with:
   `"Current branch is <base>. Check out a feature branch before packaging a PR."`
4. **Confirm the branch has been pushed.** Run
   `git rev-parse --abbrev-ref --symbolic-full-name @{u}`. If it
   errors, abort with:
   `"No upstream for <branch>. Run: git push -u origin <branch>"`.
5. **List commits ahead of base.** Run
   `git log <base>..HEAD --format="%H%x09%s"`. If the output is empty,
   abort with:
   `"No commits on <branch> ahead of <base>. Nothing to package."`
6. **Extract the issue number.** In priority order, use the first hit:
   1. **Branch name.** Match the pattern
      `issue-(\d+)-` or a trailing `-(\d+)$` against the current
      branch name, or an explicit `#(\d+)` token.
   2. **Commit messages.** Scan the commit subjects in
      `git log <base>..HEAD` for `#(\d+)` tokens (typically the
      trailing `(ADR-NNN, #N)` convention this repo uses). Use the
      first unique number seen, most-recent commit first.
   3. **Most recent issue prompt.** Glob `prompts/issue-(\d+)-*.md`,
      pick the file with the newest mtime, and read `NNN` from its
      filename. Strip leading zeros for the PR body.
   If no hit is found, leave `{{ISSUE_NUMBER}}` as
   `<!-- TODO: fill in issue number -->` and flag it during the
   approval gate rather than blocking.
6.5. **Scan for design-questions.** With the issue
    number resolved, read `notes/eval-issue-NNN.md` (zero-padded).
    If the file is absent, skip silently and continue to step 7.
    If present, locate the `### design-questions` heading under
    `## Follow-ups` and parse the fenced YAML block beneath. Each
    entry is a `(title, target-issue, context)` triple. Group
    entries by `target-issue`; preserve in-block order within a
    group. The result is a map from target-issue number to a list
    of entries, used in step 11 to emit `## Notes for #M` sections.
    A malformed YAML block surfaces a one-line warning to the user
    at the approval gate but does not abort the skill — the rest of
    the PR body still renders. The canonical schema and field
    semantics live in
    [`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040).

7. **Extract ADR references.** Scan the same sources (branch name,
   commit subjects, most recent prompt file) for `ADR-(\d+)` tokens
   (case-insensitive). Deduplicate, preserve first-seen order. For
   each unique `NNN`, glob `design/adr/adr-<NNN>-*.md`. If a file
   matches, record the path. If none match, keep the `ADR-NNN` token
   and flag it as a TODO in the approval gate. If no ADR tokens are
   found anywhere, set the `## ADR` body to `none`.
8. **Derive the change summary.** From the commit subjects, group by
   conventional-commit verb prefix: `feat`, `fix`, `docs`, `refactor`,
   `chore`, `test`, `perf`, `ci`, `build`, `infra`, `style`. (`infra`
   is included to match the kit's canonical label set in
   `templates/claude-md-template.md` — `infra(scope):` commits go in
   their own group rather than `other`.) Any commit without a
   recognised prefix goes under a final `other` group. Within each
   group, keep one bullet per commit, preserving commit order
   (oldest-first) and stripping the trailing `(ADR-NNN, #N)` suffix
   for readability. If there is only one group, omit the group
   heading and just list the bullets.
9. **Derive the PR title.** Use the newest commit subject on the
   branch, stripped of the trailing `(ADR-NNN, #N)` suffix. If the
   title still ends with something like `(#NN)`, strip that too. The
   user can override during approval.
10. **Draft the Summary paragraph.** One sentence: take the verb and
    object from the PR title, plus the issue number if known. Example:
    `"Adds the pr-review-packager skill that packages feature
    branches into well-structured PRs (closes #17)."` This is a
    best-effort draft — the user will edit if needed.
11. **Fill the template.** Read `templates/pr-template.md` and
    substitute each placeholder:

    | Placeholder | Filled with |
    |---|---|
    | `{{One-paragraph description of what this PR changes and why.}}` | the Summary draft from step 10 |
    | `{{ISSUE_NUMBER}}` | issue number from step 6 (no `#`) |
    | `` `design/adr/adr-{{NNN}}-{{short-title}}.md` `` line | one resolved ADR path per line, each as `Related ADR: design/adr/adr-NNN-short-title.md`. If no ADRs, the whole line becomes `Related ADR: none`. |
    | `{{Bullet the substantive changes, not every file touched.}}` block | the grouped bullets from step 8 |
    | `{{Paste test-runner output: total / passed / failed / skipped.}}` | left as a placeholder `<!-- TODO: paste test-runner output or delete the code fence and write "no code changes — docs only" -->` |
    | `{{Steps a reviewer should run to convince themselves the change works.}}` | `<!-- TODO: list verification steps, or write "none needed" -->` |

    **After the rendered template body, append `## Notes for #M`
    sections (per ADR-040)**, one per unique `target-issue` from
    step 6.5, in ascending issue-number order. Each section has the
    form:

    ```markdown
    ## Notes for #<M>

    Carried forward from this issue's eval summary
    (`notes/eval-issue-NNN.md`). The next executor session for #<M>
    should address these in its plan.

    - **<title 1>**: <context paragraph 1>
    - **<title 2>**: <context paragraph 2>
    ```

    If step 6.5 produced no entries, no `## Notes for #M` sections
    are emitted (skip silently — most PRs have none). The section
    title format `## Notes for #<M>` is the kit-canonical anchor
    that `prepare-issue` later scans for; do not vary it.

    Strip the template's HTML comments that instruct the author (they
    are not part of the rendered body the skill produces).

12. **Show the filled body to the user** as a fenced markdown block
    plus the derived title on a line above it. Flag any TODO markers
    and any unresolved tokens (e.g. ADR file missing, no issue
    number). Ask explicitly:
    `"Open PR with this title and body? (yes / edit / cancel)"`.
    **Do not call `gh pr create` before this confirmation.**
13. **Handle the response.**
    - `yes` → proceed to step 14.
    - `edit` → ask the user what to change, apply it, re-render, re-ask.
      Loop until `yes` or `cancel`.
    - `cancel` → stop without calling `gh`.
14. **Open the PR.** Call:
    ```
    gh pr create \
      --title "<title>" \
      --body  "<body>" \
      --base  "<base>" \
      --head  "<current-branch>" \
      [pass-through flags]
    ```
    Pass-through flags are the `--label`, `--milestone`, `--reviewer`,
    `--assignee`, `--draft` values the user provided at invocation.
15. **Update `design/state.md` if present.** Per
    [ADR-035](../../design/adr/adr-035-state-md-session-continuity.md),
    close out the issue in the state file:
    - prepend a one-line entry to the `state:recent` zone of the
      form `#<PR> — ADR-NNN — <commit-summary first sentence>`
      (use `none` for the ADR token if no ADR was resolved). If the
      zone now has more than five entries, drop the oldest so the
      rolling list stays at five.
    - rewrite the `state:in-flight` zone to `Issue: none`,
      `Prompt: n/a`, `Branch: n/a`, `Status: none`.
    - rewrite the `state:continue-here` zone to one short paragraph
      pointing at the just-opened PR, e.g. `"Review and merge #<PR>;
      then pick the next issue from the queue."`.
    Marker fences bound each zone; rewrite only the bytes between
    the fences. If `design/state.md` is absent, skip silently. If
    marker fences are broken, do not rewrite; surface the broken
    zone in the final report and suggest `/pause`.
16. **Report.** Print the PR URL returned by `gh`, plus a one-line
    summary of what was filled vs. what was left as TODO. Done.

## Reference: extraction rules, edge cases, self-check

Detailed rules and tables live in [`reference.md`](reference.md):

- **Issue-link extraction** — branch-name → commit-subject → prompt-file priority order; leading-zero strip rule.
- **ADR-link extraction** — token regex, glob resolution, multi-ADR handling.
- **Change-summary derivation** — conventional-commit prefix grouping; group ordering with `infra` adjacent to `build`.
- **Edge cases** — detached HEAD, no upstream, missing template, multiple issues, existing PR.
- **Self-check before calling `gh`** — ADR-023 index sync and ADR-040 Notes-for-#M emission gates.
- **Relationship to other skills** — `/review`, `claude-issue-executor`, `/changelog`, `/release`.

## Review-before-create checkpoint

The user always sees the rendered title and body in chat before
`gh pr create` is called. This preserves the approval gate from
ADR-015's chosen option. Never skip this step — not even when the
draft looks clean, not even with a `--yes` flag (the skill does not
accept one).

## Handoff

The PR is the handoff. Once opened, the review and merge are
human-driven (or handled by `/review`). This skill is done when
`gh pr create` returns a URL and the URL is reported to the user.

See [`example.md`](example.md) for a worked invocation on this very
issue.
