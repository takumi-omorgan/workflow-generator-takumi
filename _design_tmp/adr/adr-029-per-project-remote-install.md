# ADR-029: Recommend per-project remote install over local-clone-once

**Status:** accepted
**Date:** 2026-04-26

## Context

[ADR-009](adr-009-installer-script.md) introduced
`bin/install-workflow-kit`, which scaffolds a target project from a
kit clone. Today's documented user flow (per `README.md` and
`docs/install.md`) asks the user to:

1. Clone the kit once into a fixed local path (e.g.
   `~/src/workflow-generator`).
2. For every new project, run the installer from that path:
   `~/src/workflow-generator/bin/install-workflow-kit
   --project-name=NAME`.

This is friction. Users have to:

- Pick a permanent location for the kit clone before they can use
  it.
- Remember to `git pull` the kit clone before installing into a new
  project to pick up new releases.
- Carry the clone across machines (or re-establish it on each one).
- Reason about which version of the kit a given target project was
  scaffolded from.

The intent of the local-clone model was simplicity, but in practice
"clone once, reuse forever" creates a slowly-drifting local copy
that gets out of date and surprises the user when a fresh project
turns out to be using yesterday's kit.

A better default for end users is **fetch-on-demand, version-pinned**:
each project install grabs the exact tagged version of the kit from
GitHub, runs the installer, and discards the temporary copy. The
target project ends up with everything it needs (skills under
`.claude/skills/`, prompts, CLAUDE.md, etc.); the temporary kit
clone vanishes. The next project picks the version it wants
explicitly.

The local-clone path remains useful for **kit developers and
contributors** — anyone editing the kit itself needs a local clone
to work in, and `link-skills` makes that clone usable as a live
dogfooding source. Contributors are a small minority of the user
population.

This ADR refines [ADR-009](adr-009-installer-script.md) — it does
not supersede it. The installer script's behaviour is unchanged.
What changes is the recommended **invocation pattern** for end
users: fetch-on-demand instead of long-lived clone.

This ADR also does not supersede
[ADR-001](adr-001-project-local-installation-model.md). Skills still
end up under each target project's `.claude/skills/`, per-project,
no global install. The change is purely about how the kit's source
gets to the installer at install time.

## Options considered

### Option A: Keep the local-clone-once model as primary

- Pros: no new code; matches the current docs.
- Cons: friction described above; users get a stale clone over
  time; cross-machine setup is awkward; version of the kit that
  scaffolded a given target project is implicit, not pinned.

### Option B: Document a `gh repo clone` one-liner as primary; keep local-clone as a contributor path

- Pros: zero new code (just docs); explicit version pinning via
  `--branch=vX.Y.Z`; temporary clone vanishes on completion; users
  who are not kit contributors never need a long-lived kit clone.
- Cons: user has to copy-paste a multi-line snippet; the snippet
  needs to be kept in sync between README and docs/install.md
  (manageable).

### Option C: Add a small `bin/bootstrap-workflow-kit` script that does the fetch-and-install in one command, distributed via the GitHub Releases page

- Pros: single user-facing command (`bootstrap-workflow-kit
  --project-name=NAME`); consolidates the snippet into one
  inspectable script; pinnable via `WORKFLOW_KIT_VERSION` env or
  a flag; the script falls back to plain `git clone` if `gh` is
  unavailable.
- Cons: one more script to maintain; users may want to inspect
  before running (mitigation: ship as a release asset from the
  tagged repo, not piped from raw URLs).

### Option D: Rewrite the installer to fetch its own dependencies at runtime (single-file installer)

- Pros: ultimate single-command experience.
- Cons: large refactor of `install-workflow-kit`; harder to dogfood
  while developing the kit; harder to inspect what gets installed
  before running.

## Decision

Adopt **Option B + Option C together.**

Option B (docs change) is the primary, always-available path:

```bash
TMPKIT="$(mktemp -d)" && \
  gh repo clone olivermorgan2/workflow-generator "$TMPKIT" -- --depth=1 --branch=v3.2.0 && \
  "$TMPKIT/bin/install-workflow-kit" --project-name=my-project && \
  rm -rf "$TMPKIT"
```

Three lines, explicit, no piping or trust assumptions beyond
`gh repo clone` itself. Pinned by `--branch=vX.Y.Z` so a given
project's scaffolding is reproducible.

Option C (the bootstrap script) is the convenience wrapper for
users who prefer one command:

```bash
bash <(curl -fsSL https://github.com/olivermorgan2/workflow-generator/releases/download/v3.2.0/bootstrap-workflow-kit) --project-name=my-project
```

The bootstrap script ships as a release asset from each tagged
release, so users can also download it explicitly first
(`gh release download`), inspect it, and run locally. It is a
~30-line shell script that does what Option B does, plus version
defaulting via `WORKFLOW_KIT_VERSION` env var.

The local-clone path stays documented under a "Contributors" or
"Kit developers" section of `docs/install.md`, marked clearly as
the contributor flow (not the recommended user flow).

This ADR refines [ADR-009](adr-009-installer-script.md). The
installer's behaviour, flags, and outputs are unchanged. The change
is documentation-and-bootstrap-only.

## Consequences

- README's quick-start replaces the "clone once locally, then run
  from clone" flow with the `gh repo clone` one-liner. Users no
  longer need to think about a long-lived kit clone path.
- `docs/install.md` documents two paths:
  1. **Per-project remote install** (recommended for users) — Option B.
  2. **Local kit clone** (recommended for kit contributors only) —
     a clearly-labelled contributor section.
- A new `bin/bootstrap-workflow-kit` script ships in the repo and
  is uploaded as a release asset on each tagged release. The script:
  - Detects `gh` and uses it; falls back to `git clone` if absent.
  - Defaults to the latest tagged version, overrideable via
    `WORKFLOW_KIT_VERSION=vX.Y.Z` env var.
  - Forwards all CLI args to `bin/install-workflow-kit`.
  - Cleans up the temporary clone on exit (success or failure).
- Each tagged release's GitHub Release uploads
  `bootstrap-workflow-kit` as an asset so users can fetch a stable
  version directly. The `/release` skill (per ADR-017) is updated
  to upload this asset.
- Cross-machine setup becomes trivial: a user with `gh` installed
  can scaffold a new project anywhere without a pre-existing kit
  clone.
- Per-project version pinning becomes explicit and visible in the
  install command (`--branch=vX.Y.Z` or `WORKFLOW_KIT_VERSION=vX.Y.Z`).
  Reproducing a project's scaffold becomes mechanical.
- Kit dogfooding is unaffected. Contributors still clone the kit
  locally and run `~/dotfiles/claude-config/bin/link-skills` per
  the dogfooding playbook.
- The installer script (`bin/install-workflow-kit`) is unchanged;
  ADR-009's decision stands.
- Per [ADR-026](adr-026-kit-versioning-policy.md), this change is
  **MINOR** — additive. The local-clone path remains supported and
  documented (under contributors); existing installation flows
  continue to work without modification.
