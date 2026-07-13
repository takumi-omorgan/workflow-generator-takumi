# ADR-057: Public export integrity gate

**Status:** accepted
**Date:** 2026-07-08

## Context

[ADR-056](adr-056-two-repo-public-distribution-export-model.md) makes the
public distribution a deterministic function of the source tree at `HEAD`:
`bin/export-public` builds the artifact, `bin/check-public-export` asserts
the public contract over it (checks A–I: top-level allowlist, excluded
private paths absent, required artifacts present, no link into an excluded
path, no stale owner/repo strings, no personal paths, no stale version pin,
curated changelog, no private dogfooding section), and `bin/export-eval`
exercises that contract offline on every change via `bin/self-test`.

That machinery proves a **local staging tree** is clean. It stops there by
design: ADR-056 Decision 1 states the export "performs **no** `git push`,
repo creation, release, or auth switch", and
[`docs/publishing.md`](../../docs/publishing.md) makes publishing a manual,
identity-gated human sequence — switch `gh` auth to the public owner, push
the verified `dist/` tree as a fresh history, tag `v<kitVersion>`, cut the
release, upload the bootstrap asset.

The consequence is a seam. The tree we **verify** (`dist/`, local) and the
tree that is **live** on the public remote are two separately derived
artifacts, and nothing asserts they are the same one. Every leg of the
export contract is machine-checked except the last: *what is actually
published is what we verified*. A hand-push, a partial or wrong-branch push,
a stale re-export from an older `HEAD`, or a hotfix committed directly on the
public remote would all pass every gate the kit has today.

**This is a latent gap, not an active defect.** A manual audit performed on
2026-07-13 against the published repo (`olivermorgan2/claude-workflow-kit`) at
its then-current HEAD — commit `1c0eba3`, itself dated 2026-06-29 — confirms
the export contract *is* being honoured: the published file set is exactly
what `bin/export-public`
produces from source today — no extra files, none missing; no excluded path
(`archive/`, `notes/`, root `design/`, `.hermes/`) is present; `prompts/` is
reduced to `_template.md`; the `CLAUDE.md` contributor section is stripped;
and the install-surface identity strings (`README.md`, `docs/install.md`,
`bin/bootstrap-workflow-kit`) all name the repo they ship in. The
export-time identity rewrite and leak prune are working as ADR-056 specified.

So the argument for this ADR is not "the published repo is broken". It is
that the *only* reason we know it is not broken is that a human went and
looked — a one-off audit, unrepeatable at release cadence. Comparing a
published tree against an export artifact is work where two competent runs
must produce byte-identical output, which is precisely what
[ADR-054](adr-054-script-vs-skill-boundary.md)'s decision rule classifies as
a deterministic script rather than human judgment. We are optimising for a
published artifact whose compliance is a *checked invariant* rather than an
intention that has so far held.

## Options considered

### Option A: Rely on pre-publish verification plus care at publish time (status quo)

- Pros: nothing to build or keep green; the contract has held in practice —
  the 2026-07-13 audit found the published tree fully compliant; the publish
  step is rare and performed deliberately by one person.
- Cons: leaves the last leg of the export contract as the only one not
  machine-checked; proves a local tree clean while saying nothing about the
  remote; detection of a bad publish depends on someone happening to look
  again; contradicts the kit's own script-the-spine boundary
  ([ADR-054](adr-054-script-vs-skill-boundary.md)), which is the credibility
  the kit sells.

### Option B: Add a post-publish verification gate (`bin/verify-published`)

Add a source-only script that fetches the public remote at the published tag,
compares it against the artifact `bin/export-public` produces from `HEAD`, and
re-runs the ADR-056 contract checks against the **fetched** tree. Publishing is
not complete until it passes.

- Pros: closes the seam with a script rather than a habit; reuses the existing
  verifier and its check set rather than inventing a second contract; makes
  "what is published is what we verified" a checked invariant; turns the
  one-off manual audit into a repeatable command; makes drift on the public
  remote detectable rather than merely unlikely.
- Cons: one more script and fixture set to keep green; introduces the kit's
  first network-dependent check, which must be kept out of the offline
  `bin/self-test` path; verifies the remote at a point in time, so it detects
  post-publish drift only when re-run.

### Option C: Automate the push inside `bin/export-public`

Let the export itself create the commit, push, tag, and release, so the
verified tree is the only thing that can reach the remote.

- Pros: closes the gap by construction — a divergent tree cannot be published
  because no human hand is in the publish path.
