---
name: pr-review-packager
description: Draft a pull-request body from templates/pr-template.md, auto-fill the Closes line and ADR references from branch and commit history, show the draft for approval, then open the PR via gh pr create. Use when packaging a feature branch into a PR after implementation commits land.
permission-category: 3  # non-substitutable — gh pr create is public, hard-to-reverse, per workflow-guide §7
inputs:
  - name: "--label / --milestone / --reviewer"
    required: false
    description: "Pass-through flags to gh pr create"
  - name: "--draft"
    required: false
    description: "Open the PR as a draft"
  - name: "--base"
    required: false
    description: "Override the base branch (default main)"
outputs:
  - artefact: "(GitHub PR)"
    description: "PR opened via gh pr create"
  - artefact: "design/state.md"
    description: "Updated (in-flight cleared, recent prepended)"
next: []
---

# pr-review-packager

Package a feature branch into a pull request: read
[`templates/pr-template.md`](../../templates/pr-template.md), fill `Closes #N`
and ADR references from branch/commit history, derive a change summary
from `git log <base>..HEAD`, show the body for **approval**, then call
`gh pr create`. Completes the pipeline `/prepare-issue` →
`claude-issue-executor` → **`/pr-review-packager`**, and **preserves** the
ADR-040 design-question carry-forward as `## Notes for #N` sections in the PR
body.

Operator reference (rationale, permission detail, data-source/`state.md`
specifics): [`docs/skills/pr-review-packager.md`](../../docs/skills/pr-review-packager.md).
Co-installed companions read as needed: [`reference.md`](reference.md)
(extraction rules, edge cases, self-check), [`example.md`](example.md).

## When to use

When an implementation branch is ready and the user wants the PR opened
without hand-filling the template. Invoke `/pr-review-packager` (no args).
Optional flags forwarded to `gh pr create`:
`--label`/`--reviewer`/`--assignee` (repeatable), `--milestone`, `--draft`,
`--base <branch>` (default `main`). Never forward flags that suppress the body
(`--fill`, `--body-file`), bypass the gate, or are destructive. Read-only
w.r.t. `templates/pr-template.md`; does not push, rewrite commits, or run CI.

## Output

A new PR via
`gh pr create --title "..." --body "..." --base <base> --head <branch>` plus
pass-through flags, and a one-line chat confirmation with the PR URL.

Deterministic extraction is delegated to `bin/pr-context` (step 6). `gh` is
the only tool allowed to create the PR — never call the REST/GraphQL API
directly.

## Execution protocol

Run in order; stop on the first failure unless noted.

1. **Working tree.** `git status --porcelain`; if non-empty, warn that
   uncommitted changes won't be in the PR and ask whether to continue.
2. **Branch.** `git symbolic-ref --short HEAD`; a detached HEAD aborts.
3. **Base.** `main` unless `--base`; if the current branch equals the base,
   abort ("check out a feature branch first").
4. **Pushed.** `git rev-parse --abbrev-ref --symbolic-full-name @{u}`; on
   error, abort ("no upstream — run `git push -u origin <branch>`").
5. **Commits ahead.** `git log <base>..HEAD --format="%H%x09%s"`; if empty,
   abort.
6. **Context.** Run `bin/pr-context --base <base> --format json`; read
   `outputs`:
   - `issueNumber`/`issueSource` (branch → commit subjects → newest prompt →
     `none`). If `none`, leave `{{ISSUE_NUMBER}}` as a `<!-- TODO -->` and
     flag at approval (don't block).
   - `carryForward[]` — groups `{targetIssue, entries:[{title, context}]}`
     (ascending), each → one `## Notes for #M` section (empty → none; a
     `warnings` malformed-block note is surfaced at approval).
   - `adrs[]` — `{token, path, resolved}` deduped; resolved `path` → a
     `Related ADR:` line, unresolved → TODO, empty → `## ADR` = `none`.
   - `commitGroups[]` — `{verb, bullets[]}` oldest-first, `(ADR-NNN, #N)`
     stripped; one bullet per entry, a single group omits its heading.
   - `prTitle` — newest subject, trailing `(…)` stripped; user may override.
7. **Summary paragraph.** One sentence from the PR title's verb+object plus
   the issue number if known (e.g. "Adds … (closes #17)"); best-effort,
   editable.
8. **Fill `templates/pr-template.md`**: description placeholder → the
   Summary; `{{ISSUE_NUMBER}}` → the issue number (no `#`); the
   `design/adr/adr-{{NNN}}-…` line → one `Related ADR: <path>` per resolved
   ADR (or `Related ADR: none`); the changes-bullets block → the grouped
   bullets; test-results and manual-verification placeholders →
   `<!-- TODO … -->`. Strip the template's author-instruction comments.
   **Then append**, ascending, one section per carry-forward group:

   ```markdown
   ## Notes for #<M>

   Carried forward from `notes/eval-issue-NNN.md`; the next executor session
   for #<M> should address these in its plan.

   - **<title>**: <context>
   ```

   The anchor `## Notes for #<M>` is what `prepare-issue` scans for — do not
   vary it. No groups → none.
9. **Approval gate.** Show the derived title (own line) and filled body
   (fenced), flag every TODO/unresolved token, and ask "Open PR with this
   title and body? (yes / edit / cancel)". **Do not call `gh pr create`
   before an explicit `yes`.** `edit` → apply, re-render, re-ask; `cancel` →
   stop.
10. **Open the PR:**
    `gh pr create --title "<title>" --body "<body>" --base "<base>" --head "<branch>"`
    plus pass-through flags.
11. **Update `design/state.md`** if present (ADR-035/048): with `bin/fence
    replace`, prepend `#<PR> — ADR-NNN — <summary>` to `recent` (trim to
    five), clear `in-flight`, point `continue-here` at the PR, and set
    `next-action` to `skill: none, blocked-by: "PR #<PR> awaiting
    review/merge"`. Absent → skip; broken fence (`bin/fence` exit 1) → report
    and suggest `/pause`. Exact zone bodies: reference.
12. **Report** the PR URL from `gh`, plus a one-line summary of what was
    filled vs. left as TODO.

## Approval gate is mandatory

Never skip the step-9 gate — not when the draft looks clean, not via a
`--yes` flag (the skill accepts none); auto-mode does not satisfy this cat-3
explicit-yes gate (ADR-015).

## Receipts

Cat-3 mutating skill: idempotency receipt keyed by the **issue (or PR)
number** ([`docs/receipts.md`](../../docs/receipts.md)). **Before** creating
the PR, check for one
(`bin/write-receipt --find --skill pr-review-packager --key <issue>`); a
`completed` receipt naming an open PR → surface it instead of duplicating.
**On completion**, write a `completed` receipt with the PR number in
`outputs`. Best-effort, gitignored, never blocks handoff.

## Handoff

The PR is the handoff: the skill is done once `gh pr create` returns a URL
and it is reported. Review/merge are human-driven (or `/review`).
