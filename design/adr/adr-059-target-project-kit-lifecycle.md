# ADR-059: Target-project kit lifecycle — upgrade, doctor, uninstall

**Status:** accepted
**Date:** 2026-07-14
<!-- Redraft. The first draft of this ADR was HALTED before review on
     2026-07-14 (knowledge/reviews/2026-07-14-adr-059-halt.md, issue #55):
     its Decision rested on a premise that verification falsified — that
     the receipt layer already records what the installer wrote. It does
     not. Oliver ruled Option A of the halt note's option space (issue #55,
     operator attestation). This redraft replaces that draft wholesale.
     It supersedes no accepted ADR. -->

## Context

The installer (ADR-009, ADR-029) covers day zero: a pinned-version,
idempotent install into a fresh project. Nothing covers day thirty. A
target project on kit v5.0 has no supported path to v5.2: skills under
`.claude/skills/` go stale, generated files drift from the templates they
came from, and `bin/` helpers that newer skills reference may be absent.
There is no health check inside a target project — `bin/self-test` exists
only for the kit repo itself (ADR-050) — and no uninstall, which makes
trying the kit feel like a one-way door.

Upgrade is the hard case, because installed material bifurcates: files the
kit owns and may safely replace, and files the user owns (or has edited)
which must never be clobbered. Answering "may I replace this file?"
requires two facts: **who owns it**, and **has it changed since we wrote
it**.

### What actually exists today

The first draft of this ADR asserted that the receipt layer
(`bin/write-receipt`) "already records what the installer wrote and at
which version." That is false, and the Decision it carried has been
withdrawn. The verified position, stated plainly:

**Nothing in a target project records what the installer wrote.** There is
no install ledger, manifest, or lockfile of any kind. Specifically:

1. **The installer writes no receipt.** `write-receipt` appears exactly
   once in `bin/install-workflow-kit`, at line 410 — inside a copy loop
   (`for script in review-pr publish-review review-eval write-receipt`)
   that is itself gated on `--with-ai-review` (line 406). It *copies the
   script* into the target's `.claude/bin/`, and only when AI review is
   requested. It never invokes it. No installer code path writes a
   receipt.
2. **The receipt schema cannot express file ownership.**
   `schemas/receipt.v1.yaml` is keyed by **work unit**, not by file: its
   required fields are `schema, version, skill, key, status, timestamp`,
   where `key` is "an issue number, a PR number, a milestone slug, or a
   release tag." There is no path list, no per-file version, and no hash.
   "Unmodified since install" is not a question this schema can answer.
3. **Receipts do not survive a clone.** They are gitignored in target
   projects — `templates/gitignore.target:22` (`.claude/receipts/`), with
   the reason stated at lines 20–21: "local per-run state, not committed
   artefacts." A fresh clone of a target project has **zero** receipts, so
   any lifecycle command built on them would have nothing to read.
4. **No lifecycle code exists.** There is no `doctor`, `upgrade`, or
   `uninstall` in `bin/` or `skills/`, and nothing in the repo references
   one. This ADR decides a greenfield surface.

ADR-050 (accepted; `design/adr/adr-050-reliability-validation-self-test.md:3`)
is explicit about what receipts are *for*: idempotency for mutating skills —
"the actions you cannot simply re-run." Cat-1 file-writing skills
deliberately do not write them, "their outputs are already idempotent." A
durable, committed, file-keyed ownership ledger is the opposite kind of
artifact, and asking receipts to become one would contradict an accepted
decision.

### What ADR-061 gives us, and what it deliberately does not

ADR-061 (accepted; `design/adr/adr-061-runtime-asset-manifest.md:3`)
decides a kit-side declarative manifest, `runtime-assets.md`, parsed by
`bin/list-runtime-assets`: one row per asset carrying id, source path,
install destination, required/optional, profiles, **ownership class**, and
since-version. It is authoritative for "installation and ownership
decisions." It names "the ADR-059 upgrade planner" among its consumers,
and it settles the ownership vocabulary **there, not here**: the closed set
is `kit-owned | generated | user-seeded`, and ADR-059 "adopts this
taxonomy."

ADR-061 is **decided, not built**: neither `runtime-assets.md` nor
`bin/list-runtime-assets` exists in the tree today. This ADR depends on
ADR-061's *decision*, and claims nothing about tooling that has not
shipped.

