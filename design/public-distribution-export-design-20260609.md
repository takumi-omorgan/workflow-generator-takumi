# Public Distribution Export — Design Proposal

**Date:** 2026-06-09
**Status:** DRAFT — export model awaiting approval (plan-first, ADR-006).
**Versioning & changelog policy (O1/O2): RESOLVED** — see
[ADR-055](adr/adr-055-public-distribution-versioning-policy.md) (issue #17).
**Author:** Claude Code (PTY session, Hermes-supervised)
**Scope:** How to publish this repository as a clean public distribution
repo at `olivermorgan2/claude-workflow-kit` without leaking internal
artifacts, stale names, or stale version pins.

> This is a design document, not an implementation. Per the repo's
> plan-first rule, the export model below is not built until approved. The
> versioning/changelog **policy** (O1/O2) is settled in
> [ADR-055](adr/adr-055-public-distribution-versioning-policy.md); the
> two-repo **export-model** decision is recorded as its own ADR when issue
> #16 lands. (The originally reserved number `ADR-053` was assigned to the
> architecture-document decision before this work landed — see O6.)

> **Revision — 2026-06-09 (supersedes §6 as originally drafted).**
> The public distribution now ships a **single, current, public-facing
> architecture document** — [`docs/architecture.md`](../docs/architecture.md)
> — and **does NOT ship the accepted ADR set (`/design/adr/**`) by
> default.** The ADRs, evaluation reports, roadmaps, and superseded
> designs remain in this source/internal repo as the private decision
> history. `docs/architecture.md` states explicitly that detailed ADR
> history is maintained internally and is not part of the public
> distribution. The sections below are updated to reflect this; the
> known implementation cost of excluding ADRs (orphaned links, `kit.json`
> metadata, the markdown link checker) is accounted for in §2.3, §5,
> and the rewritten §6. Individual ADRs may still be promoted into the
> public set later by explicit selection, but that is opt-in, not the
> default.

---

## 1. Decision summary: two-repo model

We keep a **two-repo distribution model**:

| Repo | Role | Pushed to public? |
|---|---|---|
| `takumi-omorgan/workflow-generator-takumi` (this repo) | **Source of truth.** Holds everything: skills, docs, ADRs, *and* internal eval reports, roadmaps, per-issue prompts, working notes, archive. | **No.** Never pushed to the public remote. |
| `olivermorgan2/claude-workflow-kit` (new) | **Generated distribution artifact.** A curated, transformed subset of the source. | Yes — this is the public repo. |

The public repo is **produced by a deterministic export tool**, not by
renaming a remote or force-pushing the source. This guarantees internal
material can never reach the public history, and the export is
reproducible and reviewable (dry-run + leak-scan before any push).

This warrants a new ADR because it establishes a distribution decision
not covered by ADR-029 (per-project remote install) — that ADR governs
how *target projects* fetch the kit; it assumes a public repo exists but
does not say how that repo is produced.

---

## 2. Public export contract

The export takes tracked files at `HEAD` (via `git archive`, so untracked
material like `.hermes/` can never be included) and produces a clean tree
by applying **include**, **exclude**, and **transform** rules.

All path patterns are **root-anchored** (leading `/` = repo root) so that
nested `examples/projects/*/design/**` and similar are preserved.

### 2.1 INCLUDE (ships to public)

