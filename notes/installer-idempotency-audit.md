# Installer idempotency & fresh-start audit — M0-3

**Date:** 2026-06-05
**Branch:** `m0-baseline-health-and-drift`
**Issue:** M0-3 (Audit installer idempotency and fresh-start behavior)
**Subject:** `bin/install-workflow-kit` (the local installer that
`bin/bootstrap-workflow-kit` ultimately invokes).

## Method

All runs used a throwaway temp directory (`mktemp -d`), cleaned up after.
Nothing was written into the kit repo. The installer was driven
non-interactively so the run is deterministic and repeatable.

```bash
KIT=/path/to/workflow-generator-takumi
TGT=$(mktemp -d)/fresh-proj
# RUN 1 — fresh install
"$KIT/bin/install-workflow-kit" --target="$TGT" --project-name=demo --non-interactive
# RUN 2 — idempotent rerun (no flags changed)
"$KIT/bin/install-workflow-kit" --target="$TGT" --project-name=demo --non-interactive
# RUN 3 — forced rerun
"$KIT/bin/install-workflow-kit" --target="$TGT" --project-name=demo --non-interactive --force
```

## RUN 1 — fresh install

**Result: succeeds (exit 0), with one defect in the git step.**

Generated tree (top level):

```
.claude/skills/<19 skills>/        # full skill cohort copied
.claude/bin/sync-adr-index         # ADR-index helper (per ADR-023)
.github/pull_request_template.md
.gitignore                         # from templates/gitignore.target
CLAUDE.md                          # rendered from template
design/adr/README.md               # seeded with sync-adr-index marker fences
prompts/_template.md
templates/<12 runtime templates>
notes/                             # created empty
```

Prompts (non-interactive): the installer printed a `git init`, then
`creating initial commit`, then `done`. With `--non-interactive` it never
blocks for input; missing placeholders are reported as warnings (see
"Placeholder classification" below).

### Defect: initial commit omits `design/`

After RUN 1's commit, `git status` in the target shows:

```
?? design/adr/README.md
```

**Root cause.** The installer creates `design/adr/` (lowercase, the
ADR-045 canonical casing) and seeds `design/adr/README.md`, but the git
staging block lists the directory as `Design` (capital):

```sh
git -C "$TARGET_DIR" add \
  CLAUDE.md .claude .github .gitignore \
  Design \              # <-- capital D; created dir is lowercase 'design'
  prompts notes templates 2>/dev/null || true
```

On a case-sensitive checkout the `git add Design` matches nothing and the
`2>/dev/null || true` swallows the error, so `design/adr/README.md` is
**never staged**. The "initial commit" the installer advertises is
therefore incomplete: a freshly installed project is left with an
untracked file that `bin/sync-adr-index` depends on. The condition
persists across reruns (the file already exists, so RUN 2/3 skip
re-seeding it, and it stays untracked).

**Severity:** high (every fresh install is affected; the headline
"installs and commits cleanly" promise is broken).

**Disposition:** **not fixed in this M0 PR.** The open M1 PR
(`m1-front-door-simplification`, PR #1) already rewrites this exact block
to lowercase `design` (verified on `origin/m1-front-door-simplification`),
and M1 substantially refactors `bin/install-workflow-kit` overall. Fixing
it again in M0 would guarantee a merge conflict on a file M0 has no other
reason to touch. Captured in `notes/bug-fixes.md` (installer cluster) so
it is tracked regardless of M1's merge timing. **If M1 is dropped or
reshaped such that this line survives, promote the bug-fixes entry to a
standalone one-line PR** (`Design` → `design`).

This is distinct from the already-filed installer issue #60 (which was
about `design/adr/README.md` not being *created* at all); here the file
is created correctly but not *committed*.

## RUN 2 — idempotent rerun (no `--force`)

**Result: clean and idempotent (exit 0).**

- Every skill: `skip (exists)`.
- `.claude/bin/sync-adr-index`, `prompts/_template.md`, all 12 templates,
  `.github/pull_request_template.md`, `.gitignore`, `design/adr/README.md`,
  `CLAUDE.md`: all `skip (exists)`.
- Git step: `nothing to commit (idempotent re-run)` — **no second commit
  created**. `git log` still shows exactly one commit.
- `git status` unchanged: the same single `?? design/adr/README.md` from
  RUN 1 (no new churn introduced by the rerun).

Idempotency verdict for the default path: **correct**. A rerun makes zero
new file changes and zero new commits.

## RUN 3 — forced rerun (`--force`)

**Result: re-copies as designed (exit 0).**

- Skills and templates: `overwrite:` (re-copied on top, as `--force`
  intends).
- `CLAUDE.md` re-rendered; content identical → git step found nothing new
  to commit (no duplicate commit).
- `git status` still `?? design/adr/README.md` (the casing bug is
  orthogonal to `--force`).

`--force` behaves as documented: it overwrites kit-managed files but does
not fabricate spurious commits when content is unchanged.

## Placeholder classification

