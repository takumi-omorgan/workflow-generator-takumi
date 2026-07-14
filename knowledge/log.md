# Knowledge Log

Append-only, dated log of knowledge-layer updates. Newest entries at the
top. One line per update; link to the file or section that changed.

## 2026-07-14

- **ADR-059 redrafted and accepted under mandate — the lifecycle now rests on a
  committed install ledger, not on receipts.** Oliver ruled **Option A** of the halt
  note's option space (issue #55 — an **operator attestation** relayed through the
  Hermes supervision channel, directive verbatim: *"approved"*, applied to a plan
  recommending Option A; **no Oliver-authored artifact in this repo was observed**,
  and the [ruling comment](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/55#issuecomment-4967121740)
  is that artifact). The Decision: the installer writes a committed, file-keyed,
  hashed `.claude/kit-lock.json`, and `upgrade`/`doctor`/`uninstall` are built on
  **manifest (ADR-061) + ledger (ADR-059)** — the manifest declares what *should* be
  installed and who owns it; the ledger records what *was* written. `.claude/` is
  already committed in targets except three paths, so the ledger needs **no gitignore
  change** (`templates/gitignore.target:18-22`). Scope issue #60,
  [review receipt](reviews/2026-07-14-adr-059-redraft-review.md).
- **ADR-050 is explicitly *not* superseded.** The redraft **stops depending on**
  receipts rather than redefining them — which is precisely what dissolves the
  "contradicts ADR-050" risk the [halt note](reviews/2026-07-14-adr-059-halt.md)
  raised. Receipts stay gitignored, per-run, work-unit-keyed idempotency artifacts;
  ADR-050's deferred follow-ups stay deferred. ADR-061 is **adopted, not extended**:
  its closed ownership vocabulary (`kit-owned | generated | user-seeded`) is used
  verbatim, its profile set stays `{ full }`, its since-version column stays
  informational. ADR-059 is **decided, not built** — and it is blocked on ADR-061,
  which is *also* not built.
- **ADR-059 now occupies the ratification-debt cap** (freed hours earlier by ADR-061's
  ratification). It is accepted *under mandate*, **awaiting Oliver's async
  ratification** — tracked in a follow-up ratification-request issue. Until he
  ratifies, **ADR-060 and ADR-059's implementation issues may not be filed**.
  **ADR-060 remains HALTED** pending its own redraft; ratifying ADR-059 will not
  unhalt it.
- **Review lesson — one agreeable pass is not a gate.** Pass 1 (neutral framing)
  returned READY on 17 checked premises. Pass 2 re-ran the *same artifact* under an
  explicitly **hostile** framing and found a **blocking** defect: the missing-ledger
  path would have written the *user's own edited* content hash under a kit asset ID,
  so the next upgrade would read it as proof of kit provenance and **auto-clobber the
  user's work** — violating the ADR's headline guarantee via its own documented
  degradation path. Fixed with a `provenance: installed | adopted` field: an `adopted`
  entry is never eligible for `replace`, and provenance is *earned by being written,
  never by being observed*. READY on pass 3 of 3.
- **Durable lesson: when one field is asked to mean two things, it will eventually
  authorise the wrong one.** `sha256` meant "bytes we wrote" in the happy path and
  "bytes we found" in the degraded path, and the degraded value flowed into the happy
  path's decision. Ask of every field: *who may write it, and what may a reader
  conclude from it?* If those answers do not compose, it is two fields. (Same shape as
  the halt that produced this redraft, which asked *receipts* to mean something they
  did not.)