Crucially, ADR-061 draws its own boundary: the manifest declares what
*should* be installed. A target-side record of what *was* written is
outside its scope. That record is the gap this ADR fills.

A note on one line of ADR-061's Context, so it is not mistaken for
evidence: it contrasts receipts ("record what *was* written") with the
manifest ("declares what *should* be"). Read as a claim about target
projects today, that overstates receipts — as §1–3 above establish, no
receipt records an installer write at all. ADR-061's *Decision* does not
rest on the line (it decides the manifest, not the receipt layer), so
nothing in ADR-061 needs revisiting. But this ADR does not inherit it as a
citation. The gap it gestures at is real; the artifact it names is not.

We are optimising for: no clobbered user edits, a legible diff before
anything changes, offline operation, and reversibility.

## Options considered

### Option A: Document manual re-install as the upgrade path

- Pros: nothing to build.
- Cons: a wholesale re-install cannot distinguish kit-owned from
  user-edited files. Users either skip upgrades (staleness) or lose edits
  (worse). This is the status quo, and it is why the ADR exists.

### Option B: Receipt-driven lifecycle — build on `bin/write-receipt`

The original draft's decision. **Rejected on verified fact**, not on
taste: receipts are not written by the installer, are gitignored, and are
work-unit-keyed with no path, version, or hash (Context §1–3). Rescuing
this option means making receipts committed and file-inventoried — which
contradicts **accepted** ADR-050, whose receipts serve a different job
(idempotency for hard-to-reverse mutations), and would require a
superseding ADR first. Superseding a correct decision to borrow its
filename is a bad trade.

### Option C: Committed install ledger, composed with the ADR-061 manifest

The installer writes a committed, file-keyed, hashed, version-stamped
ledger into the target: `.claude/kit-lock.json`. Lifecycle commands read
**manifest + ledger**:

- **Manifest** (kit-side, ADR-061) — what *should* be installed, who owns
  it.
- **Ledger** (target-side, this ADR) — what *was* written, at which kit
  version, with which content hash.

- Pros: makes "unmodified since install" a decidable question, which is
  the one fact upgrade cannot proceed without; survives `git clone`;
  works offline; leaves ADR-050 untouched; reuses ADR-061's ownership
  column rather than inventing a rival taxonomy; needs no new runtime
  dependency.
- Cons: a new committed artifact in target projects, and a schema to
  version; the installer gains a write it did not have. Accepted: the
  alternative is guessing at ownership, which is precisely the failure
  mode this ADR exists to prevent.

### Option D: No ledger — fetch the pinned old kit version at upgrade time and diff

Reconstruct "what we wrote" by fetching the version recorded somewhere and
comparing file-by-file.

- Pros: no new committed artifact.
- Cons: makes upgrade and doctor **network-dependent** — they cannot run
  offline or in a sandboxed CI environment. And it still cannot separate
  "the user edited this" from "an older kit shipped a different file"
  without exact per-file provenance — which is the ledger, arrived at by a
  slower road.

### Option E: Vendored subtree (kit as git subtree/submodule)

- Pros: git-native updates and diffs.
- Cons: submodule/subtree ergonomics are hostile to this kit's audience;
  conflates kit history with project history; does nothing for
  generated-file drift.

### Option F: Split this ADR — ship `doctor` now, defer `upgrade`

- Pros: a read-only doctor could ship against the manifest alone.
- Cons: a doctor without the ledger cannot answer "modified since
  install" — the headline drift check, and the main reason to run it.
  `uninstall` needs the ledger too (what is safe to remove). The ledger
  decision must be made regardless; one ADR with a staged rollout is
  cheaper than two ADRs and a later amendment. **The correct instinct here
  is kept as implementation ordering** (see Consequences), not as a split.

## Decision

**Option C.** The installer writes a committed install ledger,
`.claude/kit-lock.json`, in the target project. `upgrade`, `doctor`, and
`uninstall` are built on **manifest (ADR-061) + ledger (this ADR)**. The
receipt layer is not involved.

### The ledger is committed, and needs no gitignore change

