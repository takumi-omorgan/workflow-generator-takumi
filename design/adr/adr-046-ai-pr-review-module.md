# ADR-046: Optional AI PR review module

**Status:** superseded by [ADR-051](adr-051-operator-driven-ai-pr-review.md)
**Date:** 2026-05-07

## Context

The kit currently carries a project from planning (ADR-003 PRD intake)
through implementation (ADR-014 executor) and PR creation (the
`pr-review-packager` skill), but the **review** step on the PR is
manual once the PR is open on GitHub. For a kit whose value
proposition is a GitHub-first delivery workflow (ADR-004), this is a
notable gap — review is the one stage where the operator currently
has no kit-shaped support.

Two constraints frame the decision:

1. **Stay GitHub-native.** Per ADR-004, the kit does not introduce
   non-GitHub surfaces. Any review tooling must surface its output
   inside the GitHub PR — no separate dashboard, no provider
   portability in v1.
2. **Stay opt-in and lightweight.** Per CLAUDE.md ("no premature
   automation, no speculative abstractions") and ADR-001's
   per-project copy-install model, a review layer must integrate
   into the existing installer surface without becoming a default
   dependency for users who don't want it.

The feature-ideas entry (`notes/feature-ideas.md` lines 487–515,
captured 2026-05-06, status `ready-for-adr`) sketches a hybrid
diff-first reviewer running on `pull_request` events, posting
structured review comments, with Claude Code preserved as the
implementation agent. Two follow-up entries (full-codebase indexing
for AI review; advanced model and credential customization) remain
`idea` status — deliberately deferred behind a usable v1.

This ADR records the architectural shape for v1 of the optional AI
PR review module so implementation, when it begins, has a single
contract to follow. The module's `Target: future` status in the
notepad means this ADR is forward-looking — recorded now,
implemented in a later milestone.

## Options considered

### Option A: Optional module shipped in this repo, installer-flag-driven

- Pros: matches the kit's existing per-project copy-install model
  (ADR-001) without requiring a new distribution channel; opt-in via
  one boolean installer flag mirrors the established `--license`
  pattern from ADR-030; users who don't want AI review pay zero file
  or dependency cost; OpenRouter as the provider layer keeps the kit
  one-secret-per-target-project; a default model alias avoids
  forcing an ADR amendment whenever the recommended model changes.
- Cons: introduces an external API dependency surface and a secret
  (`OPENROUTER_API_KEY`) into target projects; v1 review quality is
  bounded by diff-first context (mitigated by the future-entry
  follow-ups); an additional `.github/` workflow file to maintain as
  GitHub Actions runners and action versions evolve.

### Option B: Always-installed module, disabled-by-default

- Pros: no installer-flag surface; activation is "set the secret"
  rather than "re-run the installer with a flag"; one fewer flag in
  the installer's combinatoric matrix.
- Cons: every install carries `.github/workflows/ai-pr-review.yml`
  and `.github/ai-review/config.yml` whether or not the user wants
  them, mixing optional-feature config into the mandatory kit asset
  list (the same drift class feature-ideas #36 / #37 are already
  trying to close, in the opposite direction); harder to keep
  `.github/` clean for users who genuinely do not want AI review.

### Option C: Separate sibling kit in its own repo

- Pros: cleanest scope split — the main kit stays focused on
  planning and execution; the review module evolves on its own
  release cadence; matches the long-running plugin / public-repo
  split direction in feature-ideas #19.
- Cons: doubles the distribution surface; users who want both have
  two install steps and a version-alignment problem (kit-vN with
  module-vM); premature for v1 — there is no evidence yet that the
  module's lifecycle differs enough from the kit's to justify the
  split. Rejected as speculative abstraction per CLAUDE.md.

## Decision

Adopt **Option A**. The optional AI PR review module ships in this
repo, behind a `--with-ai-review` boolean installer flag. When set,
the installer copies two files into the target project:

- `.github/workflows/ai-pr-review.yml` — runs on `pull_request`
  `opened` and `synchronize` events. Invokes a small helper script
  that calls OpenRouter, reads the diff and config, and posts the
  review back to the PR via the GitHub API. Skips silently when an
  `ai-review-skip` label is present, so operators can opt out per PR.
- `.github/ai-review/config.yml` — declares the model alias (default:
  the OpenRouter-recommended OpenAI-family alias, not a pinned
  version), the inline-comment toggle (default: on, with a
  conservative high-confidence threshold), and any path-glob
  excludes.

Activation requires the operator to set `OPENROUTER_API_KEY` as a
repository secret. Without the secret, the workflow exits cleanly
with a one-line "module not configured" message. This keeps the
file-system surface installable in advance of credential setup.

**Output shape:** one structured top-level review comment (Summary,
Strengths, Concerns, Suggestions) plus selective inline comments for
high-confidence actionable issues, gated by the config's threshold.
The structured top-level comment is always posted; inline comments
are opt-out via config.

**Two explicit deferrals** for v1, each with a captured follow-up
entry in `notes/feature-ideas.md`:

1. **Full-codebase context and indexing** is out of scope. v1 is
   diff-first plus nearby-files only. Notepad entry already
   captured (line ~519).
2. **Advanced model / credential customization** — multiple model
   profiles, organization-level secrets, per-repo model overrides
   beyond the single config knob — is out of scope. Notepad entry
   already captured (line ~550).

A separate, larger deferral — an automated PR-comment remediation
helper that ingests unresolved PR comments and converts them into a
Claude Code remediation prompt — is captured as its own
feature-ideas entry rather than collapsed into a deferral bullet
here, because its option-space (new skill vs flag-on-`prepare-issue`,
comment-thread schema, re-run semantics) is distinct from this
ADR's. v1's contract stops at writing review feedback to GitHub —
the operator reads and addresses comments via the existing manual
flow until the remediation helper ships in its own ADR. This
preserves ADR-041's permission-contract spirit; any automated
GitHub write-back from a Claude Code session would require its own
permission-contract entry.

The module's interaction with `pr-review-packager` (the existing PR
creation skill) is one-way and additive: the packager still drafts
the PR body the operator pushes; the AI review module reads the
resulting PR diff and posts review feedback. No skill-spec changes
to `pr-review-packager` are required.