- **Oliver ratified ADR-061 (operator attestation — provenance in the next bullet);
  the ratification-debt cap is free.** ADR-061 was accepted *under mandate* in PR #54
  (issue #53) and held the one slot the overlay allows for a phase of ADRs awaiting
  async ratification ([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"). With it
  ratified, **no phase sits unratified**: a further phase of ADRs may be accepted, and
  ADR-061's implementation issues — plus the ADR-058 follow-ups — are now fileable.
  Recorded **here and in [`design/state.md`](../design/state.md), not in the ADR**: the
  format carries only `Status` and `Date` — there is no ratification field — and
  accepted ADRs are never edited in place (ADR-044). Ratification changes no substance:
  `runtime-assets.md`, `bin/list-runtime-assets`, and the required/optional fail-fast
  installer semantics remain **decided, not built**. Bookkeeping tracked in issue #58.
- **Provenance of that ratification, stated at its true strength.** It was conveyed
  through the **Hermes supervision channel** (session directive of 2026-07-14, verbatim:
  *"I ratify ADR-061 and approve you to move forward"*), not by any Oliver-authored
  artifact in this repo — **no signature, no email, no commit, and no repo-side message
  was observed before the attestation comment was posted.** It is an **operator
  attestation**, anchored to issue [#58 comment 4966870880](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/58#issuecomment-4966870880),
  which was posted *before* the bookkeeping landed and invites Oliver to confirm it into
  a first-party record. This is the ADR-057/058 ratification rule being applied rather
  than re-learned: **a human approval is not self-evidencing, and the knowledge layer
  may not out-claim its evidence.** If the relay is wrong, reverting the PR for issue #58
  restores the debt and re-blocks the next phase of ADRs; nothing else depends on it.
- **Clearing the debt cap does not unhalt ADR-059/060 — a necessary condition is not a
  sufficient one.** The two are independent blocks that happened to coincide, and the
  tempting inference ("the cap is free, so the halted drafts may proceed") is exactly
  the one to refuse. ADR-059 is halted on *substance*: its Decision rests on a falsified
  premise and needs a **committed install manifest**, a different artifact — Oliver's
  ruling, still open in **#55**. ADR-060 is downstream of it. All three files
  ([`design/state.md`](../design/state.md), [index.md](index.md), and this log) say so
  explicitly, so a future session cannot read the freed cap as a green light. Durable
  lesson: **when one of two overlapping blocks lifts, say plainly that the other did
  not** — a closeout that only reports what unblocked reads as though everything did.
- **`state.md`'s `next-action` YAML has been silently lossy — `#` and `: ` are live
  syntax in an unquoted scalar.** Found while applying the review finding above, not by
  the reviewer. In YAML, a `#` after a space **starts a comment**: the pre-existing
  `args:` line (`... redraft (issue #55) — receipt-layer premise falsified ...`) parsed
  *successfully* while **truncating everything from `#55` onward**, and a `: ` inside a
  plain scalar is a hard parse error. The `next-action` block routinely carries issue
  numbers and prose colons — precisely the two characters that corrupt it. All three
  values are now **quoted** and the block is verified to round-trip through
  `yaml.safe_load` intact. Note which failure mode is the dangerous one: the invalid
  case **errors loudly**; the lossy case **parses**. And
  [`bin/check-state-cap`](../bin/check-state-cap) counts lines — it **never parses the
  YAML it guards**, so nothing caught this. Durable lesson: **quote YAML scalars that
  can contain `#` or `: `; a guard that does not parse its artifact does not guard it.**
  Closing that check is a fileable follow-up.
- **ADR-059 HALTED before review — its load-bearing premise is false.** The draft
  claimed "the receipt layer already records what the installer wrote and at which
  version" and made that the Decision: *"the receipt layer becomes the source of
  truth for what the kit owns in a target project."* Verification falsified it four
  ways: the installer **writes no receipt** (`bin/install-workflow-kit:410` merely
  *copies* the `write-receipt` script); `docs/receipts.md` calls installer receipts
  a **deferred follow-up**; receipts are **gitignored** (`templates/gitignore.target:22`),
  so a fresh clone has none; and the ADR-050 schema is keyed by **work-unit**
  (issue/PR/release tag) with **no path list, version, or hash** — it cannot answer
  "unmodified since install." ADR-059 needs a *committed install manifest*, which is
  a **different artifact**, and making receipts committed would **contradict accepted
  ADR-050** (which requires a superseding ADR first). That reaches the Decision, so
  the pre-approved plan's stop condition fired. **ADR-060 is halted with it** (its
  Option C calls `doctor`, an ADR-059 surface). No ADR-059/060 issue, branch or PR
  was opened; both remain untracked drafts. Escalated to Oliver — see
  [reviews/2026-07-14-adr-059-halt.md](reviews/2026-07-14-adr-059-halt.md), which
  lays out the option space **without choosing one**.
- **Durable lesson: "the X layer already does Y" is a premise, not a citation.**
  ADR-059 named artifacts that genuinely exist (`bin/write-receipt`,
  `schemas/receipt.v1.yaml`) and inferred a *capability* from their *existence*.
  Existence was true; shape, durability and coverage were all false — and the
  Decision rested on all three. The cheap mechanical check: **for every "X already
  does Y", open X and find Y.** Three greps falsified it before a line of review
  was spent. This is the same failure class as ADR-057, whose audit falsified two
  of three premises.
- **ADR-061 (declarative runtime-asset manifest) accepted under mandate**
  (issue #53) — the first of the three M6–M9 prerequisite ADRs, and the one the
  other two consume. It replaces the installer's inline `RUNTIME_TEMPLATES`
  array with a `runtime-assets.md` manifest + `bin/list-runtime-assets` parser,
  and turns a missing **required** asset from warn-and-continue into fail-fast.
  The drift it targets is not hypothetical: the array shipped with **12** entries
  (PR #65, `d245674`) and carries **13** today. **Decided, not built.**
- **The review caught a dependency inversion that would have made the sequencing
  decorative.** ADR-061 sequences before ADR-059/060 *because* they consume its
  manifest — but as drafted it exposed two enumerated columns (`profiles`,
  ownership class) whose valid values were defined by those very drafts. It
  would have shipped a column only an unaccepted document could validate. The
  cure: **ADR-061 now owns both vocabularies** — ownership is a closed set that
  ADR-059 adopts (changing it needs a superseding ADR), and profiles ship as
  exactly `{ full }`, closed and enforced, which ADR-060 extends on acceptance.
  Durable lesson: **if X sequences before Y because Y consumes X, every
  enumerated value X exposes must be closed by X.** Caught at review it is a
  wording fix; caught later it is a data migration. See
  [reviews/2026-07-14-adr-061-review.md](reviews/2026-07-14-adr-061-review.md).
- **The parser contract is part of the decision, not an implementation detail.**
  The reviewer's sharpest finding: the cited precedent (`criteria.md`) is a table
  scripts *cite* but none parses, so `bin/list-runtime-assets` is the kit's first
  such parser — and a *permissive* parser that skipped malformed rows would have
  recreated the warn-and-continue failure the ADR exists to end, one layer up.
  The ADR now pins it: strict parsing (a bad row is a hard error, never skipped),
  **no fallback to a hardcoded list** on an unparseable manifest (that would
  quietly restore the rejected Option A), and `--allow-missing` as an explicit,
  loud, test-only flag.
- **Reviewer identity is evidenced by routing, not self-report.** Both passes
  recorded `model: qwen/qwen3.7-plus`, `provider: openrouter`, `failed: false`
  from `hermes --usage-file`, with a fallback chain containing no Anthropic
  model. This is the ADR-058 hallucinated-self-ID lesson applied: **a model's
  claim about which model it is carries no evidential weight in either
  direction** — the routing record does.
- **Oliver ratified ADR-058 (operator attestation — provenance in the next
  bullet); the ratification-debt cap is free.** ADR-058 was
  accepted *under mandate* in PR #50 (issue #49) and held the one slot the
  overlay allows for a phase of ADRs awaiting async ratification
  ([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"). With it ratified, no
  phase sits unratified and the remaining M6–M9 prerequisite ADRs
  (`adr-059`..`adr-061`) are unblocked for proposal. Recorded **here and in
  [`design/state.md`](../design/state.md), not in the ADR**: the format carries
  only `Status` and `Date` — there is no ratification field — and accepted ADRs
  are never edited in place (ADR-044). Ratification changes no substance:
  `bin/check-skill-budget`, the generated baseline, and the skill migrations
  remain **decided, not built**.
- **Provenance of that ratification, stated at its true strength.** It was
  conveyed through the **Hermes supervision channel** (session directive of
  2026-07-14), not by any Oliver-authored artifact in this repo — no signature,
  no email, no commit was observed. It is an **operator attestation**, anchored
  to issue [#51 comment 4964025789](https://github.com/takumi-omorgan/workflow-generator-takumi/issues/51#issuecomment-4964025789),
  which was posted *before* the bookkeeping landed and invites Oliver to confirm
  it into a first-party record. This is the ADR-057 ratification rule being
  applied rather than re-learned: **a human approval is not self-evidencing, and
  the knowledge layer may not out-claim its evidence.** If the relay is wrong,
  reverting PR for issue #51 restores the debt and re-blocks `adr-059`..`adr-061`;
  nothing else depends on it.
- **A reviewer's narration of its own process is not evidence either.** The
  ratification review ([reviews/2026-07-14-adr-058-ratification-review.md](reviews/2026-07-14-adr-058-ratification-review.md))
  opened its second pass by describing how it had "read all three changed files,
  grepped the full tree, verified ADR-057's file is untouched, and re-run the
  validation suite." It has no repo access and no tools — it saw only the
  self-contained pack it was handed. The conclusions held (each is checkable
  against the pack), but the account of how they were reached was **fabricated
  tool-use**. This generalises the ADR-058 self-ID lesson: both a model's
  identity claim and its diligence claim are just fluent text it can invent.
  Trust only what the operator can independently check — routing config,
  provider report, and whether each conclusion follows from material the
  reviewer actually received. **Verify the claim; discard the narration.**
- **ADR-058 (SKILL.md body budget and progressive disclosure) accepted under
  mandate; the ratification-debt cap is consumed.** Accepted in the PR for
  issue #49 after adversarial review reached READY (4/5, zero blockers) on its
  second pass — see
  [reviews/2026-07-14-adr-058-review.md](reviews/2026-07-14-adr-058-review.md).
  ADR-058 is now the one phase of ADRs awaiting Oliver's async ratification
  ([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"), so **`adr-059`..`adr-061`
  may not be proposed and no M6 implementation issues may be filed** until he
  ratifies it. Decision-only: `bin/check-skill-budget`, the generated baseline,
  and the skill migrations are **decided, not built**.
- **The review killed the ADR's original mechanism, and the reason generalises.**
  The draft proposed an *advisory* 800-word check plus a grace list that "must
  shrink each release"; the reviewer rejected it as *"a hope that future-you
  will feel differently, which is the status quo that produced the problem"* —
  the proposed cure was a weaker form of the disease. The accepted design
  (Option D) instead pins each of the 18 over-budget skills to **its own current
  word count** as a CI-blocking ceiling, blocking from the checker's first
  commit, with no advisory phase to flip. Growth stops on day one without
  demanding a 22-skill rewrite first. Durable lesson: **a baseline is only a
  ratchet if the baseline itself is ratcheted** — ceilings must be provably
  non-increasing, or one PR raises the ceiling and the body together and passes.
- **Measured, not estimated.** The draft's "roughly 35,000 words" was replaced
  with observed counts: **33,444 words across 22 skills**, 18 of which exceed
  800 (median 1,397); five heaviest 2,384–2,706 words. The reviewer itself
  miscounted ("20 of 22 exceed"; actual is 18) — its conclusion held, but the
  slip is a reminder that a reviewer's arithmetic is not evidence either.
- **A model's self-report is not evidence of which model served the request.**
  The reviewer availability probe answered `claude-opus-4-6`, which would have
  meant Claude reviewing its own work. It was a hallucinated self-ID: no
  Anthropic model exists in the configured primary *or* fallback chain, the
  `hermes --dev` routing banner read `qwen/qwen3.7-plus`, and three repeat
  probes agreed. Receipts must cite routing/provider evidence, never the
  model's self-description — it can neither confirm nor condemn the reviewer.
- **Open defect recorded:** [ADR-054](../design/adr/adr-054-script-vs-skill-boundary.md)
  is still marked `proposed` although its helpers shipped under issue #13 (17
  `bin/` files cite it) — implementation merged without its ADR ever being
  accepted. ADR-058 no longer claims otherwise. The drift needs its own gate;
  it was out of scope for a decision-only PR. Tracked in
  [`design/state.md`](../design/state.md) → Blockers.

## 2026-07-13

- **Oliver ratified ADR-057; the ratification-debt cap is free.** ADR-057 was
  accepted *under mandate* in PR #46 (issue #45) and had been sitting as the
  one phase of ADRs allowed to await async ratification
  ([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"). Oliver has now ratified
  it, so no phase sits unratified and the M6–M9 prerequisite ADRs
  (`adr-058`..`adr-061`) are unblocked for proposal. Ratification is recorded
  **here and in [`design/state.md`](../design/state.md), not in the ADR**: the
  ADR format carries only `Status` and `Date` — there is no ratification field
  — and accepted ADRs are never edited in place (ADR-044). Ratification does
  not change ADR-057's substance: `bin/verify-published` remains **decided, not
  built**, so [risks.md](risks.md) R1 stays open until it ships.
  **Provenance, stated honestly:** the ratification was conveyed through the
  Hermes supervision channel (session directive of 2026-07-13) and is an
  **operator attestation** — no Oliver-authored artifact in this repo was
  directly observed. It is anchored to issue #47 comment `4963184634` rather
  than to a commit message alone. The adversarial review of the ratification PR
  (`qwen/qwen3.7-plus`, READY 4/5, 0 blockers) raised exactly this as its one
  major finding; the attestation comment is the fix. Receipt:
  [reviews/2026-07-13-adr-057-ratification-review.md](reviews/2026-07-13-adr-057-ratification-review.md).
- **Accepted ADR-057 (public export integrity gate) — after falsifying two of
  its three motivating premises.** The first draft claimed the published repo
  had an identity mismatch and shipped internal exhaust (`archive/`, `notes/`,
  the `CLAUDE.md` contributor section). An audit of the live public repo at its
  then-HEAD (`1c0eba3`) found **both claims false**: the published tree is
  exactly the 258 files `bin/export-public` produces, with correct identity
  strings and no excluded paths. The **ADR-056 export contract is being
  honoured**. Only the third claim held — there is no post-publish verification
  — and it is *latent*, not an active defect. ADR-057 was **rewritten** around
  that one real gap (the verified `dist/` tree and the live remote are
  separately derived; nothing asserts they match) and re-reviewed to `READY`
  (`qwen/qwen3.7-plus`, 4/5, 0 blockers, 4 minor findings all applied). The
  identity-rewrite work the false premise had commissioned was **dropped**.
  Resolved [open-questions.md](open-questions.md) Q1 and re-scoped
  [risks.md](risks.md) R1 (mitigation decided; `bin/verify-published` not yet
  built). Receipt:
  [reviews/2026-07-13-adr-057-review.md](reviews/2026-07-13-adr-057-review.md).
  **Durable lesson (second occurrence): when a review asserts an observable
  defect, observe it before designing against it.** A `READY` score from a
  reviewer without repo access is conditional on its own premise findings —
  read the findings, not just the verdict.
- **Switched the default adversarial reviewer from Codex to Qwen 3.7 Plus.**
  The hardened-workflow gate in [`CLAUDE.md`](../CLAUDE.md) and the roles/gates
  in [project-brief.md](project-brief.md) named Codex as the reviewer. The
  operating default is now **Qwen 3.7 Plus** (`qwen/qwen3.7-plus`) via
  OpenRouter/Hermes. **The gate itself is unchanged** — `READY` is still
  required, and reviewer-unavailable still means HALT, now explicitly with no
  silent fallback to another model. Made the durable-review wording in
  [SCHEMA.md](SCHEMA.md) and [reviews/README.md](reviews/README.md)
  model-neutral, and required receipts to record the **model ID actually
  used** so the next default change doesn't invalidate the archive. Historical
  receipts keep their accurate Codex attribution — they *were* Codex reviews.
- **Recorded the Hermes Kanban direction: external / orchestrator-only.**
  Answered [open-questions.md](open-questions.md) Q3 in principle (build still
  deferred, nothing implemented). GitHub remains canonical for issues, PRs, and
  milestones; the kit ships no board/queue/DB runtime and this decision adds
  none. A Hermes Kanban, if built, mirrors GitHub and reads the
  fence-parseable `design/state.md` zones (`state:in-flight`,
  `state:next-action`) as dispatch inputs; optional backlog import stays
  Hermes-side. No Hermes-specific board internals enter the public kit unless
  a later ADR scopes it. Distinct from ADR-012 (GitHub Projects boards inside a
  *target* project), which is untouched.
- **Closed out v5.0.x: the kit is published.** `design/state.md` had been stale
  since 2026-06-21, still describing v5.0.0 as frozen and "awaiting
  identity-gated publish". Verified against `gh`: the public repo
  `olivermorgan2/claude-workflow-kit` exists (created 2026-06-12, public), and
  releases `v5.0.0` (tag `a38a142`, 2026-06-12) and `v5.0.1` (tag `1c0eba3`,
  2026-06-29, latest) are both published; source `kit.json` kitVersion is
  `5.0.1`. Rewrote the in-flight, blockers, recent-work, continue-here, and
  next-action sections accordingly — the publish blocker is cleared, and the
  next step is proposing the M6–M9 prerequisite ADRs (which currently exist
  only as untracked local drafts), not opening M6 issues.
- Recorded the durable lesson behind PR #40: the `guard` placeholder check
  grepped whole changed files, so a knowledge/design file that *describes* a
  placeholder token false-positived. Process checks over an append-only
  knowledge layer must scan **added lines**, not file contents — otherwise the
  layer's own history makes the gate unusable. Added
  [open-questions.md](open-questions.md) Q3 (Hermes Kanban, deferred).

## 2026-06-23

- **Corrected the Codex-findings diagnosis (second pass).** The first-pass
  read assumed source was at `v4.0.0` with the v5 command model/docs/validation
  scripts absent; current source is `kit.json` `kitVersion 5.0.0` with all of
  it present. Re-verified: 4 of 7 findings are source-actionable doc/content
  fixes (now shipped), 3 are false positives, none transform-created. Shipped
  source fixes: `jq` prerequisite added to `README.md` + `docs/install.md`
  (Finding 1 — standalone `jq` is used in six target-installed helpers and
  `bin/self-test`'s tool gate); de-staled `docs/github-setup.md` "What's next"
  and fixed its stale repo name (Finding 7); clarified the verb layer vs. the
  installed `/start` router in `README.md` + `docs/architecture.md` (Findings
  2/3). Retired risk R2 and resolved question Q2 (no source↔public divergence).
  Updated [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
- Verified Codex's 7 public-release (v5.0.0) findings against the source repo:
  1 valid (Finding 7, `docs/github-setup.md`), 3 invalid, 1 invalid-as-stated,
  2 not-applicable. Recorded the source↔public divergence as risk R2 /
  question Q2 and added
  [reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
  No public-release fixes implemented.
- Initialized the knowledge layer: added `SCHEMA.md`, `index.md`,
  `project-brief.md`, `risks.md`, `open-questions.md`, `log.md`, and
  `reviews/README.md`. Seeded the project brief with the kit overview, the
  Scope → Decide → Backlog → Implement → Ship lifecycle, the public/private
  split, and the Claude/Codex/Hermes collaboration protocol. Recorded the
  public-release-protocol risk as an open risk/question pending details.