The target `.gitignore` template already commits `.claude/` with three
exceptions — `templates/gitignore.target:18-22`: `.claude/worktrees/`,
`.claude/settings.local.json`, and `.claude/receipts/`. Its comment at
line 17 makes the intent explicit: ".claude/skills/ is NOT ignored —
that's where the installed kit lives." `.claude/kit-lock.json` therefore
commits by default, with **no change to the ignore template**. Surviving
`git clone` is the property receipts lack and the ledger's whole purpose
requires.

### Ledger shape

Top level: `schema` (literal `kit-lock`), `version` (integer, 1),
`kitVersion` (the installing kit's version — the kit already declares one
at `kit.json:3`, currently `5.0.1`), `installedAt` (ISO 8601 UTC),
`profile`, and `assets`.

Per asset: `id` (the ADR-061 manifest's stable asset ID), `dest` (path
relative to the project root, as written), `ownership` (ADR-061's
class, recorded at write time), `sha256`, `provenance`, and `since` (the
manifest's since-version column).

```json
{
  "schema": "kit-lock",
  "version": 1,
  "kitVersion": "5.0.1",
  "installedAt": "2026-07-14T09:12:00Z",
  "profile": "full",
  "assets": [
    {
      "id": "skill-prepare-issue",
      "dest": ".claude/skills/prepare-issue/SKILL.md",
      "ownership": "kit-owned",
      "sha256": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
      "provenance": "installed",
      "since": "5.0.0"
    },
    {
      "id": "template-state",
      "dest": "design/state.md",
      "ownership": "generated",
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "provenance": "installed",
      "since": "5.0.0"
    }
  ]
}
```

#### `sha256` means one thing only, and `provenance` guards it

`sha256` records **the bytes the kit itself wrote**. It is never a record
of "whatever happened to be on disk." This distinction is the ledger's
entire load-bearing property: `replace` is authorised by hash equality, so
if bytes the kit did *not* write could ever enter the `sha256` field, a
later upgrade would read them as proof of kit provenance and overwrite
user work — reintroducing, one layer up, the exact clobbering this ADR
exists to prevent.

Because a degraded run (below) may need to record a file it did not write,
`provenance` is a required per-asset field with a closed vocabulary:

- **`installed`** — the kit wrote these exact bytes. The hash is evidence.
- **`adopted`** — the entry describes a file found on disk that the kit did
  **not** write (a pre-ledger install, or a file the operator chose to
  keep). The hash records *what is there*, and is explicitly **not**
  evidence of kit provenance.

**An `adopted` entry is never eligible for `replace`.** It is always
*skip + diff*. It converts to `installed` only when the operator accepts a
kit version for that file and the kit actually writes those bytes. There
is no other path from `adopted` to `installed` — provenance is earned by
being written, never by being observed.

Constraints that keep this honest:

- **`ownership` uses ADR-061's closed vocabulary verbatim** —
  `kit-owned | generated | user-seeded`. This ADR **adopts** it and does
  not extend or reinterpret it. Needing a different taxonomy (splitting
  `generated`, say) would be a superseding ADR against ADR-061, not a
  silent redefinition here.
- **`profile` is `full`.** ADR-061 fixes the valid profile set at exactly
  `{ full }` and validates it as a closed vocabulary. The field exists so
  the ledger records *which* profile produced this install; it is
  forward-compatible with ADR-060, but `ship-loop` becomes a legal value
  only if and when ADR-060 is accepted and amends ADR-061's column
  vocabulary. This ADR does not extend it.
- **`since` is informational.** ADR-061 states its since-version column is
  "informational and explicitly not validated" and that "nothing may
  branch on it." The ledger carries it for human legibility only. **No
  lifecycle command branches on `since`** — classification uses
  `ownership` and `sha256`, never version arithmetic.
- **`id` is the manifest's ID**, so the ledger joins to the manifest on a
  stable key rather than on a path that a later kit version may move.
- **The ledger does not describe itself**, and it does not list the
  manifest or its parser. Per ADR-061 those "ship in the kit tree the
  installer runs *from*, never as installed assets." The ledger records
  installed assets only.

### Who writes and reads it

- **Installer** — derives its write-list from `bin/list-runtime-assets`
  (per ADR-061) and writes the ledger as its final step, hashing each file
  as written.
- **`upgrade`** — reads it, computes a plan, rewrites it on success.
- **`doctor`** and **`uninstall`** — read it; never write it.

### Upgrade classification

The plan is computed by joining manifest rows to ledger entries on `id`,
and is presented in full **before** anything is written.

**Ownership is read from the current manifest, never from the ledger.**
The ledger's recorded `ownership` is informational (it says what the class
was when the file was written). If a later kit version reclassifies an
asset — say `kit-owned` becomes `generated` — the new manifest wins, and
the asset immediately becomes untouchable. This follows from ADR-061 being
authoritative for "installation and ownership decisions," and it fails
safe: reclassification can only ever *remove* the kit's licence to write,
never grant one.

