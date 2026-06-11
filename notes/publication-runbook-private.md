# Private publication runbook — public distribution

This note is for the private/source repo only. It lives under `notes/`, which is excluded by the public export contract and must not be copied into `olivermorgan2/claude-workflow-kit`.

## Model

- Private/source repo: `takumi-omorgan/workflow-generator-takumi`
- Public generated repo: `olivermorgan2/claude-workflow-kit`
- The public repo is a generated artifact, not a fork, mirror, renamed remote, or hand-maintained copy.
- Source `kit.json` `kitVersion` is the canonical version.
- Public tag must equal `v<kitVersion>`.
- `bin/export-public` builds and verifies the public tree. It never pushes, creates repos, switches auth, tags, or releases.
- Publishing is an identity-gated human step performed as `olivermorgan2`.

## What does not ship

The export is generated from tracked files at source `HEAD` and excludes private/source-only material, including:

- root `design/adr/**`
- root `design/*.md` reports and `design/prd-addenda/**`
- `notes/**`
- `archive/**`
- `.hermes/**`
- private prompts except `prompts/_template.md`
- `ai-review/config.json`
- `ai-review/artifacts/**`
- source-only export tooling/runbooks such as `bin/export-public`, `bin/check-public-export`, `bin/export-eval`, fixtures, and `docs/publishing.md`

Public architecture is represented by `docs/architecture.md`, not the internal ADR history.

The exported `CHANGELOG.md` is curated to the **current release section only** (`bin/lib/export-changelog.py`); internal development history and its commit/issue deep links never ship.

## Before any public release

From the private/source repo:

```bash
cd /Users/hermes/workflow-generator-takumi-m5
git switch main
git pull --ff-only origin main
git status -sb
```

Expected status may include untracked `.hermes/`; that is fine. Export uses `git archive HEAD`, so untracked files cannot ship.

Run the source validation suite:

```bash
git diff --check
./bin/validate-kit-json
./bin/check-consistency
./bin/self-test
./bin/check-install-render
./bin/review-eval
./bin/collect-eval
./bin/export-eval
```

Then build and verify the public artifact:

```bash
rm -rf dist/public
./bin/export-public --dest dist/public --keep
```

Clean output should say roughly:

```text
export-public: ok — built vX.Y.Z for olivermorgan2/claude-workflow-kit (... files), verifier clean, gates passed
```

Optional inspection:

```bash
cd /Users/hermes/workflow-generator-takumi-m5/dist/public

grep -n '"kitVersion"' kit.json
sed -n '1,40p' CHANGELOG.md
grep -c '^## v' CHANGELOG.md                                  # expect: 1
grep -n 'github.com/.*/\(commit\|issues\|pull\)/' CHANGELOG.md || echo 'no deep links'
grep -n 'releases/download/v' README.md docs/install.md bin/bootstrap-workflow-kit

test -f docs/architecture.md && echo 'architecture present'
test -f prompts/_template.md && echo 'template present'

test ! -e design/adr && echo 'private ADRs absent'
test ! -e notes && echo 'notes absent'
test ! -e archive && echo 'archive absent'
test ! -e .hermes && echo '.hermes absent'
```

## First public publication

Use this only when `olivermorgan2/claude-workflow-kit` does not exist yet.

Authenticate as the public owner:

```bash
gh auth login                    # if needed
gh auth switch -u olivermorgan2  # if multiple accounts exist
gh auth status                   # MUST show olivermorgan2 active
```

Create the public repo from the verified export tree as fresh public history:

```bash
cd /Users/hermes/workflow-generator-takumi-m5/dist/public

git init
git add -A
git commit -m "v5.0.0 — public distribution"

gh repo create olivermorgan2/claude-workflow-kit \
  --public \
  --source=. \
  --remote=origin \
  --push
```

Tag and create the release. Release notes are the **current version's
section only**, generated from the source repo's changelog — never the
whole `CHANGELOG.md`:

