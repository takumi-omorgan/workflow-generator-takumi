# Claude Code Workflow Kit — State

**Last updated:** 2026-06-21
**Source of truth:** `gh` is canonical for issue/PR status; this file is a pointer.

<!-- state:phase:start -->

## Phase

single

<!-- state:phase:end -->

<!-- state:in-flight:start -->

## In-flight issue

- **Issue:** v5.0.0 public distribution — publish to `olivermorgan2/claude-workflow-kit`
- **Prompt:** notes/publication-runbook-private.md + docs/publishing.md
- **Branch:** main (source frozen) / publish operates on generated `dist/public`
- **Status:** source frozen at `kit.json` kitVersion `5.0.0`; public export hardened through PR #31; **awaiting identity-gated publish** (public repo not yet created, no `v5.0.0` tag)

<!-- state:in-flight:end -->

<!-- state:recent:start -->

## Recent work

Rolling list of the last five issues completed (oldest drops off as
new entries land). One line each: PR number, ADR if any, one-line
summary.

- #31 — none — drop "dogfooding" from public-shipped write-receipt header
- #30 — none — make pr-context ADR paths symlink-stable so collect-eval passes in public export
- #29 — none — point contributor clone at the real source repo
- #28 — none — close v5.0.0 public-export follow-up gaps from the Fable 5 review
- #27 — none — keep kit-private guiding-doc references out of the public export

<!-- state:recent:end -->

<!-- state:blockers:start -->

## Blockers

Public repo `olivermorgan2/claude-workflow-kit` not yet created; `gh` auth
must switch to `olivermorgan2` before the identity-gated publish step.

<!-- state:blockers:end -->

<!-- state:continue-here:start -->

## Continue here

v5.0.0 metadata is frozen (`kit.json` kitVersion `5.0.0`, curated `CHANGELOG.md` v5.0.0 section) and the public-export workstream is hardened through PR #31. The release is blocked only on the human, identity-gated publish step — not on code. Pre-publish correctness fixes folded in stay v5.0.0 (no bump): ship `bin/check-plan` to target projects so the `adr-writer` ADR gate actually runs, and expand `ADR-NNN..MMM` range / comma-list tokens in `bin/pr-context`. Next: run pre-publish validation (`notes/publication-runbook-private.md`), then the identity-gated publish (create the public repo, push `dist/public`, tag `v5.0.0`, `gh release create`). After publish, file the remaining `notes/workflow-kit-notes.md` dry-run feedback (review-pr timeout/heartbeat, docs-render preamble, prd-to-mvp default, install-summary clarity, trusted auto-publish, Codex provider docs, quality-gate orchestrator) as the v5.0.1 / v5.1.0 backlog.

<!-- state:continue-here:end -->

<!-- state:next-action:start -->

## Next action

```yaml
skill: release            # or the manual runbook (publish is identity-gated)
args: --version=5.0.0
preconditions: [clean export-public on HEAD, gh auth = olivermorgan2]
blocked-by: public repo olivermorgan2/claude-workflow-kit not yet created
```

<!-- state:next-action:end -->