For `ownership` = `generated` or `user-seeded`, there is exactly one
outcome — **never touch**, regardless of hash, ledger, or provenance. If
such a file is *absent*, upgrade reports it and may create it only with
explicit operator approval (creating an absent file clobbers nothing).

For `ownership` = `kit-owned`:

| Ledger entry | Manifest | On disk | Outcome |
|---|---|---|---|
| `installed`, hash matches disk | present | present | **replace** — the kit wrote these bytes and they are unchanged |
| `installed`, hash differs | present | present | **skip + diff** — locally modified; emit the diff, operator decides |
| `adopted` (any hash) | present | present | **skip + diff** — provenance unverified; never auto-replace |
| any | present | absent | **restore** — nothing to clobber |
| **none** | present | **present** | **skip + diff** — unknown provenance; never overwrite a file we cannot vouch for |
| **none** | present | absent | **install** — new asset; nothing to clobber |
| `installed`, hash matches | absent | present | **remove** — asset dropped from the kit, and we wrote it |
| `adopted`, or hash differs | absent | present | **leave + report** — never delete work we cannot vouch for |

Two invariants make clobbering structurally impossible rather than merely
unlikely:

1. **A file is overwritten only against a hash the kit itself wrote.**
   `installed` + hash equality is the *only* evidence accepted for
   "unmodified since install."
2. **Absence of evidence is never evidence of absence.** A file present on
   disk with no ledger entry, or with an `adopted` one, is *skip + diff* —
   not *install*. The permissive reading ("no entry, so nothing to lose")
   is exactly the reasoning that clobbers a pre-ledger project's work.

### Missing ledger — conservative degradation

Installs predating the ledger exist, and a user may delete the file. A
missing ledger is never treated as "nothing was installed." Note that no
special-case logic is required: a missing ledger is simply the case where
*every* asset has **no ledger entry**, and the table above already gives
the safe answer for that — every file present on disk is *skip + diff*,
and only genuinely absent files are installed.

- **`doctor`** — reports **unknown provenance** for every kit file. It can
  still check the manifest against disk (present / absent) but must not
  claim any file is unmodified.
- **`upgrade`** — replaces nothing automatically; the operator resolves
  every existing file from its diff.
- **`uninstall`** — **refuses**, unless given an explicit override flag,
  because it cannot distinguish kit files from user files and deletion is
  irreversible. The override is scoped to this case and is not a general
  bypass: with a ledger present, uninstall is always governed by it.

**The fresh ledger a degraded upgrade writes must not launder unknown
files into trusted provenance.** This is the sharp edge of the whole
design. When such an upgrade finishes, it records, per asset:

- files whose new kit version the operator **accepted** — the kit wrote
  those exact bytes, so `provenance: installed`;
- files the operator **kept** (declining replacement) — the kit did **not**
  write those bytes, so `provenance: adopted`.

Provenance **carries forward**; it is not re-earned each run. An entry
already marked `installed` whose file still hash-matches stays `installed`
even if this run did not rewrite it — the kit did write those bytes, and
that fact does not expire because a later upgrade had nothing to do. The
rule is simply: `installed` iff the kit wrote the bytes now on disk (in
this run or a previous one, evidenced by an unbroken hash), else
`adopted`.

A naive "record what is on disk" would stamp the operator's own edits with
`installed` and hand the *next* upgrade a hash it would read as proof the
kit wrote them — auto-clobbering user work on the following run, while
reporting it as a safe replace. `provenance` exists precisely to make that
outcome unrepresentable.

### ADR-050 is not superseded

**Receipts are unchanged.** They remain what ADR-050 accepted: gitignored,
per-run, work-unit-keyed idempotency artifacts under `.claude/receipts/`,
written by mutating skills so a resuming run does not repeat a
hard-to-reverse action (an issue, a PR, a milestone, a release).
ADR-050's deferred follow-ups — including shipping `write-receipt` into
target projects — stay exactly as deferred as they were.

