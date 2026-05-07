# ADR-025: License the kit under MIT

**Status:** accepted
**Date:** 2026-04-26

## Context

The kit's source — `skills/`, `templates/`, `bin/`, `docs/`,
`examples/`, `Design/`, `notes/`, top-level docs — currently ships
without a `LICENSE` file. The README states "License: not yet
specified." Without an explicit license, default copyright applies:
downstream users technically cannot redistribute, modify, or fork
the kit, even though it is in a public repository.

This is a soft blocker on external adoption. For a kit whose entire
purpose is to be installed into other projects, the absence of a
license is the wrong default. It is also a hard blocker on the
public-distribution split tracked as feature-ideas #19, which
cannot proceed until the public repo has a license.

The kit's design goal is widest possible applicability and
permissive distribution. The license should match: maximally
permissive, well-recognized, and unambiguous — so license
scanners (GitHub, npm, SPDX, package managers), legal teams, and
casual readers all reach the same conclusion without effort.

A separate question is the **boundary between the kit's license and
the user's work product**. The kit ships templates, skills, and
scripts. Users install these into their own projects and run them
to scaffold and produce their own artifacts (`Design/mvp.md`,
`Design/prd.md`, ADRs, prompts, source code, tests). The user's
artifacts are the user's work — original content the user authored
through the kit's prompting. The kit's license must apply to the
kit's source, not propagate into anything users create with it.

## Options considered

### Option A: MIT License

- Pros: most widely understood permissive license; ~30 lines of
  unambiguous text; instantly recognized by every dev, every license
  scanner, every package ecosystem; allows commercial use,
  modification, sublicensing, redistribution; one trivial condition
  (preserve the notice in copies); compatible with everything.
- Cons: no explicit patent grant — irrelevant for a kit of markdown
  templates and shell scripts.

### Option B: Apache License 2.0

- Pros: explicit patent grant from contributors; explicit trademark
  reservation; widely used in large-corp open source.
- Cons: longer text (~200 lines); NOTICE-file rules add small adopter
  friction; the patent grant buys nothing for templates and scripts.

### Option C: BSD 2-Clause / 3-Clause

- Pros: functionally near-identical to MIT.
- Cons: less recognized than MIT outside the BSD ecosystem; the
  3-Clause "no endorsement" provision adds a clause that does not
  apply to a tooling kit.

### Option D: ISC License

- Pros: even shorter than MIT.
- Cons: less recognized than MIT outside the npm ecosystem;
  effectively "MIT but obscurer."

### Option E: The Unlicense / CC0

- Pros: most permissive on paper — public-domain dedication.
- Cons: public-domain dedication is legally fragile in some
  jurisdictions (Germany, France); the FSF specifically advises
  against The Unlicense for this reason; downstream users get
  legal ambiguity in exchange for marginal additional permissiveness.

### Option F: Custom or modified license

- Pros: could embed the kit-vs-user-output clarification directly.
- Cons: any modification to a standard license stops it being
  recognized as that license; license scanners default to "custom"
  or "unknown"; legal review burden on adopters; downstream
  ecosystems treat unknown licenses as risky and often skip them.

## Decision

License the kit under **MIT**, copyright `(c) 2026 Oliver Morgan`.
Add a standard `LICENSE` file at the repo root containing the
canonical, unmodified MIT text.

The kit-vs-user-output boundary is documented in the kit's
`README.md` and in this ADR — **not** in the `LICENSE` file itself.
Modifying the canonical MIT text would defeat the recognition
benefit (Option F). The boundary is supported in plain text
elsewhere where readers will find it; legally, MIT's terms already
do not propagate to user-created original content (the user's
filled-in `Design/mvp.md`, source code, etc., are their own
copyrightable work, not derivatives of the kit's empty templates).

Specifically:

- **Kit source under MIT:** all files shipped in this repository —
  `skills/`, `templates/`, `bin/`, `docs/`, `Design/`,
  `examples/`, `notes/`, top-level `*.md`, `LICENSE`, etc.
- **What the user produces by running the kit is the user's:**
  rendered `Design/mvp.md`, `Design/prd.md`, individual ADRs the
  user authors, prompts under `prompts/`, working notes, and any
  source code, tests, or build artifacts of the project being
  built. The kit's MIT terms cover the empty templates and skills,
  not the user's filled-in content.
- **Copies of MIT-licensed kit files inside a target project:**
  when the installer copies `skills/<name>/SKILL.md`, the
  `LICENSE` notice should remain associated with those files. In
  practice, the installer keeps them under `.claude/skills/<name>/`
  with their original headers, and the kit's LICENSE applies to
  those copies. This is a one-time installation obligation, not
  a license-propagation concern.

**Installer behaviour for target-project licensing:** the installer
does **not** auto-scaffold a `LICENSE` into target projects by
default. License choice is the target-project author's decision; the
kit does not pick it for them. An optional flag — `--license=mit`
(and possibly other SPDX identifiers in future) — scaffolds a fresh
`LICENSE` populated with a `--license-holder` value (or the
`--project-name` as a fallback). When scaffolded, the target's
`LICENSE` is a **new** MIT license attributed to the user, not a
copy of the kit's `LICENSE`. This keeps the legal model clean: the
target project's license stands on its own.

## Consequences

- A `LICENSE` file is added at the kit root with canonical MIT text
  and Oliver Morgan's copyright.
- The kit's README replaces "License: not yet specified" with a
  short section pointing at `LICENSE` and stating the kit-vs-user
  boundary.
- License scanners on GitHub will now correctly identify the repo
  as MIT.
- The public-distribution split (feature-ideas #19) is unblocked on
  the licensing front.
- The installer adds an optional `--license=mit` flag (and
  `--license-holder=NAME`) for users who want a `LICENSE` scaffolded
  alongside the rest of the target-project setup. Default behaviour
  is unchanged: no `LICENSE` is written into target projects unless
  explicitly requested.
- Future contributors: contributions to the kit are accepted under
  MIT (standard inbound=outbound rule). No CLA required for a
  permissive license of this nature.
- The `examples/projects/` content remains under MIT as part of the
  kit (it is documentation/sample material, not user-authored
  output).
- Adoption-tooling cost: zero. MIT is the most-recognized
  permissive license; no friction for downstream users, package
  scanners, or legal review.
