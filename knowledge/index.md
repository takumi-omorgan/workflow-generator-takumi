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
supervision channel, not a first-party artifact). It is the first of the three
M6–M9 prerequisite ADRs (`adr-059`, `adr-060`, `adr-061`), and the only one that
landed. Its manifest and parser are **decided, not built**.

**No phase of ADRs is awaiting ratification** — ADR-061 was the sole occupant of
the ratification-debt cap ([`CLAUDE.md`](../CLAUDE.md) → "Ratification debt"),
which is now **free**. A further phase of ADRs may be accepted, and ADR-061's
implementation issues (plus the ADR-058 follow-ups) may be filed.

**ADR-059 and ADR-060 are HALTED, not merely un-proposed.** ADR-059's Decision
rests on a premise verified false — the receipt layer neither records what the
installer wrote, survives a clone, nor can express file ownership (see
[reviews/2026-07-14-adr-059-halt.md](reviews/2026-07-14-adr-059-halt.md)). It
needs a *committed install manifest*, a different artifact, and adopting one
changes its Decision — so it was stopped before review rather than patched.
ADR-060 is downstream of it. **Both remain untracked drafts; neither may be
proposed until Oliver rules on the redraft** (issue #55, still open). The freed
ratification-debt cap does **not** unhalt them: the cap was never what blocked
them, so clearing it is necessary but not sufficient.

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
