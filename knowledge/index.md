# Knowledge Layer — Index

A hand-maintained map of the internal knowledge layer for the
private/source workflow-kit repository. Start here.

See [SCHEMA.md](SCHEMA.md) for conventions and curation rules.

## Current state

The kit is **published**. Source is at `kit.json` kitVersion `5.0.1`; the
public kit lives at `olivermorgan2/claude-workflow-kit` with releases
`v5.0.0` (2026-06-12) and `v5.0.1` (2026-06-29, latest). The source repo is
post-release and carries the Hermes hardened-workflow overlay.

ADR-057 (public export integrity gate) is **accepted and ratified** (ratified
by Oliver on 2026-07-13).

ADR-058 (SKILL.md body budget and progressive disclosure) is **accepted and
ratified** (accepted under mandate, issue #49; ratified by Oliver on 2026-07-14,
issue #51 — an operator attestation relayed through the Hermes supervision
channel, not a first-party artifact). Its tooling (`bin/check-skill-budget`, the
generated baseline, the skill migrations) is **decided, not built**.

ADR-061 (declarative runtime-asset manifest) is **accepted and ratified**
(accepted under mandate 2026-07-14, issue #53 / PR #54; ratified by Oliver on
2026-07-14, issue #58 — an operator attestation relayed through the Hermes
supervision channel, not a first-party artifact). Its manifest
(`runtime-assets.md`) and parser (`bin/list-runtime-assets`) are **decided, not
built** — neither file exists yet.

ADR-059 (target-project kit lifecycle) is **accepted under mandate and
UNRATIFIED** — it is the sole occupant of the ratification-debt cap
([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"). Its original draft was
HALTED on a falsified premise; Oliver ruled **Option A** (issue #55 — an operator
attestation relayed through the Hermes supervision channel, not a first-party
artifact) and it was **redrafted**: the installer writes a committed, file-keyed,
hashed `.claude/kit-lock.json` **install ledger**, and `upgrade`/`doctor`/
`uninstall` are built on **manifest (ADR-061) + ledger (ADR-059)** — what *should*
be installed, plus what *was* written. **ADR-050 is explicitly not superseded**:
the redraft stops *depending* on receipts rather than redefining them. Also
**decided, not built**, and blocked on ADR-061's tooling. See
[reviews/2026-07-14-adr-059-redraft-review.md](reviews/2026-07-14-adr-059-redraft-review.md).

**Until Oliver ratifies ADR-059, no further phase of ADRs may be accepted and
ADR-059's implementation issues may not be filed.** ADR-061's implementation
issues and the ADR-058 follow-ups were freed by ADR-061's ratification and remain
fileable — they are not blocked by ADR-059's debt.

**ADR-060 (ship-loop adoption tier) remains HALTED** and is an untracked draft. It
was halted as downstream of ADR-059 (its Option C calls `doctor`), and accepting
ADR-059 does **not** unhalt it: it needs its own redraft — adding the ADR-061
citation its text lacks — and it may not be proposed while ADR-059's ratification
debt is outstanding.

`design/state.md` is the session-continuity pointer for what to do next;
`gh` is canonical for issue and PR status. This line is the knowledge
layer's phase claim — it and [log.md](log.md) move together in a closeout.

## Contents

| File | What you'll find |
|---|---|
| [project-brief.md](project-brief.md) | What the kit is, its lifecycle, the public/private split, and the Claude / adversarial-reviewer / Hermes collaboration protocol |
| [risks.md](risks.md) | Active risks being tracked |
| [open-questions.md](open-questions.md) | Unresolved questions awaiting input or a decision |
| [log.md](log.md) | Dated, append-only log of knowledge updates |
| [reviews/](reviews/README.md) | Distilled findings from adversarial reviews |
| [SCHEMA.md](SCHEMA.md) | Conventions, file layout, and curation rules |

## Related (outside this layer)

- `design/adr/` — accepted Architecture Decision Records that govern the kit
- `docs/` — kit documentation (install, workflow, skills, troubleshooting)
- `notes/` — freeform working notes and per-issue eval summaries
- `CLAUDE.md` — Claude Code rules for working inside this repo
