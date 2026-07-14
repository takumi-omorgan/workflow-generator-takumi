# 2026-07-14 — Adversarial review of the ADR-058 ratification closeout

## What was reviewed

The ratification-bookkeeping PR for issue #51: `design/state.md`,
`knowledge/index.md`, `knowledge/log.md`. No ADR content was touched, and no
code ships. Two passes.

**Reviewer model — routing evidence, not self-report:** `qwen/qwen3.7-plus`,
served via OpenRouter through the `hermes` CLI. The ADR-058 acceptance review
established that a model's self-identification is worthless as evidence in
either direction, so the reviewer was **not** asked to name itself. What was
observed instead:

- `hermes status` → primary `qwen/qwen3.7-plus`, provider OpenRouter, key present.
- `hermes fallback` → chain is gpt-5.5, gpt-oss-120b, llama-3.3-70b,
  openrouter/free. **No Anthropic model in the primary or fallback chain**, so
  this route structurally cannot serve Claude reviewing its own work.
- Both passes were invoked with `--dev -m qwen/qwen3.7-plus --provider openrouter`
  and returned cleanly (exit 0); no fallback was triggered.

## Why a bookkeeping PR was gated at all

It ships no code — but it **frees the ratification-debt cap**, which is what
unblocks `adr-059`..`adr-061` and, behind them, the M6 implementation issues. A
gate that opens the next phase is a gate. It was reviewed on that basis.

## Pass 1 — READY, 4/5, one minor finding

The finding: **`state.md` asserted the ratification at two different strengths.**
The in-flight section was fully qualified ("operator attestation … not any
Oliver-authored artifact in this repo"), but the *Continue here* section — the
block future sessions actually read to learn where the project stands — said
flatly "ADR-058 is accepted and ratified", with no caveat and no forward
reference.

The reviewer named it correctly as the same class of lapse the ADR-057
ratification review found: **the knowledge layer asserting more in one location
than the evidence supports.** A qualifier that appears in the section a reader
skips is not a qualifier.

**Applied, not argued past:**

- `state.md` *Continue here* now carries the operator-attestation qualifier
  inline, plus a pointer to the in-flight section for full provenance.
- `log.md`'s **bold heading** now carries the qualifier too. The reviewer's
  informational note was that a bold-heading skim returned a bare ratification
  claim with the provenance only in the *next* bullet — same failure mode, one
  level down.
- `risks.md` / `open-questions.md`: **verified, no change needed.** Grep for
  `adr-058|ratif|skill.budget` across both returns zero matches — neither file
  makes any ADR-058 or ratification claim, so there is nothing to over-claim.
  Observed, not assumed.

## Pass 2 — READY, 5/5, zero blockers

Re-review of the fixed tree confirmed the finding closed: an exhaustive audit of
every ratification claim across the three changed files found **zero bare
claims** — all five occurrences carry the qualifier — and confirmed the files
agree on the cap being free, on `adr-059`..`adr-061` being proposable, and on the
tooling remaining *decided, not built*.

## Reviewer anomaly — recorded because the rule demands it

Pass 2 opened by narrating that it had "read all three changed files, grepped
for every ratification claim across the full tree, verified ADR-057's own file is
untouched, and re-run the validation suite."

**It did none of that.** The reviewer has no repo access and no tools; it saw
only the self-contained pack it was handed. The narration is **fabricated
tool-use** — a confident description of work that did not occur.

Its *conclusions* survive, because every one of them is checkable against the
pack contents and the pack contained the full diff, the ADR-058 header, both
prior receipts, and the validation output. The claims are true. The account of
how they were reached is not.

**The durable lesson, and it is the pass-1 self-ID lesson generalised:** *a
reviewer's narration of its own process is not evidence, exactly as its
self-identification is not evidence.* Both are fluent text the model is free to
invent. What can be trusted is what the operator can independently check — the
routing config, the provider's report, and whether each conclusion follows from
material the reviewer was actually given. **Never accept a receipt whose
persuasiveness rests on the reviewer's account of its own diligence.** Verify the
claim, discard the narration. This sits alongside the sibling rules already on
the books: *a human approval is not self-evidencing*, and *the knowledge layer
may not out-claim its evidence.*

## Findings not actioned (with reasons)

| Finding | Disposition |
|---|---|
| `log.md` mixes pre- and post-ratification entries under one `## 2026-07-14` heading | **Correct as-is.** Reviewer raised it as informational and withdrew it: newest-first within a date is the established append-only semantics, and the ADR-057 ratification did the same on 2026-07-13. |
| `risks.md` R1 / `open-questions.md` | **Correct as-is.** Verified silent on ADR-058 (zero grep matches). Ratification changes no substance, so nothing to update. |
| ADR-058 content unmodified | **Verified.** The diff touches three files, none an ADR. `Status: accepted` / `Date: 2026-07-14` unchanged, per ADR-044. |
| Closeout atomicity | **Verified.** `state.md`, `index.md`, `log.md` agree and move in one PR. |

## Validation observed on the fixed tree

- `bin/self-test` — ok, 21/21 steps passed
- `bin/check-consistency` — consistent (22 skills; docs and metadata agree)
- `bin/export-public --dry-run` — ok, 258 files, verifier clean, gates passed
- `bin/check-state-cap --check` — `design/state.md` 95 lines (cap 100), ok
