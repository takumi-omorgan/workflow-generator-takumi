# Adversarial review — ADR-059 redraft (target-project kit lifecycle, on a committed install ledger)

**Artifact:** `design/adr/adr-059-target-project-kit-lifecycle.md`
**Issues:** #60 (scope), #55 (the halt, and Oliver's Option A ruling)
**Date:** 2026-07-14
**Outcome:** **READY on pass 3 of 3.** Accepted under mandate; **ratification pending**.

Supersedes nothing. This reviews the *redraft* that replaced the draft HALTED earlier
today ([halt note](2026-07-14-adr-059-halt.md)).

## Reviewer and routing evidence

The reviewer model is recorded from **observed routing**, not model
self-identification. The ADR-058 receipt incident (a model hallucinating its own
identity) is why: a model's claim about which model it is carries no evidential
weight in either direction. Routing config and the per-call usage record do.

- **Configured route** (`hermes status`, `hermes fallback list`): primary
  `qwen/qwen3.7-plus` via **OpenRouter**. The fallback chain (gpt-5.5 /
  gpt-oss-120b / llama-3.3-70b / openrouter/free) contains **no Anthropic model**,
  so no silent same-family review was possible.
- **Per-call evidence** (`hermes --usage-file`), all three passes:

| Pass | `model` | `provider` | `session_id` | `failed` | Verdict |
|---|---|---|---|---|---|
| 1 | `qwen/qwen3.7-plus` | `openrouter` | `20260714_105500_45ebbd` | `false` | READY |
| 2 | `qwen/qwen3.7-plus` | `openrouter` | `20260714_105653_4f6a24` | `false` | **REVISE** |
| 3 | `qwen/qwen3.7-plus` | `openrouter` | `20260714_110608_b1fb7d` | `false` | READY |

`failed: false` on every call establishes the primary served each request — no
fallback entry was reached.

The reviewer had **no repository access**. Each pass was a self-contained packet:
the full ADR, the halt note verbatim, ADR-050's and ADR-061's accepted text, the
receipt schema, the target `.gitignore` template, and the installer's relevant
lines with true line numbers (`grep -n`, not hand-transcribed).

## The pass-1 lesson: an agreeable pass is not a gate

Pass 1 used a neutral framing and returned **READY**, checking 17 premises and
finding no contradiction. Pass 2 re-ran the *same artifact* under an explicitly
**hostile** framing — "a previous reviewer passed this; find what they missed" —
and landed a **blocking** defect. The redraft would have shipped with it.

The durable point: **one agreeable review pass is not evidence of correctness.**
A reviewer asked "is this okay?" and a reviewer asked "break this" are running
different experiments. The halt this ADR came from was caught by a hostile
question too. Cost of the extra pass: ~$0.03 and two minutes.

## Pass 2 — REVISE (one blocking finding)

**B1 (BLOCKING) — the missing-ledger path laundered user edits into trusted
provenance.** The draft said a degraded upgrade "may write a fresh ledger
afterwards, **recording what is on disk at that point**." The failure chain:

1. Pre-ledger install; the user edits kit-owned files.
2. Upgrade finds no ledger → every asset is *skip + diff*.
3. The operator **keeps** their edits (explicitly permitted).
4. The fresh ledger records **the user's** content hash under a kit asset ID.
5. The *next* upgrade sees hash-match → **"replace — provably unmodified since
   install"** → **user edits auto-clobbered**, reported as a safe replace.

The ADR's headline guarantee — no clobbered user edits — was violated by its own
documented degradation path. The reviewer also killed the obvious alternative
("only record what the installer wrote"): omitted files then have *no* ledger
entry, and the table's `absent → install` row overwrites them anyway. Both
readings clobber.

Non-blocking notes: ownership-change ambiguity (manifest or ledger wins?); the
"no new runtime dependency" claim overstated for the *installer*; CRLF drift;
the absent-`generated` case unspecified.

## The fix

The root cause was **one field carrying two meanings**. `sha256` was being used
both as "the bytes the kit wrote" (which authorises `replace`) and as "whatever
is on disk" (which authorises nothing). The fix separates them:

- New required per-asset field **`provenance`**, closed vocabulary
  `installed | adopted`. `installed` = the kit wrote these exact bytes, so the
  hash is evidence. `adopted` = found on disk, kit did not write it, hash is
  **not** evidence of provenance.
- **An `adopted` entry is never eligible for `replace`** — always *skip + diff*.
  It converts to `installed` only by the kit actually writing those bytes.
  Provenance is *earned by being written, never by being observed*.
- The classification table was rebuilt and completed: a file **present on disk
  with no ledger entry** is now *skip + diff*, **not** *install*. Invariant:
  *absence of evidence is never evidence of absence*.
- **Ownership is read from the current manifest, never the ledger** — closing the
  reclassification ambiguity, and failing safe (reclassification can only remove
  the kit's licence to write, never grant one).
- The dependency claim was corrected against verified fact: the installer treats
  `python3` as **optional** (`bin/install-workflow-kit:623` — "Use Python if
  available … otherwise fall back to portable sed"), so the ledger is emitted with
  `printf` from bash rather than promoting an optional dependency to a hard one.
  The one genuinely new requirement — a `sha256sum`/`shasum` hasher — is stated,
  with a loud failure if absent.
- CRLF drift and the absent-`generated` case are now explicit consequences.

Notably, the missing-ledger case stopped being a special case: it is simply the
state where every asset has no ledger entry, and the general table already gives
the safe answer.

## Pass 3 — READY

The reviewer traced its own failure chain step-by-step through the new rules and
confirmed step 8 now classifies *skip + diff*; it searched for any path from
`adopted` to auto-replace and found none. It confirmed the second hole
(`none | present | present`) closed, the `installed`/`adopted` distinction
maintainable (the upgrader only needs "did I write this file in this run?"), and
**no trespass on ADR-061**: `ownership` (manifest, "who owns this?") and
`provenance` (ledger, "did we write this?") are orthogonal axes, and ADR-061
explicitly scopes a target-side record of what *was* written as outside itself.

One non-blocking clarity note — whether a carried-forward `installed` file is
downgraded to `adopted` when a run doesn't rewrite it — was closed in the final
text: provenance carries forward, `installed` iff the kit wrote the bytes now on
disk (this run or a previous one, evidenced by an unbroken hash).

## Non-supersession, confirmed on all three passes

- **ADR-050 is not superseded.** Receipts stay gitignored, per-run, work-unit-keyed
  idempotency artifacts. The redraft **stops depending on** them rather than
  redefining them — which is exactly what dissolves the "contradicts ADR-050" risk
  the halt note raised. ADR-050's deferred follow-ups stay deferred.
- **ADR-061 is adopted, not extended.** Its closed ownership vocabulary
  (`kit-owned | generated | user-seeded`) is used verbatim; its profile set stays
  `{ full }`; its since-version column stays informational and un-branched-on.

## Durable lesson

**When one field is asked to mean two things, it will eventually authorise the
wrong one.** `sha256` meant "bytes we wrote" in the happy path and "bytes we
found" in the degraded path, and the degraded path's value flowed into the happy
path's decision. The defect was invisible at the level of the sentence that
introduced it ("record what is on disk" reads as obviously correct bookkeeping)
and only appeared when a hostile reader traced a value across two upgrade cycles.

This is the same shape as the halt that produced this redraft: the first draft
asked *receipts* to mean something they did not. **Ask of every field: who is
allowed to write it, and what is a reader allowed to conclude from it?** If those
two answers do not compose, the field is two fields.
