# pr-review-packager — operator reference

Rationale and background for the `pr-review-packager` skill. The agent
operates from `skills/pr-review-packager/SKILL.md` and its co-installed
companions (`reference.md`, `example.md`); it never reads this file.
Anything needed to produce a correct result stays in the body or those
companions — this file is for the human operator.

## Why this skill exists

It completes the implementation pipeline `/prepare-issue` →
`claude-issue-executor` → **`/pr-review-packager`**, per
[ADR-015](../../design/adr/adr-015-pr-review-packager-skill.md). It is also
the **preserver** in the cross-skill design-question carry-forward chain
([ADR-040](../../design/adr/adr-040-cross-skill-design-question-carry-forward.md)):
it reads the executor's `notes/eval-issue-NNN.md` and emits `## Notes for #N`
sections in the PR body so the carry-forward survives in PR history. Canonical
schema:
[`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040),
mirrored in
[`schemas/design-questions.v1.yaml`](../../schemas/design-questions.v1.yaml).

## What this skill does not do

- Does not edit `templates/pr-template.md` — a read-only consumer.
- Does not modify the local branch or rewrite commits. Clean up history
  before invoking.
- Does not push the branch. It fails cleanly if the upstream branch does not
  exist and reports the exact `git push -u origin <branch>`.
- Does not create a draft PR by default (`--draft` if you want one).
- Does not review PR content for correctness (that is `/review`).
- Does not run CI, tests, or linters — it reports only what `git log` shows.
- Does not open the PR without explicit approval of the rendered body.

## Auto-mode permission category (why cat-3)

This is a **category-3, non-substitutable** skill in the kit-wide auto-mode
permission contract
([`docs/workflow-guide.md` §7](../../docs/workflow-guide.md#7-auto-mode-permission-contract-adr-041)).
`gh pr create` is public-visibility and hard-to-reverse: a PR opened in error
is visible to collaborators, may trigger CI and notifications, and needs
explicit close-or-edit follow-up. So the contract requires an **explicit
`yes` from the operator before `gh pr create`, regardless of whether
auto-mode is active** — the body's approval gate implements this. A future
change that silences the gate under auto-mode must be rejected at review as a
cat-3 violation; any new public-state operation the skill adds (labelling,
assigning reviewers as a merge side-effect) must gate the same way. `gh` is
the only allowed tool for creating the PR — never call the REST/GraphQL API
directly.

## Data sources (what `bin/pr-context` reads)

The body delegates deterministic extraction to `bin/pr-context`. For
reference, the five sources it reads, in priority order, are:

1. **Current branch and git history** — `git symbolic-ref --short HEAD` (the
   branch; detached HEAD aborts);
   `git rev-parse --abbrev-ref --symbolic-full-name @{u}` (upstream, to
   confirm the branch is pushed);
   `git log <base>..HEAD --format="%H%x09%s"` (commits ahead, for the change
   summary and as a secondary token source).
2. **PR template** — `templates/pr-template.md`, read verbatim (missing →
   abort).
3. **Issue prompt file** (fallback) — newest `prompts/issue-NNN-*.md`, when
   the branch name does not encode the issue number.
4. **ADR files** — for each `ADR-NNN` token, `design/adr/adr-<NNN>-*.md`.
5. **Eval-summary file** (optional) — `notes/eval-issue-NNN.md`; parse the
   `### design-questions` block under `## Follow-ups`, group by
   `target-issue`; each group becomes one `## Notes for #M` section. Absent /
   no block → skip silently.

The detailed extraction rules (issue-link priority and leading-zero strip,
ADR token regex and multi-ADR handling, change-summary grouping with `infra`
adjacent to `build`), the full edge-case list (detached HEAD, no upstream,
missing template, multiple issues, existing PR), the self-check gates, and
the relationship to other skills (`/review`, `claude-issue-executor`,
`/changelog`, `/release`) live in the co-installed
[`reference.md`](../../skills/pr-review-packager/reference.md).

## `design/state.md` close-out — exact zone bodies (ADR-035, ADR-048)

Rewrite each zone with
`bin/fence replace --file design/state.md --dialect state --zone <zone> --body-file <tmp>`:

- `recent`: prepend `#<PR> — ADR-NNN — <commit-summary first sentence>` (use
  `none` for the ADR token if none resolved); if the zone now exceeds five
  entries, drop the oldest so the rolling list stays at five.
- `in-flight`: `Issue: none`, `Prompt: n/a`, `Branch: n/a`, `Status: none`.
- `continue-here`: one short paragraph pointing at the opened PR, e.g.
  "Review and merge #<PR>; then pick the next issue from the queue."
- `next-action` (ADR-048): `skill: none`, `args: n/a`, `preconditions: []`,
  `blocked-by: "PR #<PR> awaiting review/merge"` — the next action is human
  review, not a skill. Skip this zone if the file predates it.

If `design/state.md` is absent, skip silently. A broken fence makes
`bin/fence` exit 1 instead of writing; surface the broken zone in the final
report and suggest `/pause`.

## Worked example

See [`../../skills/pr-review-packager/example.md`](../../skills/pr-review-packager/example.md)
for a worked invocation.
