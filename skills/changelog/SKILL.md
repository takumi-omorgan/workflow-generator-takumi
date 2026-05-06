---
name: changelog
description: Parse git log between two refs and emit grouped, readable release notes in markdown to stdout, a file, or a GitHub Release body
permission-category: 1  # substitutable — renders to stdout / file / Release-body draft; publishing is /release's job, per workflow-guide §7
---

# changelog

Generate release notes from git history between two refs. The skill
reads `git log`, parses each commit for verb prefix, ADR tokens, and
issue references, groups the commits into sections (Features, Fixes,
Docs, Refactoring, Chores, Other), and emits markdown suitable for a
`CHANGELOG.md` entry or a GitHub Release body.

The skill is read-only with respect to git (it never creates tags,
commits, or branches). The one write it can perform is posting the
rendered markdown to a GitHub Release body via `gh release`. Release
tagging itself is out of scope — see [ADR-016](../../Design/adr/adr-016-changelog-and-release-notes-skill.md)
and the future `/release` skill.

## When to use this skill

Typical invocations:

```
/changelog --since-last-release
/changelog --from=v1.2.0 --to=HEAD
/changelog --from=v1.2.0 --to=v1.3.0 --output=CHANGELOG.md
/changelog --since-last-release --github-release=v1.3.0
```

Use this skill when:

- You are cutting a release and want draft notes to paste into
  `CHANGELOG.md` or a GitHub Release.
- You want a quick summary of what has landed on `main` since the last
  tag, before deciding whether to ship.
- You want to review what two refs differ by, grouped by area.