| Path | Notes |
|---|---|
| `/README.md` | transformed (name + version) |
| `/LICENSE` | as-is |
| `/CLAUDE.md` | transformed — **scrub the dogfooding section** that points to `~/dotfiles/...` personal paths (see §6) |
| `/kit.json` | as-is; `kitVersion` is the version source of truth |
| `/skills/**` | all skills |
| `/templates/**` | all templates |
| `/docs/**` | transformed (name + version); **includes the new public-facing [`docs/architecture.md`](../docs/architecture.md)** — the single current architecture statement that replaces shipping the ADR set. Also transformed to **neutralize links into the now-excluded `/design/adr/**`** (see §2.3). Some prose describes internal-only dirs — see open question O4 |
| `/schemas/**` | as-is |
| `/bin/**` | all programmatic surfaces (install/bootstrap/validators ship) |
| `/ai-review/**` | the M5 prompt pack, config **example**, and eval fixtures (artifacts/ and config.json already gitignored) |
| `/examples/**` | including `examples/projects/*/design/**` and `.../design/adr/**` — these are **worked-example** ADRs *inside* example projects (illustrative output of the kit), not the kit's own governing ADRs; they still ship |
| `/prompts/_template.md` | **only this one file** from `prompts/` |
| `/.github/**` | issue/PR templates + `kit-checks.yml` CI |
| `/.gitignore` | scrub personal-only entries (`mac-connect*`, `.obsidian/`, `.hermes/`) |
| `/CHANGELOG.md` | **regenerated/scrubbed public changelog** — not the raw internal one (see O1) |

### 2.2 EXCLUDE (internal-only — never ships)

| Pattern | Why |
|---|---|
| `/design/*.md` (root-level only) | eval plans/reports, roadmaps, fix blueprints, `state.md` — internal |
| `/design/adr/**` (the **kit's own** ADRs, `adr-001`…`adr-052` + README + index) | **NEW — internal decision history.** Replaced in the public distribution by [`docs/architecture.md`](../docs/architecture.md). Root-anchored so it does **not** match `examples/projects/*/design/adr/**`, which still ship (those are illustrative example output, not the kit's governing ADRs). |
| `/design/prd-addenda/**` | internal PRD addenda |
| `/prompts/*` **except** `/prompts/_template.md` | all `issue-NNN-*.md` execution briefs are internal |
| `/notes/**` | internal working notes, audits, eval logs |
| `/archive/**` | historical framing; CLAUDE.md says "do not treat as current direction" — not public-ready |
| `/.hermes/**` | supervision artifacts (untracked anyway; belt-and-suspenders) |
| `/ai-review/artifacts/**`, `/ai-review/config.json` | generated/local (already gitignored) |
| editor/OS junk, SSH key material | already gitignored; export asserts absence |

**Root-anchoring is load-bearing.** `/design/*.md` and
`/design/prd-addenda/` must not match `examples/projects/*/design/...`.
Confirmed at risk: `examples/projects/phased-podcast-pipeline/design/adr/*`,
`.../design/build-out-plan.md`, `examples/projects/*/design/{prd,mvp}.md`
all legitimately ship.

### 2.3 TRANSFORM (rewrite on the way out)

1. **Repo-name rewrite** (root-anchored to text references, not blind):
   - `olivermorgan2/workflow-generator` → `olivermorgan2/claude-workflow-kit`
   - `takumi-omorgan/workflow-generator-takumi` → `olivermorgan2/claude-workflow-kit`
   - bare repo/dir forms in docs (`~/src/workflow-generator`, the
     `workflow-generator/` tree header in `docs/repo-structure.md`) →
     `claude-workflow-kit`
   - `WORKFLOW_KIT_REPO` default in `bin/bootstrap-workflow-kit` →
     `olivermorgan2/claude-workflow-kit`
   - **Example-project ADR bodies are exempt from blind rewrite** (they
     still ship, but as illustrative content) — see §6 / O5. The kit's
     **own** ADRs no longer ship, so the previous source-vs-export ADR
     name-rewrite dilemma is moot for them.