- Cons: reverses ADR-056 Decision 1 and its identity-gating rationale — the
  build tool would need public-owner credentials, making a script that runs in
  CI capable of publishing; it would require a superseding ADR, not this one;
  and it still cannot detect drift introduced *after* the push (a direct commit
  on the public remote), so a verifier is wanted anyway.

## Decision

Adopt **Option B**. Publishing is not complete until the public remote is
proven to match the artifact the export produced.

1. **`bin/verify-published`** — a new source-repo-only script. Given
   `--version vX.Y.Z` (default: `kit.json` `kitVersion`) and a public remote
   (default: the public-repo constant already in `bin/lib/export_paths.py`),
   it:
   - builds the expected artifact by running the existing `bin/export-public`
     into a temporary staging dir — the artifact stays a deterministic
     function of `HEAD`, not a second re-implementation of the contract;
   - fetches the public remote's tree at tag `vX.Y.Z`;
   - asserts **file-set equality** (no extra, no missing) and **content
     equality** (per-file digest) between the two trees, naming every
     offending path individually;
   - re-runs `bin/check-public-export` against the **fetched** tree, so
     checks A–I hold on what is actually published, not only on what was
     staged locally;
   - asserts the published tag resolves to the remote default branch's HEAD,
     that the fetched `kit.json` `kitVersion` equals the tag (the ADR-055
     `tag == kitVersion` invariant, re-checked on the remote), and that the
     release and its bootstrap asset exist at that tag.

   The tag-resolves-to-default-branch-HEAD assertion derives from the *current*
   publish model in `docs/publishing.md` (the verified tree is pushed as the
   default branch's fresh history), not from an invariant ADR-056 states. If the
   publish model ever gains release branches, that assertion must be revised in
   tandem.

2. **It is the final step of a public release.** `docs/publishing.md`'s
   "After a clean export" sequence gains it as step 4, and the `/release`
   public shape does not consider a release done — nor announce it — until
   `verify-published` exits `0`.

3. **Network policy.** This is the kit's first check that requires network,
   so it stays off the offline path: `bin/verify-published` is **not** wired
   into `bin/self-test`, which remains fully offline (ADR-056 Decision 5). An
   unreachable remote is reported as a distinct "could not verify" status —
   advisory during local development, **blocking** in the release flow. Its
   comparison and diff-reporting logic is covered by offline golden fixtures
   under the existing `bin/export-eval` pattern, so the logic itself is
   exercised on every change without a network call.

4. **A failed verification is an incident, not a warning.** It means the
   public remote holds something the export did not produce. The response is
   to republish from a clean export and record the divergence in
   `knowledge/log.md` — not to amend the check.

## Consequences

- The last unchecked leg of the ADR-056 export contract becomes machine-
  verified. "What is published is what we verified" moves from human care to
  a script, which is where ADR-054's decision rule puts it.
- The *mechanical* part of the manual audit that currently underwrites
  confidence in the published tree — tree equality, excluded-path absence,
  identity strings, version pin — becomes a repeatable command, so future
  releases do not need a human to re-derive it by hand. Holistic "does this
  read right to a newcomer" judgment is not automated by this and remains a
  human review concern.
- The public release flow gains a network-dependent final step; a failed
  verification blocks the announcement. Offline development is unaffected —
  `bin/self-test` stays offline and green without network.
- Direct pushes or commits to the public remote outside the export pipeline
  become detectable, and are treated as incidents rather than absorbed
  silently.
- One more source-only script plus fixtures to keep green. It is pruned from
  the public artifact along with the rest of the export tooling, with the
  `kit.json` / `bin/self-test` / `docs/README.md` reconciliation that
  [ADR-056](adr-056-two-repo-public-distribution-export-model.md) Decision 6
  already specifies for exactly this class of script.
- **Out of scope: parametrising the export's identity rewrite** (e.g. a
  `--public-repo=OWNER/NAME` flag for forks). ADR-056's TRANSFORM rules
  already rewrite owner/repo references to the public repo name and check E
  asserts none of the old strings survive; the published tree confirms both
  work. There is no defect motivating that work, and fork support is its own
  decision if it is ever wanted.
- **Threat model: accidental divergence, not adversarial tampering.** The
  comparison is a filesystem-level digest match against a locally rebuilt
  artifact. It catches a bad, stale, partial, or hand-made publish. It is not
  a cryptographic supply-chain guarantee, and accepting this ADR should not be
  read as closing that question. Signing/checksumming the bootstrap release
  asset stays deferred — tracked separately under ADR-055's versioning policy,
  not this ADR.