```bash
git tag v5.0.0
git push origin v5.0.0

python3 /Users/hermes/workflow-generator-takumi-m5/bin/lib/export-changelog.py \
  --mode notes --version v5.0.0 \
  /Users/hermes/workflow-generator-takumi-m5/CHANGELOG.md \
  > /Users/hermes/workflow-generator-takumi-m5/dist/release-notes-v5.0.0.md

gh release create v5.0.0 \
  --repo olivermorgan2/claude-workflow-kit \
  --title "v5.0.0" \
  --notes-file /Users/hermes/workflow-generator-takumi-m5/dist/release-notes-v5.0.0.md \
  bin/bootstrap-workflow-kit
```

Smoke-test the release asset:

```bash
curl -fsSL https://github.com/olivermorgan2/claude-workflow-kit/releases/download/v5.0.0/bootstrap-workflow-kit | head
```

Optional install smoke test in a temp project:

```bash
tmpdir=$(mktemp -d)
cd "$tmpdir"
git init
bash <(curl -fsSL https://github.com/olivermorgan2/claude-workflow-kit/releases/download/v5.0.0/bootstrap-workflow-kit)
```

## Future public releases after the repo exists

Do not recreate the public repo. Do not manually edit public files. Regenerate the public tree from private source, then copy it into a clean clone of the existing public repo and commit normally.

Example for `v5.1.0`:

```bash
# 1. In private/source repo, update release metadata through normal PR flow.
cd /Users/hermes/workflow-generator-takumi-m5
git switch main
git pull --ff-only origin main

./bin/release-suggest --since-last-release --format text
# Update kit.json kitVersion and CHANGELOG.md via reviewed source PR.
# Merge that PR before publishing.

# 2. Rebuild verified public artifact.
rm -rf dist/public
./bin/export-public --dest dist/public --keep

# 3. Clone existing public repo to a temp worktree.
tmp=$(mktemp -d)
git clone git@github.com:olivermorgan2/claude-workflow-kit.git "$tmp/claude-workflow-kit-public"

# 4. Replace public repo contents with generated artifact, preserving .git.
cd "$tmp/claude-workflow-kit-public"
find . -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
rsync -a --delete /Users/hermes/workflow-generator-takumi-m5/dist/public/ ./

# 5. Commit and push generated changes.
git status -sb
git add -A
git commit -m "v5.1.0 — public distribution"
git push origin main

# 6. Tag and release with current-version-only notes generated from the
#    source repo's changelog (never --notes-file CHANGELOG.md).
git tag v5.1.0
git push origin v5.1.0

python3 /Users/hermes/workflow-generator-takumi-m5/bin/lib/export-changelog.py \
  --mode notes --version v5.1.0 \
  /Users/hermes/workflow-generator-takumi-m5/CHANGELOG.md \
  > /Users/hermes/workflow-generator-takumi-m5/dist/release-notes-v5.1.0.md

gh release create v5.1.0 \
  --repo olivermorgan2/claude-workflow-kit \
  --title "v5.1.0" \
  --notes-file /Users/hermes/workflow-generator-takumi-m5/dist/release-notes-v5.1.0.md \
  bin/bootstrap-workflow-kit
```

## Important differences: first publish vs future publish

First publish:

- `dist/public` becomes a new git repo.
- `gh repo create ... --source=. --push` creates `olivermorgan2/claude-workflow-kit`.
- Public history starts with one generated commit.

Future publish:

- Clone the existing public repo.
- Replace contents from regenerated `dist/public`.
- Commit normally on public `main`.
- Do not force-push unless intentionally repairing a bad initial publication.

## Common failure modes

- Wrong GitHub identity: stop if `gh auth status` does not show `olivermorgan2` active.
- Public repo already exists: do not run `gh repo create`; use the future-release flow.
- `export-public` fails: fix the private/source repo, do not patch `dist/public` manually.
- Version mismatch: `bin/export-public --version vX.Y.Z` must match `kit.json` `kitVersion`.
- Missing release asset: README install commands depend on the GitHub release asset `bin/bootstrap-workflow-kit`.
- Manual public edits: avoid them; they will be overwritten by the next generated export.

## Current v5.0.0 status at time of writing

- Source-side hardening complete through public release-candidate metadata.
- `kit.json` version: `5.0.0`.
- Final audit passed with `./bin/export-public --dest dist/public --keep`.
- Public repo `olivermorgan2/claude-workflow-kit` had not yet been created.
- Active `gh` account during audit was `takumi-omorgan`; switch to `olivermorgan2` before publication.
