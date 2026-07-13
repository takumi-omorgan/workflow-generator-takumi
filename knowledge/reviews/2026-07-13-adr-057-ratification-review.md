# 2026-07-13 — Adversarial review of the ADR-057 ratification closeout

## What was reviewed

The ratification-bookkeeping PR for issue #47: `design/state.md`,
`knowledge/index.md`, `knowledge/log.md` at commit `138f618`. No ADR content
was touched.

**Reviewer model (observed, not assumed):** `qwen/qwen3.7-plus`, served via
OpenRouter through the `hermes` CLI. Availability was probed before the run —
the model self-identified as `qwen/qwen3.7-plus`. No fallback model was used at
any point.

**Verdict: `READY`, 4/5, zero blockers.**

## Why this PR was gated at all

It is bookkeeping, not code — but it *clears the ratification-debt cap*, which
is what unblocks `adr-058`..`adr-061`. A gate that opens the next phase is a
gate. It was reviewed on that basis.

## The one finding that mattered

The review's single **major** finding: the ratification claim had **no artifact
in the repo**. The overlay's evidence-honesty rule ("never write a claim that
was not directly observed; cite the run ID / commit") is written for
machine-verifiable facts — coverage, CI, PRs. A *human ratification* is a
different category the overlay does not explicitly cover, so this was a gap in
the rules rather than a violation of them. But the effect was real: the
knowledge layer would have asserted "Oliver ratified ADR-057" with nothing
behind it but a commit message, and a false or garbled relay would have
recorded a false state and opened the next phase on it.

**Applied fix:** the ratification is now anchored to an explicit provenance
record — issue #47 comment `4963184634` — which states what was *actually*
observed (a directive relayed through the Hermes supervision channel), names it
an **operator attestation**, and says plainly that no Oliver-authored artifact
in this repo was seen. `log.md` carries the same qualification. The claim is now
no stronger than its evidence.

**Durable rule, and it generalizes:** *a human approval is not self-evidencing.*
Ratifications, sign-offs, and waivers must land as first-party artifacts (an
issue comment, a review, a signature) or be recorded explicitly as relayed
attestations. Writing them into the knowledge layer as bare fact is the same
class of error as a fabricated coverage number — the layer ends up asserting
more than anyone observed. The prior review (ADR-057 itself) produced the
sibling lesson: *observe an asserted defect before designing against it.* Both
reduce to: **the knowledge layer may not out-claim its evidence.**

## Findings not actioned (with reasons)

| Finding | Disposition |
|---|---|
| `risks.md` R1 not updated | **Correct as-is.** `bin/verify-published` is decided, not built; R1 stays open until it ships. Reviewer agreed no update was needed. |
| `open-questions.md` not updated | **Correct as-is.** Q1 was resolved in the ADR-057 acceptance PR (#46); this PR does not touch it. |
| Closeout atomicity | **Verified.** `state.md`, `index.md`, `log.md` agree and moved in one PR; the reviewer found no contradiction between them. |
| ADR-057 content unmodified | **Verified.** Diff touches three files, none an ADR. `Status: accepted` / `Date: 2026-07-08` unchanged, per ADR-044. |

## Validation observed at review time (commit `138f618`)

- `bin/self-test` — ok, 21/21 steps passed
- `bin/check-consistency` — consistent (22 skills; docs and metadata agree)
- `bin/export-public --dry-run` — ok, 258 files, verifier clean, gates passed
- `bin/check-state-cap --check` — `design/state.md` 96 lines (cap 100), ok
