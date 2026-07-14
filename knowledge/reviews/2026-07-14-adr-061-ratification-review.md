# 2026-07-14 — Adversarial review of the ADR-061 ratification closeout

## What was reviewed

The ratification-bookkeeping PR for issue #58: `design/state.md`,
`knowledge/index.md`, `knowledge/log.md`. No ADR content was touched, and no code
ships. Two passes.

**Reviewer model — routing evidence, not self-report:** `qwen/qwen3.7-plus`, served
via OpenRouter through the `hermes` CLI. Per the standing rule, the reviewer was
**not** asked to name itself — a model's self-identification is worthless as evidence
in either direction. What was observed instead:

- `hermes status` → Model `qwen/qwen3.7-plus`, Provider OpenRouter, OpenRouter key
  present (`sk-o...d7a9`).
- `hermes fallback` → primary `qwen/qwen3.7-plus` (via openrouter); fallback chain is
  gpt-5.5, `openai/gpt-oss-120b:free`, `meta-llama/llama-3.3-70b-instruct:free`,
  `openrouter/free`. **No Anthropic model anywhere in the primary or fallback chain**,
  so this route structurally cannot serve Claude reviewing its own work.
- Both passes were invoked with `--dev -m qwen/qwen3.7-plus --provider openrouter` and
  returned cleanly (exit 0); no fallback was triggered.

The reviewer was also explicitly instructed **not to narrate tool use** — the ADR-058
ratification review caught its reviewer fabricating an account of having grepped the
tree and re-run the suite. It complied: it named its pack gaps rather than inventing
verification it could not perform.

## Why a bookkeeping PR was gated at all

It ships no code — but it **frees the ratification-debt cap**, which is what permits
the next phase of ADRs to be accepted and implementation issues to be filed. A gate
that opens the next phase is a gate. It was reviewed on that basis.

## Pass 1 — READY, 4/5, zero blockers, one minor finding

The gate threshold (READY, ≥4, zero blockers) was met on the first pass. The finding
was taken anyway rather than banked.

The finding: **the `next-action` YAML block asserted the ratification bare.** Its
`preconditions: [ADR-061 ratified, ...]` carried no operator-attestation qualifier,
while every prose claim around it did. The reviewer correctly declined to call this
the ADR-058 pass-1 failure (that was bare prose in the section readers actually read;
this is a machine-readable summary three lines below a qualified paragraph) — but
named the principle that still applies: **a YAML field is part of the knowledge layer,
and the knowledge layer may not out-claim its evidence.**

**Applied, not argued past:** the precondition now reads
`"ADR-061 ratified (operator attestation, issue #58)"`.

The reviewer separately confirmed the ADR-058 pass-1 lesson *had* been applied at every
prose site: the qualifier appears inline in `state.md`'s in-flight section, in its
*Continue here* block, in `index.md`, and in `log.md`'s **bold heading** — not only in
a follow-up bullet a skimmer would miss.

## A latent YAML defect found while applying the fix — not by the reviewer

Applying the finding meant putting `issue #58` inside a YAML flow sequence. Parsing the
block before and after revealed a bug that **neither the reviewer nor any repo check
catches**:

- `#` after a space **starts a YAML comment**. `preconditions: [ADR-061 ratified
  (operator attestation — issue #58), ...]` does not merely lose text — it fails to
  parse outright (unterminated flow sequence).
- Worse, the **pre-existing** `args:` line had the same flaw in a silent form: `args:
  Oliver ... (issue #55) — receipt-layer premise falsified ...` parsed *successfully*
  while **truncating everything from `#55` onward**. The `next-action` block has been
  quietly lossy, and nothing flagged it.

All three scalar values are now **quoted**, and the block is verified to round-trip
through `yaml.safe_load` with no truncation.

**Durable lesson: `#` and `: ` are live syntax in an unquoted YAML scalar.** The kit's
`next-action` block routinely contains issue numbers (`#55`) and prose colons — exactly
the two characters that silently corrupt a plain scalar. Quote the values. And note the
failure mode that matters: the *invalid* case is safe, because it errors loudly; the
*lossy* case is the dangerous one, because it parses. **`check-state-cap` counts lines
and never parses the YAML it guards** — a gap worth closing separately.

## Pass 2 — READY, 5/5, zero blockers

Re-review of the fixed tree, with the pack gap closed (pass 1 correctly noted it had not
been shown this receipt, which did not exist yet). Confirmed the finding closed, the
YAML round-trip clean, and no ratification claim left bare across the three files.

## The substantive point the review was pointed at, and cleared

Freeing the debt cap must **not** be readable as unhalting ADR-059/060 — their halt is
substantive (ADR-059's Decision rests on a falsified premise and needs a *committed
install manifest*, a different artifact), not a debt-cap block. The reviewer verified
all three files say so explicitly and unanimously, and concluded: *"A future session
cannot read this PR as unhalting ADR-059/060."* Issue #55 stays open for Oliver's
ruling.

`log.md` records the generalisation: **when one of two overlapping blocks lifts, say
plainly that the other did not** — a closeout that reports only what unblocked reads as
though everything did.

## Findings not actioned (with reasons)

| Finding | Disposition |
|---|---|
| ADR-061 content unmodified | **Verified.** The diff touches three files, none an ADR. `Status: accepted` / `Date: 2026-07-14` unchanged, per ADR-044. |
| Closeout atomicity | **Verified.** `state.md`, `index.md`, `log.md` agree and move in one PR. |
| Reviewer could not independently confirm ADR-061 untouched (pack gap) | **Correct as-is.** Inherent to a no-tools reviewer; the full diff was in the pack and contains no ADR path. Noted honestly rather than papered over. |
| `risks.md` / `open-questions.md` | **Correct as-is.** Ratification changes no substance, so neither has an ADR-061 claim to over- or under-state. |

## Validation observed on the fixed tree

- `bin/self-test` — exit 0; ok, 21/21 steps passed
- `bin/check-consistency` — exit 0; consistent (22 skills; docs and metadata agree)
- `bin/export-public --dry-run` — exit 0; ok, 258 files, verifier clean, gates passed
- `bin/check-state-cap --check` — exit 0; `design/state.md` 99 lines (cap 100)