2. **ADR-reference neutralization (NEW — the cost of excluding `/design/adr/**`).**
   With the kit's ADRs no longer shipping, every reference into them from
   *shipping* content must be removed or transformed, or the markdown
   link checker (§5) fails on orphaned links. Measured scope in the
   current tree:

   | Reference kind | Where | Count | Treatment |
   |---|---|---|---|
   | **Markdown links** `](…/design/adr/adr-NNN-….md)` | `docs/**` (39), `skills/**` (38), `templates/**` (3) | **~80** | **Must transform** — these break the link checker. Replace the link with either (a) plain de-linked text (`ADR-NNN` → bare token or the decision restated inline), or (b) a single pointer to [`docs/architecture.md`](../docs/architecture.md). Default: de-link, keep surrounding prose. |
   | **Bare inline mentions** `(ADR-NNN)` / `per ADR-NNN` | `docs/**` + `skills/**` | **~75** | Do **not** break the link checker, but they are internal-history breadcrumbs. CLAUDE.md already discourages parenthetical ADR attributions in SKILL bodies. Strip the parenthetical (preferred) or leave as opaque tokens. Decide source-vs-export (O3/O5). |
   | **CHANGELOG.md** ADR mentions | `/CHANGELOG.md` | ~114 | Absorbed by the public-CHANGELOG regeneration (§2.1, O1) — the public changelog is generated/scrubbed, so raw ADR churn drops out anyway. |
   | **`kit.json` ADR references** | `/kit.json` (paths + inline `ADR-NNN`) | several | **Must update** — `kit.json` ships as public metadata. Remove or rewrite `design/adr/…` path values and inline `ADR-NNN` attributions so public metadata points at nothing private; re-run `validate-kit-json` / `check-consistency` after. |
   | README `ADR` / `design/adr` text | `/README.md` | a few (text, **no file links**) | No broken links; revise prose so it does not imply a shipped ADR set (point to `docs/architecture.md` instead). |

   **Preferred resolution:** neutralize at **source** (de-link / strip
   parentheticals; restate the few load-bearing decisions inline or in
   `docs/architecture.md`), so the export does file-subsetting + a final
   safety scan rather than carrying ~155 fragile per-file rewrites. This
   mirrors O3's correct-at-source recommendation and is enforceable by
   `check-consistency` + the link checker. Export-time-only rewriting
   remains the fallback if source edits are deferred.