## Consequences

- Easier: target projects gain a GitHub-native review loop without
  shifting review out of GitHub (preserves the ADR-004 GitHub-first
  posture); review becomes the first kit stage with end-to-end
  support; future entries (full-codebase context, advanced model
  config) have a stable v1 to extend rather than re-architect.
- Harder: introduces an external API dependency and a
  secret-management path into target projects (each install must
  decide whether to set `OPENROUTER_API_KEY`); review quality on
  architecture-sensitive PRs will be bounded by diff-first context
  until the full-codebase-context follow-up lands; a `.github/`
  workflow file is now part of the kit's runtime-asset surface and
  must stay current as GitHub Actions runners and action versions
  evolve.
- Maintain: one new installer flag (`--with-ai-review`); two new
  runtime assets in the target-project layout (workflow + config);
  one new bin-helper or workflow-internal script that wraps the
  OpenRouter call; the `.github/ai-review/config.yml` schema is new
  shared surface that any future module-config skill must respect.
  If the runtime-asset manifest from feature-ideas #36 lands first,
  these two files become entries in that manifest rather than
  another installer-internal hardcoded list.
- Deferred: full-codebase indexing and retrieval (notepad future
  entry, line ~519); advanced model and API-key configuration
  (notepad future entry, line ~550); automated PR-comment
  remediation helper (its own feature-ideas entry — to be drafted
  as a separate ADR once v1 of this module has shipped and produced
  real reviews to learn from). Provider portability beyond
  OpenRouter (direct OpenAI, Anthropic, GitLab/Bitbucket non-GitHub
  providers) follows the kit's existing GitHub-first / Claude-first
  scope per ADR-004 and ADR-006 and is not reopened by this ADR.
