# Public Distribution Export

This kit is developed in a **private source repo** and published as a
separate **public repo** that is a *generated, verified subset* of the
source — never a renamed remote and never hand-maintained. This document is
the export **contract** and the **pre-publish validation command**. The model
is decided in
[ADR-056](../design/adr/adr-056-two-repo-public-distribution-export-model.md);
the versioning/changelog policy it relies on is
[ADR-055](../design/adr/adr-055-public-distribution-versioning-policy.md); the
full design rationale is in
[`design/public-distribution-export-design-20260609.md`](../design/public-distribution-export-design-20260609.md).

> **Scope.** The tooling here **builds and verifies** the public artifact. It
> does **not** create or push the public repo, switch `gh` identity, or cut a
> release — that is a separate, identity-gated step performed by a human after
> a clean export.

## The two surfaces

| Script | Role | Side effects |
|---|---|---|
| `bin/export-public` | Build the public tree from `HEAD`, transform it, verify it, run the validation suite inside it. | Writes only to the export dir (default `dist/`, gitignored). **Never pushes.** |
| `bin/check-public-export` | Deterministic verifier over a staging tree. Reads only; names every violation. | None. |
| `bin/export-eval` | Offline fixture harness for the verifier; wired into `bin/self-test`. | None. |

> **These three scripts are source-repo only.** The export prunes them (and
> their `bin/lib/` helpers, fixtures, and this runbook) from the public
> artifact and reconciles the public `kit.json`, `bin/self-test`, and
> `docs/README.md` to match — a published distribution does not re-publish
> itself, and shipping the verifier would be self-referential. See
> [ADR-056](../design/adr/adr-056-two-repo-public-distribution-export-model.md)
> Decision 6.

## What ships, what does not

The export takes **tracked files at `HEAD`** (`git archive`, so untracked
material such as `.hermes/` can never be included) and applies root-anchored
include / exclude / transform rules. All patterns are anchored to the **export
root**, so nested example-project content is preserved.

**Excluded (internal only — never ships):**

- the kit's own `design/adr/**` (private decision history — replaced publicly
  by [`docs/architecture.md`](architecture.md))
- root-level `design/*.md` reports, and `design/prd-addenda/**`
- `notes/**`, `archive/**`, `.hermes/**`
- every `prompts/*` **except** `prompts/_template.md`
- `ai-review/config.json`, `ai-review/artifacts/**`

**Required to be present (public-facing):**

- `docs/architecture.md` — the single current architecture statement
- `prompts/_template.md` — the installer and `prepare-issue` depend on it

**Preserved:** `examples/projects/*/design/**` — including those example
projects' own `design/adr/**`. These are illustrative *output* of the kit, not
the kit's governing ADRs. The verifier is root-anchored to the kit's own
`design/adr/`, so example ADRs and the links into them are never flagged.

**Transforms applied on the way out:**

- old owner/repo URLs → the public repo name
- stale version pins in install commands → the export version (`tag ==
  kitVersion`, enforced)
- personal absolute paths (`~/dotfiles`, `/Users/...`) scrubbed
- markdown links that resolve into an excluded private path are de-linked to
  plain text (so no shipping doc dangles into the excluded kit ADR set)

## The verifier checks (each names the offending file/path/reference)

| ID | Check |
|---|---|
| A | only allowlisted top-level entries are present |
| B | excluded private/source paths are absent |
| C | required public artifacts are present |
| D | no markdown link points into an excluded private/source path |
| E | no old owner/repo URL strings remain |
| F | no personal absolute or temp/audit paths ship |
| G | no stale version pin in install-surface files (`README.md`, `docs/install.md`, `bin/bootstrap-workflow-kit`) |

## Pre-publish validation command

Run a dry-run export and verify it — no GitHub access required:

```bash
# build to dist/public, keep it, run the verifier and the in-export gates
bin/export-public --keep --dest dist/public

# or just verify an already-built staging tree
bin/check-public-export --staging dist/public --version v<X.Y.Z>
```

A clean run prints the file count, `verifier clean`, and `gates passed`, and
exits `0`. Any leak, orphaned link, missing artifact, or stale reference exits
non-zero and names what to fix. The same contract runs offline on every change
via `bin/self-test` (which calls `bin/export-eval`).

`bin/export-public` refuses to run when the requested `--version` disagrees
with `kit.json` `kitVersion`, keeping `tag == kitVersion` a machine-enforced
invariant (ADR-055).

## After a clean export (out of scope for this tooling)

Publishing is a deliberate, identity-gated step done by a human:

1. Switch `gh` auth to the public-repo owner and confirm with `gh auth status`.
2. Create/push the public repo from the verified `dist/` tree as a fresh
   history (the public repo does not inherit internal commit history).
3. Tag `v<kitVersion>`, cut the GitHub release, and upload the bootstrap asset.

These steps are intentionally **not** automated here; `bin/export-public`
performs no network or GitHub action.