A non-interactive install with only `--project-name` leaves **25 distinct
`{{UPPER_SNAKE}}` tokens unresolved** in the rendered `CLAUDE.md`. Each is
also reported as a `warning: placeholder {{X}} left unfilled` line. The
installer fills `PROJECT_NAME` and defaults it to the target basename when
omitted; everything else is left literal.

Classified per M0-3's required/optional/defective scheme:

### Required (genuinely needed day-one) — 4

`GITHUB_OWNER`, `GITHUB_REPO`, `DEFAULT_BRANCH`, and `PROJECT_NAME`
(PROJECT_NAME is already handled — defaulted/prompted). These match M1
Issue 3's "only project name, owner, repo, and default branch are
required" target. Today they are **not** distinguished from optional ones
— all 25 are treated identically.

### Optional (project can fill later) — 20

`PROJECT_TAGLINE`, `PRIMARY_LANGUAGE`, `FRAMEWORK`, `DATA_LAYER`,
`KEY_LIBRARIES`, `PACKAGE_MANAGER`, `INSTALL_COMMAND`, `DEV_COMMAND`,
`BUILD_COMMAND`, `TEST_COMMAND`, `LINT_COMMAND`, `TEST_FRAMEWORK`,
`TEST_LOCATION`, `FORMATTER`, `MODULE_SYSTEM`, `CURRENT_MILESTONE`,
`CURRENT_PHASE`, `DEPLOY_TARGET`, `SECRETS_LOCATION`, `COMMIT_STYLE`,
`BRANCH_NAMING`. These are reasonable to discover after day one.

**Drift against the M1 target:** today they render as raw `{{TOKEN}}`
template syntax, not as the `_TBD_` markers M1 Issue 3 wants. An agent
reading the generated file cannot distinguish "unknown but acceptable"
from "must fill before proceeding" — both look like leftover template
syntax. This is exactly what M1 Issue 3 sets out to fix.

### Defective — 1

`{{UPPER_SNAKE}}` is **not a real placeholder**. It appears inside the
template's own header comment documenting the placeholder convention:

```
PLACEHOLDERS (all use {{UPPER_SNAKE}} syntax; grep them with:
    grep -E '\{\{[A-Z_]+\}\}' CLAUDE.md
```

The installer's `discover_placeholders` regex (`\{\{[A-Z][A-Z0-9_]*\}\}`)
greedily matches this documentation token, so it gets reported as an
unfilled placeholder and, because the header comment is rendered verbatim
into `CLAUDE.md`, the literal `{{UPPER_SNAKE}}` survives into the output.
Two angles to fix (whichever M1 prefers, since M1 owns this template):
either escape/rephrase the comment so the token isn't literal, or have the
installer ignore placeholders found inside the leading comment block.

**Disposition:** not fixed in M0 — `templates/claude-md-template.md` is in
the M1 PR's change set (M1 Issue 3 reworks placeholders), and the M1
branch still carries this stray token, so the cleanest place to resolve it
is inside M1's placeholder rework. Flagged here so it isn't lost.

## README / install-doc drift

- `docs/install.md:256` shows `git add .claude CLAUDE.md Design prompts
  notes` — the **same `Design` capitalisation defect** as the installer,
  in the manual-install instructions. A user copy-pasting it on a
  case-sensitive FS would also fail to stage `design/`. This is M1 Issue 5
  territory (stale `Design` casing in `docs/install.md`) **and** is in the
  M1 PR's diff for `docs/install.md`. Not fixed in M0 (M1 owns the file).
- No other contradiction was found between the installer's actual
  generated tree and what `README.md` / `docs/install.md` describe: the
  skill copy, template copy, `.gitignore` seeding, ADR-README seeding, and
  optional `--with-docs` / `--license` paths all match their documentation.

## Repo-coordinate drift (informational)

`bin/bootstrap-workflow-kit` and `bin/install-workflow-kit` headers point
at `olivermorgan2/workflow-generator` (the upstream this repo,
`takumi-omorgan/workflow-generator-takumi`, was forked from), with example
URLs at `v3.3.0`. Bootstrap's remote-fetch path was **not exercised** in
this audit (it would hit the network and depend on a published release).
For a fork that intends to publish its own releases, the default
`WORKFLOW_KIT_REPO` would need updating — but that is a deliberate
release-engineering decision, not a low-risk mechanical fix, so it is
recorded as a follow-up rather than changed here.

## Verdict

**Idempotency: correct.** Reruns make no file changes and no duplicate
commits; `--force` re-copies without spurious commits. **Fresh-start: one
real defect** — the initial commit omits `design/` because of `Design`
vs `design` casing in the installer's `git add` (and the same casing in
the manual-install doc). Both are already inside the open M1 PR's change
surface, so M0 documents them and defers the fix to avoid a conflicting
edit. **Placeholders:** 4 required, 20 optional, 1 defective stray
(`{{UPPER_SNAKE}}`); all 25 currently render as raw template syntax rather
than `_TBD_`, which is precisely the M1 Issue 3 problem.
