---
name: release
description: Tag a semver release, generate release notes via /changelog, and publish a GitHub Release
permission-category: 3  # non-substitutable — git tag, git push, gh release create — maximum public visibility, per workflow-guide §7
---

# release

Orchestrate the release ceremony for a project: pick the next semver,
generate release notes via the `/changelog` skill, create an annotated
git tag, push it, and publish a GitHub Release. Every mutating step is
gated behind a single explicit approval.

This skill implements [ADR-017](../../Design/adr/adr-017-release-skill.md).

## When to use this skill

- When `main` is at a state worth cutting a release from, and the user
  wants a tagged, published GitHub Release.
- After a feature or fix has been merged and the user wants to ship it.
- As the terminal step in the delivery chain: issue → PR → merge →
  `/release`.

Do not use this skill to draft changelog content in isolation — that is
`/changelog`. `/release` is the orchestration around it.

## What this skill does not do

- Does not generate changelog content itself. It invokes `/changelog`.
  If `/changelog` is not installed, the skill aborts with a pointer to
  install it (see ADR-016, Issue #18).
- Does not modify existing tags. Never force-pushes tags.
- Does not create releases without explicit user approval.
- Does not merge branches, push commits, or alter `main`. It only tags.
- Does not decide semver unilaterally; it proposes and the user
  confirms.

## Invocation

```
/release [--version=X.Y.Z]
         [--bump=major|minor|patch]
         [--branch=main]
         [--draft]
         [--prerelease]
         [--dry-run]
         [--milestone-phase=N]
```

Flags:

- `--version=X.Y.Z` — explicit target version. Overrides any bump
  suggestion. Must be valid semver without the `v` prefix; the tag
  itself is `vX.Y.Z`.
- `--bump=major|minor|patch` — bump level. Applied to the last
  detected tag. If there is no prior tag and `--version` is not given,
  the first release defaults to `0.1.0` (minor bump treated as the
  seed release).
- `--branch=main` — release branch. Defaults to `main`. Configurable
  for projects on a non-default primary branch.
- `--draft` — create the GitHub Release as a draft (passes
  `--draft` to `gh release create`).
- `--prerelease` — mark the GitHub Release as a prerelease
  (passes `--prerelease` to `gh release create`).
- `--dry-run` — walk through every step up to the approval gate and
  stop. Render the preview, print each command that would run, make
  no mutations.
- `--milestone-phase=N` — optional. If set, after a successful release
  the skill updates the matching phase row in
  `Design/build-out-plan.md` from `in-progress` (or `planned`) to
  `released <tag>`. Kept minimal; if the file or phase row is not
  found, the skill reports and continues.

If neither `--version` nor `--bump` is supplied, the skill computes a
**suggestion** (see below) and presents it for confirmation.

## Default release boundary (per ADR-032)

The default release unit is **one phase**. When
`Design/build-out-plan.md` has multiple `### Phase N: <name>` blocks
and `--milestone-phase` was not passed explicitly, infer the target
phase from:

1. The set of GitHub milestones closed since the previous tag — if
   exactly one phase milestone is newly closed, that phase is the
   release boundary.
2. The set of merged PRs in the range — group by their milestone; if
   they all belong to one phase milestone, use it.
3. Otherwise, prompt the user once for the phase number (or `none`
   to release as a multi-phase bundle).

Confirm the inferred phase explicitly in the plan output. Single-phase
projects (one Phase block, or no Phase headings) skip this inference
entirely and behave as before — one release covers the whole project.

To group multiple phases into one release (e.g. v1.0.0 covers Phases
1, 2, and 3), pass `--milestone-phase=` blank or accept the
"multi-phase bundle" option at the prompt. The build-out-plan rows
for every phase in the bundle are updated to `released <tag>`.

## Suggested-version heuristic

When no version is supplied, propose a bump by inspecting everything
since the last tag (or since the first commit, if no tag exists):

1. **major** if any of the following are true:
   - A commit message or PR body contains `BREAKING CHANGE` / the PR
     carries a `breaking` label.
   - A previously `accepted` ADR has been `superseded` in this range
     (detect by scanning `Design/adr/*.md` diffs: a status change from
     `accepted` to `superseded` or the addition of a `Supersedes:`
     field in a new ADR).
2. **minor** if:
   - One or more new ADRs have been added in the range (new file in
     `Design/adr/`), or
   - Any commit begins with `feat(` or uses the `add` verb on a
     user-facing area.
3. **patch** otherwise (only `fix`, `docs`, `chore`, `refactor`
     commits).

The heuristic is conservative: it proposes, the user confirms or
overrides. When multiple signals conflict, pick the highest tier
(major > minor > patch) and explain why in the plan.

## Prerequisites check

Before anything else, verify:

- `gh` is installed and authenticated (`gh auth status`).
- `git` working tree is clean (`git status --porcelain` is empty).
- Current branch equals `--branch` (default `main`).
- Local branch is in sync with `origin/<branch>` — run
  `git fetch origin <branch>` then compare `HEAD` to
  `origin/<branch>`. Refuse if ahead, behind, or diverged.
- `/changelog` skill is available at `.claude/skills/changelog/` (or
  `skills/changelog/` when running in the kit repo). Abort if missing
  with: *"/release requires the /changelog skill. Install it first
  (ADR-016, Issue #18)."*
- **ADR index is in sync.** If `Design/adr/` exists, run
  `bin/sync-adr-index --check` (or `.claude/bin/sync-adr-index --check`
  in target projects). Refuse if it reports drift (exit 1) — the
  release should not capture a stale index. The user must run
  `bin/sync-adr-index`, commit the update, and retry. (ADR-023.)

If any check fails, stop and report the specific failure. Do not
attempt to fix the environment.

## Project-shape detection

Per [ADR-042](../../Design/adr/adr-042-project-shape-detection-in-release.md).
After Prerequisites check passes, scan the project for non-product
indicators and classify the release as either *product-shape* (the
default) or *workflow-shape*. The classification gates the framing of
the release-body content.

The kit applies to any structured project — software or otherwise (per
[ADR-028](../../Design/adr/adr-028-workflow-agnostic-framing.md)). On
non-product projects (research projects, books, curricula, content
projects, design system docs, internal-policy documents), defaulting
to product-shape framing — *"first tagged release of …"*, semver-shaped
language, software-flavoured copy — actively misleads users. This
detection step is the structural enforcement point that matches the
release surface to the project's actual shape.

### Detection signals

`/release` scans for the following four indicators, in any order. Each
satisfied signal contributes to the threshold count.

1. **PRD language signal.** `Design/prd.md` or
   `Design/prd-normalized.md` contains any of *"not [shipping|building]
   a product"*, *"workflow"*, *"folder of markdown"*, or equivalent
   language in the project's problem statement or success criteria.
   Match is substring, case-insensitive, scanned over the whole PRD
   body.
2. **Build-strategy signal.** `Design/build-out-plan.md` "Build
   strategy" section (or equivalent heading) contains *"There is no
   compile / build / deploy step"* or equivalent. Match is substring,
   case-insensitive.
3. **Success-criteria-shape signal.** The PRD's "Success criteria"
   section (or equivalent) contains user-outcome strings (e.g.
   *"a researcher can …"*, *"a reader can …"*) rather than test-result
   strings (e.g. *"all tests pass"*, *"100% coverage"*). Heuristic: at
   least one bullet matches `^(a|an) [a-z]+ can `, or the section
   contains zero `test` / `pass` / `coverage` / `build` mentions.
4. **Package-manifest signal.** Repo root has *none* of:
   `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`,
   `requirements.txt`, `setup.py`, `Pipfile`, `mix.exs`, `pom.xml`, or
   `build.gradle`. Match is filesystem presence, case-sensitive.

This signal list is the **single source of truth** for project-shape
detection. Cross-references elsewhere (e.g. `docs/workflow-guide.md`
§2.i) point back here rather than maintaining a parallel list. New
signals are added here as the kit's PRD and build-out templates
evolve; changes go through the normal ADR-amendment path if material.

### Threshold

**Two or more satisfied signals** trigger the workflow-shape path.
Single-signal cases stay on the product-shape path; the threshold is
deliberately conservative to avoid false-positives on borderline
projects (e.g. a software project whose PRD happens to use the word
"workflow" in passing).

### Outcome

After scanning, `/release` records one of two values:

- `shape = product` — the default; standard product-release framing
  applies (this is the existing behaviour, unchanged).
- `shape = workflow` — when ≥2 signals fire; the release surface
  classifies the project as non-product, and subsequent release-body
  framing uses this value.

The `shape` value is presented to the user in the release plan, so
the classification is visible before the approval gate.

If `Design/prd.md` / `Design/prd-normalized.md` / `Design/build-out-plan.md`
are missing (e.g. on a fresh project that hasn't run `/idea-to-prd`
or `/prd-to-mvp` yet), those signals score zero — they neither fire
nor block. Only the package-manifest signal can fire on a project
without PRD/build-out artefacts; one signal is below threshold, so
such projects default to product-shape.

## Preceding-tag detection

Detect the last tag with:

```
git describe --tags --abbrev=0
```

- If this succeeds, use the result as the `--since` reference for
  `/changelog` and as the base version for `--bump`.
- If it fails (exit non-zero, "No names found"), treat this as the
  **first release**. Default suggestion is `0.1.0`. Pass the repo's
  initial commit as the range start to `/changelog`:
  `git rev-list --max-parents=0 HEAD | tail -1`.

## Release flow

Everything below happens in one conversational turn before any
mutation. The user sees the full plan and types `yes` exactly once to
execute every step.

1. **Run prerequisites check.** Stop on any failure.
2. **Detect the last tag.** Record it (or note "first release").
3. **Determine the target version.**
   - If `--version` is set, use it.
   - Else if `--bump` is set, apply it to the last tag.
   - Else compute the suggested bump and present it for confirmation.
4. **Refuse if `vX.Y.Z` already exists** as a local or remote tag
   (`git tag -l vX.Y.Z` or `git ls-remote --tags origin vX.Y.Z`).
   Suggest the next patch and exit; do not prompt for overwrite.
5. **Invoke `/changelog` for release notes:**
   ```
   /changelog --since-last-release --output=- --github-release=vX.Y.Z
   ```
   Capture the markdown from stdout. If `/changelog` reports no
   commits since the last tag, stop cleanly with "No changes since
   `<last-tag>`. Nothing to release." and do not create a tag.
6. **Assemble the release plan and render it for review:**
   - Target version and tag (`vX.Y.Z`).
   - Last tag (or "first release").
   - Suggested-bump rationale, if applicable.
   - Release-notes preview (the `/changelog` output verbatim).
   - Annotated tag message:
     ```
     Release X.Y.Z

     <first non-heading line from release notes>
     ```
   - GitHub Release config: draft? prerelease? title = `vX.Y.Z`.
   - The exact commands that will run, in order.
7. **Approval gate.** Ask: *"Type `yes` to create and push the tag
   and publish the release. Any other response cancels."* Accept only
   the literal string `yes` (case-insensitive, trimmed). Any other
   input — including `y`, `ok`, `sure` — cancels.
8. **On `yes`, execute in order** (see [Execution sequence](#execution-sequence)).
9. **On any other input, cancel** and report "Release cancelled. No
   changes made."

## Execution sequence

After approval (skip in `--dry-run`):

```bash
# 1. Write release notes to a temp file so `gh` and the tag share text.
NOTES=$(mktemp -t release-notes)
/changelog --since-last-release --output="$NOTES" --github-release=vX.Y.Z

# 2. Annotated tag. First line of notes becomes the tag summary.
SUMMARY=$(head -n 1 "$NOTES")
git tag -a vX.Y.Z -m "Release X.Y.Z

$SUMMARY"

# 3. Push the tag only (never the branch).
git push origin vX.Y.Z

# 4. Publish the GitHub Release.
gh release create vX.Y.Z \
    --title "vX.Y.Z" \
    --notes-file "$NOTES" \
    [--draft] [--prerelease]

# 5. Upload bootstrap-workflow-kit as a release asset (per ADR-029).
# Only if bin/bootstrap-workflow-kit exists in the repo.
if [ -f bin/bootstrap-workflow-kit ]; then
  gh release upload vX.Y.Z bin/bootstrap-workflow-kit
fi

# 6. Optional: update build-out plan phase status.
# Only if --milestone-phase=N was passed and Design/build-out-plan.md exists.
```

Then:

- Report the release URL from `gh release view vX.Y.Z --json url -q .url`.
- Clean up the temp notes file.
- Remind the user nothing else was pushed; `main` is untouched.

## Dry-run mode

With `--dry-run`:

- Run steps 1–6 of the release flow.
- Present the plan as normal.
- Instead of the approval prompt, print:
  *"Dry-run. Would execute:"* followed by the full command sequence
  with resolved values (actual version, resolved tag name, resolved
  notes file path placeholder).
- Make zero mutations. Do not create the temp file, do not invoke
  `git tag`, `git push`, or `gh release create`.

## Edge cases

| Situation | Behaviour |
|---|---|
| No prior tag | Treat as first release. Suggest `0.1.0`. Range for `/changelog` starts at the repo's initial commit. |
| Tag `vX.Y.Z` already exists (local or remote) | Refuse. Suggest the next patch (`vX.Y.(Z+1)`). Never overwrite. |
| Dirty working tree | Refuse. Report `git status --porcelain` output. Tell the user to commit or stash. |
| Wrong branch | Refuse. Report current branch vs. expected. Suggest `git switch <branch>`. |
| Branch out of sync with origin | Refuse. Report ahead/behind counts. Suggest `git pull --ff-only` or `git push`. |
| `/changelog` not installed | Abort with: *"/release requires the /changelog skill. Install it first (ADR-016, Issue #18)."* |
| `/changelog` returns empty output | Stop cleanly: *"No changes since `<last-tag>`. Nothing to release."* No tag created. |
| `gh` not authenticated | Abort. Tell the user to run `gh auth login`. |
| User declines approval | Cancel. Report "Release cancelled. No changes made." Exit 0. |
| `gh release create` fails after tag is pushed | Report failure. The tag is already pushed. Tell the user the tag stands and they can retry the release with `gh release create vX.Y.Z --notes-file …` manually. Do **not** delete the tag. |

## Invariants

- Never force-push tags. Never run `git push --force` or `git tag -f`.
- Never modify or delete existing tags.
- Never mutate without the literal `yes` approval.
- Never mutate in `--dry-run`.
- Never touch files outside the working tree except the GitHub Release
  (and the optional `Design/build-out-plan.md` update).

## Self-check before presenting the plan

- [ ] Prerequisites passed.
- [ ] Target version is valid semver and the tag does not already
      exist.
- [ ] `/changelog` produced non-empty notes.
- [ ] The annotated tag message, GitHub Release config, and command
      sequence are all shown in the plan.
- [ ] The approval prompt is present and explicit.

## Self-check after execution

- [ ] The tag exists locally (`git tag -l vX.Y.Z`) and on origin
      (`git ls-remote --tags origin vX.Y.Z`).
- [ ] `gh release view vX.Y.Z` returns a release with the expected
      title, notes, and draft/prerelease flags.
- [ ] Working tree is still clean.
- [ ] `main` has not moved.

## Handoff

`/release` is the terminus of the delivery chain. After it succeeds,
there is no downstream skill to invoke. The user's next action is
external: share the release URL, notify stakeholders, start the next
issue.

See [`example.md`](example.md) for a worked walkthrough.