The kit-lock ledger is a **different artifact for a different job**:
committed rather than local, file-keyed rather than work-unit-keyed,
provenance rather than idempotency. This ADR **stops depending on
receipts** rather than redefining them, which is precisely why no
superseding ADR is required. Nothing here edits, contradicts, or
reinterprets ADR-050.

### No new runtime dependency — stated precisely

The house rule is that a new runtime dependency requires its own ADR, so
this claim has to be exact rather than convenient.

- **JSON writing adds nothing.** The ledger is a flat structure — strings,
  one array of objects with fixed scalar fields, all drawn from paths,
  hex digests, versions, timestamps, and closed vocabularies. It is
  emitted with `printf` from the installer's existing bash. This is
  deliberate: the installer treats `python3` as **optional**, using it for
  placeholder substitution only when present and falling back to `sed`
  otherwise (`bin/install-workflow-kit:623`, "Use Python if available …
  otherwise fall back to portable sed"). A ledger writer that *required*
  `python3` would quietly promote an optional dependency to a hard one.
  It does not.
- **Hashing needs a hasher.** `sha256sum` and `shasum -a 256` are both
  present on the supported platforms, and either satisfies it. This is the
  one genuinely new requirement, so it is stated rather than glossed: if
  **neither** is available, the install **fails loudly** rather than
  writing a ledger whose hashes it cannot compute. A ledger the kit cannot
  vouch for is worse than no ledger, because the table above trusts it.

## Consequences

- **Implementation is staged, and the order is load-bearing.** Each step
  depends on the one before it:
  1. **ADR-061 first** — `runtime-assets.md` and `bin/list-runtime-assets`
     must exist. They do not today; everything below is blocked on them.
  2. **Installer ledger writer** — the installer derives its write-list
     from the manifest and emits `.claude/kit-lock.json`.
  3. **`doctor`** (permission category 1 — read-only): prerequisites,
     installed vs. latest kit version, manifest vs. disk, ledger vs. disk
     (missing / modified), `state.md` cap and fence integrity. The natural
     first stop, and a better answer to "something is off" than re-reading
     docs.
  4. **`upgrade`** (category 2): the plan table above, applied on
     approval.
  5. **`uninstall`** (category 3): removes only ledger entries that are
     `kit-owned`, `provenance: installed`, and hash-matching — i.e. files
     the kit demonstrably wrote and nobody has touched. Everything else is
     left in place and printed, with the reason. Deletion is irreversible,
     so it gets the strictest evidence bar of the three commands.
- A target project without a ledger is never worse off than today — it
  degrades to the conservative behaviour above, which is what an operator
  would have to do by hand anyway.
- The installer gains a write it did not have. This is an
  installer-behaviour change, and an intentional one; ADR-061 (accepted)
  already changes installer behaviour in the same phase, so the surface is
  being revised once, not twice.
- Target projects can track kit releases without fear; release notes gain
  an "upgrade impact" line per version.
- `/start` can surface doctor findings ("kit is 2 versions behind")
  without gaining mutation powers.
- Uninstall makes evaluation low-risk, which matters for the public
  distribution push (ADR-057).
- The ledger's `version` field is a parser contract, not decoration: a
  reader that meets a `version` it does not know **fails loudly** rather
  than guessing — the same rule ADR-061 sets for its manifest's
  `schemaVersion`.
- **Known consequence — line-ending normalisation looks like a local
  edit.** A project whose git config rewrites line endings on checkout
  (`core.autocrlf`) will present kit-owned files whose on-disk bytes
  differ from the hashes recorded at install. Those files classify as
  *skip + diff* forever: the upgrade is safe but noisy, and the diffs are
  phantom. This is a real ergonomic cost and it degrades in the correct
  direction (never clobbering), so it is accepted here rather than
  designed around. If it bites in practice, the fix is a normalisation
  rule at hash time — an implementation change that needs no new decision.
- **Deferred:** automated merge of locally-modified kit files (the
  operator resolves by hand from the emitted diff); multi-version
  skip-ahead migration scripts, unless a release actually needs one; and
  any `ship-loop` profile value, which belongs to ADR-060.
