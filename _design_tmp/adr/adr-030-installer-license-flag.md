# ADR-030: Implement installer `--license` flag

**Status:** accepted
**Date:** 2026-04-26

## Context

[ADR-025](adr-025-license.md) documented the kit's MIT license and
the kit-vs-user-output boundary. Among the consequences was an
optional installer flag, `--license=mit --license-holder=NAME`, that
would scaffold a starter LICENSE into a target project for users who
want one. ADR-025 documented the contract but **deferred the
implementation** to a follow-up.

This ADR closes that implementation gap. Without it, the
`--license=mit` flag is documented (in `README.md` and ADR-025) but
not wired into `bin/install-workflow-kit`. Users who try the flag
get an "unknown argument" error, and the kit's documented behaviour
disagrees with its actual behaviour — a small but real correctness
problem.

The implementation is scoped narrowly: ship the `--license=mit`
path now, leave the door open for additional SPDX identifiers
(Apache-2.0, BSD, etc.) later if anyone asks. No need to
over-engineer for licenses no one has requested.

## Options considered

### Option A: Inline the MIT license text in the installer script

- Pros: smallest possible change; no new template files; no
  templating layer for LICENSE content.
- Cons: bloats the installer (~20 lines of license text); awkward
  to add additional licenses later (each would mean another inline
  heredoc); diverges from the kit's existing pattern of templating
  user-facing artifacts via files under `templates/`.

### Option B: Template file under `templates/licenses/`, rendered by the installer

- Pros: consistent with how the kit handles other artefacts
  (CLAUDE.md, MVP, PRD, ADR templates all live under
  `templates/`); easy to add additional licenses later as more
  files in the same directory; license text is inspectable
  alongside other templates.
- Cons: one more directory to maintain; minor structural overhead
  for a single-license start.

### Option C: Defer the implementation indefinitely

- Pros: zero work.
- Cons: the documented contract in ADR-025 remains broken; users
  trying the flag get a confusing error; "promised in an ADR but
  not implemented" is a smell that grows with time.

## Decision

Adopt **Option B**. Implement the flag with a license template at
`templates/licenses/mit.txt`, rendered by `bin/install-workflow-kit`
on demand. Specifically:

- Add `templates/licenses/mit.txt` with the canonical, unmodified
  MIT license text and two placeholders: `{{YEAR}}` and
  `{{COPYRIGHT_HOLDER}}`.
- Add two flags to `bin/install-workflow-kit`:
  - `--license=mit` — opt in to scaffolding a `LICENSE` in the
    target. No license is scaffolded if this flag is absent
    (default unchanged from ADR-025).
  - `--license-holder=NAME` — copyright holder string substituted
    into the rendered LICENSE. If absent, fall back to the
    `--project-name` value. If neither is set, fall back to the
    target directory's basename.
- The year is filled with the current year at install time.
- Skip-if-exists: if the target already has a `LICENSE`, skip
  rendering and warn (consistent with `CLAUDE.md`'s skip-if-exists
  behaviour). `--force` overwrites.
- Validate the `--license` value: only `mit` is accepted in this
  release. An invalid value errors out with a list of supported
  identifiers.
- The new flags are documented in `docs/install.md`'s flag table
  and in the script's `--help` output.

Future licenses (Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC) can be
added by dropping new files under `templates/licenses/<spdx>.txt`
and extending the validator. That extension is **out of scope** for
this ADR.

The kit-vs-user-output boundary established by ADR-025 still
applies: when scaffolded, the target project's LICENSE is a fresh
MIT license attributed to the user (or whatever holder they
specified), not a copy of the kit's own LICENSE. The two licenses
are independent legal instruments.

## Consequences

- New file: `templates/licenses/mit.txt` with `{{YEAR}}` and
  `{{COPYRIGHT_HOLDER}}` placeholders. Uses the standard MIT text
  exactly as published by SPDX so license scanners recognize the
  rendered output as MIT.
- `bin/install-workflow-kit` gains two flags and one new render
  step. Default behaviour is unchanged: no LICENSE is written
  unless `--license=mit` is explicitly passed.
- `templates/README.md` index gains a row for the licenses
  directory pointing at the available license templates.
- `docs/install.md` flag table is updated with the two new flags
  and a brief example.
- Example scaffolding command in the README is updated to show
  the optional license flags in the worked example.
- The contract documented in ADR-025 is now real and exercised.
- Follow-up: if any user requests another license, a
  one-paragraph extension ADR + a new file under
  `templates/licenses/` covers it. No structural change required.
- Per [ADR-026](adr-026-kit-versioning-policy.md), this change is
  **MINOR**: a new installer flag with backwards-compatible
  default. Ships in v3.2.0 alongside ADR-028 and ADR-029.