3. **Version-pin rewrite (derive from the release tag, finding #6).**
   Every hardcoded `v3.3.0` in README/`docs/install.md`/bootstrap is
   replaced with the tag being published. The single source of truth is
   the release tag (which should equal `kit.json` `kitVersion`). The
   export refuses to run if `kit.json` `kitVersion` and the requested tag
   disagree (prevents the current 4.1.0-vs-3.3.0 drift from recurring).
   Preferred end-state: docs carry a single substitution token and the
   release stamps it, so there is exactly one place a version lives.

4. **Personal-path scrub.** Remove/neutralize `~/dotfiles/...`,
   `/Users/hermes/...`, and the dogfooding playbook pointer.

5. **Public CHANGELOG.** Generate from tagged releases (or scrub the
   internal one): apply the same name/version transforms and drop
   internal-issue churn that has no public meaning (O1).

---

## 3. Export / publish command design

Two surfaces, split because **building the artifact is safe but
publishing is identity-sensitive** (active `gh` auth is `takumi-omorgan`).

### 3.1 `bin/export-public` (build + validate; never pushes)

Standard-envelope `bin/` script (ADR-047 / `lib/json-envelope.sh`).

```
bin/export-public [--dest DIR] [--version vX.Y.Z] [--repo owner/name] [--format text|json]
```

Steps:
1. Resolve version (default: `kit.json` `kitVersion` → `vX.Y.Z`) and
   target repo (default `olivermorgan2/claude-workflow-kit`).
2. `git archive HEAD` into `DEST` (tracked files only).
3. Apply EXCLUDE rules (root-anchored prune).
4. Reduce `prompts/` to `_template.md`.
5. Apply TRANSFORM rules across text files.
6. Generate the public CHANGELOG.
7. Run all validation gates **from inside `DEST`** (§5).
8. Run leak checks (§5).
9. Emit an envelope summary (files included/excluded, transforms applied,
   gate results). Non-zero exit on any gate failure.

Default `DEST` is gitignored (`dist/public/` or a temp dir) so the
artifact never accidentally lands in the source history.

### 3.2 `bin/publish-public` (identity-gated push + release)

```
bin/publish-public --dest DIR --version vX.Y.Z [--repo owner/name] [--create]
```

Hard preconditions (abort with exit 3 / auth-service failure if unmet):
- `gh auth status` shows the **active** account == the target owner
  (`olivermorgan2`). It will **never** push to `olivermorgan2` while
  `takumi-omorgan` is active.
- `bin/export-public` validation passed for this `DEST`.

Steps (finding #9 ordering):
1. `--create`: create `olivermorgan2/claude-workflow-kit` (public).
2. Initialize the public tree as a fresh git history (squash to one
   "Initial public release vX.Y.Z" commit — the public repo does **not**
   inherit internal commit history) and push `main`.
3. Create the tag `vX.Y.Z` and a GitHub release.
4. Upload the `bootstrap-workflow-kit` asset to the release.
5. Only **after** the asset is live are the README `curl … releases/download/vX.Y.Z/bootstrap-workflow-kit` commands real.

A runbook lives at **`docs/publishing.md`** (kit-internal doc — itself
excluded from the public export, or kept; O4).

---

## 4. Public repo creation / auth plan

1. **Do not** create or push `olivermorgan2/claude-workflow-kit` while
   `gh` is authenticated as `takumi-omorgan`. (Current state:
   `takumi-omorgan` active, scopes `repo, workflow, read:org, gist`.)
2. User/Hermes switches identity first:
   - `gh auth login` (or `gh auth switch -u olivermorgan2`) → confirm
     with `gh auth status` that `olivermorgan2` is the **active** account.
3. `bin/publish-public --create` asserts the active account and aborts
   otherwise — auth identity is checked in code, not just by convention.
4. Source repo's `origin` stays `takumi-omorgan/...`. The public repo is
   pushed via an explicit remote/URL inside `bin/publish-public`, not via
   the source repo's `origin`.

---

## 5. Validation gates and failure conditions

All run **inside the exported tree** (`DEST`), proving the *shipped*
artifact is coherent — not the source. Any non-zero result aborts the
export; publish is blocked until export is clean.

| Gate | Catches |
|---|---|
| `./bin/validate-kit-json` | kit.json ↔ skill frontmatter drift |
| `./bin/check-consistency` | docs ↔ metadata drift (skills, verb layer, bin registry, schemas, permission legend) |
| `./bin/self-test` | non-mutating validation surface + install stub |
| `./bin/check-install-render` | target-project install render stays coherent |
| `./bin/review-eval` | AI-review offline eval + duplicate-publish guard |
| **markdown relative-link check** (new) | links pointing at *excluded* files — the gate that proves exclusions didn't orphan a reference (e.g. a doc/skill linking to an excluded **`design/adr/adr-NNN-*.md`**, a `design/` root report, or a `prompts/issue-*`). This is the primary gate proving the **~80 ADR links** were neutralized (§2.3). |
| **leak scan** (new) | see below |

**Leak scan — fail if any of these appear in `DEST`:**
- old name forms: `workflow-generator` (bare), `olivermorgan2/workflow-generator`, `takumi-omorgan`, `workflow-generator-takumi`
- stale version literals (e.g. `v3.3.0` when tag is `vX.Y.Z`)
- absolute/personal paths: `/Users/hermes`, `~/dotfiles`, `~/src/workflow-generator`
- internal paths: `design/prd-addenda`, `notes/`, `archive/`, root `design/*.md` report names, `prompts/issue-`
- **the kit's own ADR tree: presence of `/design/adr/` (excluded) and any *link* into it from shipping content** (`](…/design/adr/…)`)
- any `prompts/*` file other than `_template.md`
- presence of `.hermes/`, `ai-review/config.json`, `ai-review/artifacts/`

**Allowlist (load-bearing under the new decision):** `examples/projects/*/design/adr/**`
legitimately ship and legitimately *contain* the strings `design/adr` and
`ADR-NNN` — they are illustrative example output. The leak scan and the
ADR-link rule must be **root-anchored to the kit's own `/design/adr/`**
and must not fire on the example projects' ADR trees. (Bare `ADR-NNN`
*tokens* that survive as opaque text in prose are not a leak by
themselves — only links into the excluded kit ADR tree are.)

---

## 6. Handling `design/adr/` (REVISED — ADRs are internal-only)

**Decision (supersedes the original §6).** The kit's own ADRs
(`adr-001`…`adr-052` + README + index) are **real, accepted, and
substantive — and they stay internal.** They are the kit's private
decision history: *why* past choices were made. The public distribution
does **not** need that history to be installed, run, or extended, so it
ships a single current architecture statement —
[`docs/architecture.md`](../docs/architecture.md) — instead. That doc
explicitly says detailed ADR history is maintained internally and is not
part of the public distribution.

This reverses the earlier "include `/design/adr/**` in full" position.
The two-repo model (§1) already keeps the source repo as the home for all
internal material; the ADRs simply join the eval reports, roadmaps, and
superseded designs on the internal side of that boundary.

### 6.1 Why exclude rather than ship-and-prune

Shipping all 52 ADRs would publish the kit's entire deliberation history —
including superseded and reversed decisions — as if it were current
guidance, which is exactly the "history of the kit" framing
`docs/architecture.md` is meant to replace. One concise current doc is
more useful to a public consumer than 52 records they must reconcile.

### 6.2 Known implementation cost (accounted for)

Excluding the kit ADRs orphans every reference into them from shipping
content. Measured in the current tree and itemized in §2.3:

- **~80 markdown links** (`docs/**` 39, `skills/**` 38, `templates/**` 3)
  into `design/adr/adr-NNN-*.md` — **these break the markdown link
  checker** and are the must-fix set. Treatment: de-link to plain text or
  repoint to `docs/architecture.md`.
- **~75 bare `(ADR-NNN)` mentions** in `docs/**` + `skills/**` — not
  link-breaking, but internal breadcrumbs; CLAUDE.md already discourages
  these in SKILL bodies. Strip or leave as opaque tokens.
- **`kit.json`** public metadata contains `design/adr/…` path values and
  inline `ADR-NNN` attributions — rewrite/remove, then re-run
  `validate-kit-json` and `check-consistency`.
- **CHANGELOG.md** ADR churn is absorbed by public-changelog regeneration
  (O1).
- **README.md** has ADR *text* (no file links) — revise prose to point at
  `docs/architecture.md`, not a shipped ADR set.

### 6.3 Source vs. export, and the example-project exemption

Per O3/O5, the recommendation is to **neutralize at source** (de-link,
strip parentheticals, restate the few load-bearing decisions inline or in
`docs/architecture.md`) so the export is subset-plus-safety-scan rather
than ~155 fragile per-file rewrites. `check-consistency` and the link
checker then enforce coherence permanently, not just at export time.

**Do not touch the kit's ADR files themselves** — they remain immutable
internal records (CLAUDE.md); ADR-044 mechanical rewrites are no longer
needed for them since they don't ship. The earlier old-repo-name concern
inside ADR bodies is moot for the public artifact.

**Example-project ADRs still ship.** `examples/projects/*/design/adr/**`
are illustrative output of the kit (what a *user's* project produces), not
the kit's governing ADRs. They are INCLUDED (§2.1), and the leak
scan/link rule is root-anchored to the kit's own `/design/adr/` so it does
not fire on them (§5).

### 6.4 Future opt-in promotion

If a specific ADR turns out to be genuinely useful public reference, it
can be **explicitly selected** into the public set later (copied/curated,
not bulk-shipped). The default remains: ADRs are internal.

---

## 7. Open questions (need a user decision)

- **O1 — Public CHANGELOG:** ~~generate fresh from tagged releases, or
  scrub the existing 20 KB internal CHANGELOG?~~ **RESOLVED ([ADR-055](adr/adr-055-public-distribution-versioning-policy.md)):**
  curated public changelog **generated from tagged releases**, beginning at
  the first public release; the raw internal changelog is not shipped
  verbatim and private development history is not reproduced publicly.
- **O2 — First public version:** ~~`kit.json` is `4.1.0` but docs pin
  `3.3.0`. Is the first public tag `v4.1.0` (align to kit.json), or do we
  debut the public repo at `v1.0.0`/`v0.1.0`?~~ **RESOLVED ([ADR-055](adr/adr-055-public-distribution-versioning-policy.md)):**
  align to `kit.json` `kitVersion` — first public tag = current `kitVersion`
  (`v4.1.0` today), one version line, `tag == kitVersion` enforced at export.
  Not a fresh `v1.0.0` (which would collide with the existing `v1.0.0…v4.0.0`
  internal tag history). Correcting the stale `v3.3.0` doc pins is issue #16's
  source-neutralization sweep, not a policy question.
- **O3 — Correct-at-source vs export-only:** fix the repo name + version
  drift in the **source** repo (a real bug — kit.json/docs disagree), and
  let the export do only file-subsetting + a final safety rewrite? Or
  apply all transforms only at export time? *Recommend: correct name +
  versioning in source; subset + safety-scan at export.*
- **O4 — Internal-describing docs:** `docs/repo-structure.md` (and a few
  others) describe `notes/`/`archive/` which won't exist publicly, **and
  now describe the kit's `design/adr/` as a shipped "governing ADR" set
  that no longer ships** — that prose must be revised to match the new
  decision (point at `docs/architecture.md`). `CLAUDE.md` also carries a
  personal dogfooding section. Transform these for the public artifact, or
  restructure the source so public-facing docs describe only public dirs?
  Also: does `docs/publishing.md` ship or stay internal?
- **O5 — ADR-reference neutralization, source vs export (was: ADR name
  handling).** Now that the kit ADRs are excluded (§6), the residual
  choice is *where* the ~80 orphaned links + ~75 bare mentions + `kit.json`
  references get neutralized: at **source** (permanent, enforced by
  `check-consistency`/link-checker) or **export-only** (subset stays
  pristine, but ~155 transforms run every publish). *Recommend: source —
  consistent with O3; restate any load-bearing decision in
  `docs/architecture.md` so no information is lost.*
- **O6 — Where this design lives long-term:** this draft is at
  `design/public-distribution-export-design-20260609.md`. **Note:** the ADR
  number this draft originally reserved (`ADR-053`) was assigned to the
  architecture-document decision before this work landed. The
  versioning/changelog policy is now recorded as
  [ADR-055](adr/adr-055-public-distribution-versioning-policy.md); the
  two-repo **export-model** decision will be filed under its own next-free
  number when issue #16 lands.

---

## 8. Recommended next action

1. **Approve** this design and resolve the remaining open questions.
   **O1 (changelog) and O2 (version) are RESOLVED** in
   [ADR-055](adr/adr-055-public-distribution-versioning-policy.md) (issue
   #17); O3–O5 (correct-at-source, internal-describing docs, ADR-reference
   neutralization) are the substance of issue #16.
2. Open a tracked issue + write the **two-repo public distribution export**
   ADR (its own next-free number — *not* `ADR-053`, which is now the
   architecture-document decision) — and record the **ADR-exclusion /
   `docs/architecture.md`** decision (folded into that ADR or as its own).
3. Implement, in order:
   a. source correction (name + tag-derived versioning),
   b. **ADR-reference neutralization** (§2.3 item 2 / §6.2): de-link the
      ~80 `design/adr/` links in `docs/**` + `skills/**` + `templates/**`,
      strip/neutralize the ~75 bare mentions, scrub `kit.json` ADR
      references, revise `docs/repo-structure.md` + README prose (O4),
      then re-run `validate-kit-json` + `check-consistency` + the link
      checker,
   c. confirm `docs/architecture.md` is present and link-clean (ships; must
      not itself link into `design/adr/`),
   d. `bin/export-public` + leak scan + markdown-link check (root-anchored
      to exclude the kit's `/design/adr/` while keeping example-project
      ADRs),
   e. `docs/publishing.md` runbook,
   f. `bin/publish-public` (identity-gated).
4. Run `bin/export-public` **dry-run**; review the leak/link report.
5. **User switches `gh` auth to `olivermorgan2`**, then
   `bin/publish-public --create` → push, tag, release, upload bootstrap
   asset.
6. Verify the README `curl` one-liner end-to-end against the live release.