Do not use this skill to tag or publish a release — that belongs in
`/release` (future issue #19, which will call this skill internally).

## What this skill does not do

- Does not create, move, or delete git tags.
- Does not create GitHub Releases from scratch with a version bump —
  it can only write the body of a release that already exists or be
  told to create one at a tag that already exists. Tagging and version
  bumping live in `/release`.
- Does not push to any remote.
- Does not edit `CHANGELOG.md` in place beyond what `--output=FILE`
  writes. Merging a new section into an existing changelog is the
  user's call.
- Does not require a specific commit-message style. Commits that do
  not match the repo's `<verb>(<scope>): <what> (ADR-NNN, #issue)`
  convention land in an "Other" section rather than being dropped.

## Inputs

Exactly one of the following ref-selection modes is required:

- `--from=<ref> --to=<ref>` — explicit range. Both refs must resolve
  via `git rev-parse`. Either can be a tag, branch, or SHA.
- `--since-last-release` — auto-detect the most recent tag with
  `git describe --tags --abbrev=0`, use it as `<from>`, and use `HEAD`
  as `<to>`. If no tags exist, fall back to the repo's first commit
  (`git rev-list --max-parents=0 HEAD | tail -1`) as `<from>`.

Optional flags:

- `--output=FILE` — write the rendered markdown to `FILE` instead of
  stdout. Overwrites without prompting; if the user wants to preserve
  an existing file, they pass a different path.
- `--github-release=TAG` — post the rendered markdown as the body of
  the GitHub Release at `TAG` via
  `gh release edit TAG --notes-file -` (stdin). If the release does
  not yet exist, prompt once and offer `gh release create TAG --notes-file -`.
- `--title=STRING` — override the default H1 title
  (`# Changelog <from>..<to>`). Useful when posting to a GitHub
  Release, where the tag is already implied.
- `--include-merges` — include `Merge pull request` and `Merge #N:`
  commits as top-level entries. Default: excluded, because in a
  squash-merge workflow the merge commit duplicates the squashed
  commit it referenced.

If both `--from/--to` and `--since-last-release` are passed, stop and
ask the user which they meant. Do not guess.

## Output

- **Default:** rendered markdown written to stdout.
- **With `--output=FILE`:** the same markdown written to `FILE`, plus
  a one-line summary to stdout (`Wrote N entries to FILE`).
- **With `--github-release=TAG`:** the markdown piped into
  `gh release edit TAG --notes-file -` (or `gh release create` after
  confirmation). On success, print the release URL returned by `gh`.

### Markdown shape

```markdown
# Changelog <from>..<to>

## Features

- <subject> ([abbrev-sha](commit-url), [#N](issue-url), [ADR-NNN](adr-link))
- ...

## Fixes

- ...

## Docs

- ...

## Refactoring

- ...

## Chores

- ...

## Security

- ...

## Other

- ...
```

Section order is fixed as above. A section with no entries is
omitted entirely. If every section is empty, the output is:

```markdown
# Changelog <from>..<to>

_No changes in this range._
```

Within a section, entries are ordered by commit date, newest first.

**Duplicate detection.** Within each section, group commits whose
subjects describe the same underlying change. Two commits in the
same section are duplicates if any of the following holds:

- Their stripped subjects match exactly.
- They reference the same PR (same trailing `(#N)`).
- Their stripped subjects share the same `<verb>(<scope>):` prefix
  AND ≥75% of their remaining tokens overlap. The remaining-token
  comparison is token-set, lowercased, ignoring filler words ("via",
  "with", "for", "the", "a", "an"). Commits without a verb prefix
  are not grouped via this heuristic — they can still group via the
  exact-match or same-PR rules above. This avoids false-positive
  merges when distinct commits share a noun-phrase head with similar
  wording.

Render a duplicate group as a single entry. The newest commit's
stripped subject is the canonical text; all contributing short SHAs
are listed in the parenthetical.

## Data source: how git log is parsed

Run:

```
git log <from>..<to> --no-merges --format="%H%x1f%h%x1f%ct%x1f%s%x1f%b%x1e"
```

- `%H` full SHA, `%h` abbreviated SHA, `%ct` commit timestamp
  (seconds), `%s` subject, `%b` body.
- Fields separated by `\x1f` (unit separator), records by `\x1e`
  (record separator). This survives multi-line bodies, unlike
  newline-delimited formats.

If `--include-merges` is set, drop `--no-merges`.

For each record:

1. **Extract issue tokens.** Match `#(\d+)` in subject and body.
   Deduplicate per commit. The trailing `(#N)` that squash merges
   append is typically the primary PR reference. If the subject has
   the kit's two-suffix shape `<title> (#issue) (#PR)`, the second
   `(#N)` is the PR number.
2. **Extract ADR tokens.** Case-insensitive match
   `ADR-?(\d{1,4})` in subject and body. Zero-pad to three digits.
   Deduplicate per commit.
3. **Categorize the commit (label-primary, verb-fallback).** See
   "Categorization" below. This determines the section.
4. **Strip the verb prefix from the subject** (if present). Keep
   the rest as the entry text. The trailing `(#N)` references are
   moved into the issue-link slot during rendering.

### Categorization

Categorize each commit using a three-step rule, in order:

1. **Label-primary.** If the commit references a PR via a trailing
   `(#N)`, fetch the PR's labels:

   ```
   gh pr view N --json labels --jq '.labels[].name'
   ```

   Apply the label-to-section map below. If the PR has multiple
   labels, pick the highest-priority match (priority order:
   `security` > `bug` > `feature` > `refactor` > `design` > `docs` >
   `infra` > `chore`). If `gh` is unavailable, the lookup fails, or
   the PR returns no labels, fall through to step 2.

2. **Verb-fallback.** Match the subject against
   `^(feat|fix|docs|refactor|chore|test|build|perf|style|ci)(\([^)]+\))?:\s*`.
   The captured verb determines the section. No match → fall through
   to step 3.

3. **Other.** Lands in the Other section.

### Label-to-section mapping

Listed in priority order (top wins on multi-label PRs):

| Label      | Section       |
|------------|---------------|
| `security` | Security      |
| `bug`      | Fixes         |
| `feature`  | Features      |
| `refactor` | Refactoring   |
| `design`   | Refactoring   |
| `docs`     | Docs          |
| `infra`    | Chores        |
| `chore`    | Chores        |

### Verb-to-section mapping (fallback)

| Verb prefix | Section       |
|-------------|---------------|
| `feat`      | Features      |
| `fix`       | Fixes         |
| `docs`      | Docs          |
| `refactor`  | Refactoring   |
| `chore`     | Chores        |
| `test`      | Chores        |
| `build`     | Chores        |
| `perf`      | Refactoring   |
| `style`     | Chores        |
| `ci`        | Chores        |
| (none)      | Other         |

Why label-primary: GitHub squash merges produce commit subjects that
are PR titles, often without conventional-commit verb prefixes (e.g.
`Add config loader with documented precedence (#2) (#13)`). Such
commits land in "Other" under verb-only categorization despite being
ordinary `feature` PRs. Label-based categorization reads the canonical
intent (the PR's labels) and recovers the proper section. The verb
fallback covers direct-to-main commits and pre-PR-era history.

## Squash-merge handling

This repo uses GitHub squash merges. A squash produces a commit
whose subject is the PR title and whose body is the concatenation of
the squashed commit messages. Three concrete patterns show up:

1. Squash of a conventional-commit PR:
   `feat(skills): add /prepare-issue skill (ADR-013, #15)` — parsed
   normally; the trailing `(#15)` populates the issue link. Both
   label-primary and verb-fallback agree on the section.
2. Squash of a kit-shape PR with two-suffix `(#issue) (#PR)`:
   `Add config loader with documented precedence (#2) (#13)` — has
   no verb prefix. **Categorized via label-primary** (step 1 above)
   using the PR's labels (e.g. `feature` → Features). Verb-fallback
   would route it to "Other".
3. Manual merge commit written like `Merge #15: /prepare-issue skill
   (ADR-013)` — excluded by `--no-merges` by default. If
   `--include-merges` is set, it lands in "Other" (no verb prefix
   and the merge commit isn't a PR with labels) unless the subject
   also starts with a verb.

The parser must not choke on:

- Multi-paragraph bodies (handled by the `\x1e` record separator).
- Bodies containing stray `#` characters, backticks, or code
  fences — the body is only scanned for `ADR-` and `#N` tokens, not
  rendered.
- Commits whose subject is in another language or lacks ASCII
  punctuation — they land in "Other" rather than breaking.
- Non-ASCII characters in subjects — pass through verbatim.

## Rendering rules

Per entry:

```
- <subject-without-verb-prefix> ([<short-sha>](<commit-url>)[, [<short-sha-2>](<commit-url>)...][, [#N](<issue-url>)][, ADR-NNN])
```

- `<commit-url>`: `<origin-web-url>/commit/<full-sha>` where
  `<origin-web-url>` is derived from
  `git remote get-url origin` (convert `git@github.com:owner/repo.git`
  to `https://github.com/owner/repo`). If no origin is configured,
  omit the link and leave the bare short SHA.
- `<issue-url>`: `<origin-web-url>/issues/<N>`. Multiple issues are
  rendered as `[#1](...), [#2](...)`.
- ADR tokens are rendered as plain `ADR-013`, `ADR-016` — not linked,
  because ADR files live in the repo and their paths are already
  canonical.
- **Grouped commits.** When dedup grouped multiple commits into one
  entry (per "Duplicate detection" above), list each contributing
  short SHA as a linked reference, in commit-date order (newest
  first). The canonical text comes from the newest commit's
  stripped subject.

If `<subject-without-verb-prefix>` ends with `(#N)` and that `#N` is
already rendered as a linked issue, strip the trailing `(#N)` from the
subject so the reference is not duplicated.

### Title line

Default `# Changelog <from>..<to>`. When `<from>` is a tag and
`<to>` is `HEAD`, render as `# Changelog since <from>`. When both are
tags, render as `# Changelog <from> → <to>`. The `--title` flag
overrides all of this verbatim.

## Execution protocol

1. **Validate arguments.** Exactly one of `--from/--to` or
   `--since-last-release` must be set. Stop with a usage line if not.
2. **Resolve refs.** Run `git rev-parse <from>` and
   `git rev-parse <to>`. On failure, print the error and stop. For
   `--since-last-release`, run `git describe --tags --abbrev=0`
   first; if it fails, fall back to the first commit and note that
   in the run log (not the output).
3. **Detect origin URL.** Run `git remote get-url origin`. Convert
   SSH form (`git@github.com:owner/repo.git`) and HTTPS form
   (`https://github.com/owner/repo.git`) to the plain web URL
   `https://github.com/owner/repo`. If neither matches, proceed with
   bare SHAs.
4. **Collect commits.** Run the `git log` command in the "Data
   source" section. Parse with the `\x1e`/`\x1f` split.
5. **Fetch PR labels for label-based categorization.** For every
   unique `(#N)` extracted from the commit range, run
   `gh pr view N --json labels --jq '.labels[].name'` and cache
   the result. If `gh` is not installed or auth fails, skip this
   step and proceed to verb-fallback categorization only — emit a
   one-line warning to stderr
   (`gh unavailable; falling back to verb-prefix categorization`)
   so the user sees why the categorization may be coarser.
6. **Classify and group.** Apply the categorization rule from "Data
   source" (label-primary, verb-fallback, Other). Extract ADR and
   issue tokens. Build one list per section.
7. **Deduplicate.** Within each section, group commits per
   "Duplicate detection". Render each group as one entry, newest
   subject as canonical text, all SHAs as linked references in
   newest-first order.
8. **Render markdown.** Emit the title, then each non-empty section
   in fixed order.
9. **Write to target.** stdout (default), file (`--output`), or
   GitHub Release (`--github-release`). For `--github-release`:
   - Run `gh release view TAG` to check existence.
   - If exists: `gh release edit TAG --notes-file -` with the
     rendered markdown on stdin.
   - If not: show the rendered markdown and ask:
     *"Release TAG does not exist. Create it now via
     `gh release create TAG --notes-file -`? (yes/no)"*. On yes,
     create; on no, stop without writing.
10. **Report.** One-line summary to stdout: the number of entries
    per section and the destination.

## Edge cases

- **No tags, `--since-last-release` used** → fall back to first
  commit as `<from>`; print a one-line note on stderr
  (`No tags found — starting from first commit <sha>`).
- **Empty range** (`<from>..<to>` contains zero commits) → emit the
  `_No changes in this range._` body under the title. Still a
  successful run.
- **Unconventional commits with no PR reference** (no verb prefix
  AND no `(#N)` to look up) → land in "Other", full subject
  preserved.
- **PR with no labels** → label step returns an empty list; fall
  through to verb-fallback. If verb also misses, "Other".
- **PR with multiple labels** → pick the highest-priority match
  per the priority order in "Categorization" (`security` > `bug` >
  `feature` > `refactor` > `design` > `docs` > `infra` > `chore`).
  Labels not in the priority list are ignored for categorization.
- **`gh` not installed or auth fails (categorization step)** →
  warn once on stderr and proceed with verb-fallback only. The
  changelog still renders; some entries that would otherwise be
  Features/Fixes get the coarser categorization or land in "Other".
- **`gh pr view N` for a non-existent PR** (e.g. the `(#N)` was an
  issue reference, not a PR) → no labels returned; fall through to
  verb-fallback for that commit. Don't error.
- **Commits with neither ADR nor issue token** → entry is just the
  subject and a linked short SHA. Nothing else.
- **Merge commits with `--include-merges`** → subject kept verbatim;
  no PR lookup attempted (merge commits are not PRs); fall through
  the verb map (usually to "Other").
- **`gh` not installed** and `--github-release` was passed → stop
  with a clear error telling the user to install `gh` or remove the
  flag.
- **Not in a git repo** → stop with `fatal: not a git repository`
  from `git` verbatim.
- **`--from` or `--to` resolves but is ahead of the other** (empty
  diff) → same handling as empty range.

## Self-check before writing output

- [ ] Exactly one ref-selection mode is active.
- [ ] Both refs resolved via `git rev-parse`.
- [ ] The markdown has a title and at least one section (or the
  "No changes" stub).
- [ ] Every rendered entry has a resolvable short SHA.
- [ ] Every `#N` in rendered entries is a linked reference (or the
  origin URL could not be detected, in which case it is plain).
- [ ] No `<from>..<to>` placeholders remain in the title.
- [ ] Every commit with a `(#N)` PR reference was either label-
  categorized or fell through to verb-fallback for a documented
  reason (no labels, gh unavailable, etc).
- [ ] No commit appears under more than one section (sanity check
  on the dedup-then-categorize pipeline).
- [ ] When `--output=FILE` is used, the parent directory of `FILE`
  exists.
- [ ] When `--github-release=TAG` is used, `gh` is installed and
  either the release exists or the user confirmed creation.

If any fail, fix and re-render before writing.

## Handoff

The rendered markdown is the deliverable. Typical next steps for
the user:

- Paste into `CHANGELOG.md` under a new `## [version] — date`
  heading.
- Review and tweak the GitHub Release body after this skill posts
  it.
- Run `/release` (future issue #19), which calls this skill with
  `--since-last-release --github-release=<new-tag>` as part of a
  larger tag-and-publish flow.

See [`example.md`](example.md) for a worked run on this repo's own
recent history.
