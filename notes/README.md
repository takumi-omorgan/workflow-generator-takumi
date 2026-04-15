# Working notes

Scratch and intermediate files used while building the kit itself. These
are **kit-repo-only** — they are not copied into target projects.

Contents:

- `issue<n>.md` — body text for each GitHub issue on the MVP backlog
- `issue<n>-prompt.md` — the per-issue Claude Code prompt used to work on
  that issue (plan-first, see ADR-006)
- `github-setup.md` / `github-setup2.md` — one-off setup prompts used to
  provision the GitHub repo, labels, milestones, and issues

The reusable Claude Code session prompt is at
[`issue-prompt.md`](issue-prompt.md), with a worked example at
[`issue-prompt-sample.md`](issue-prompt-sample.md). See
[`docs/issue-prompt-guide.md`](../docs/issue-prompt-guide.md) for how
to fill it and what the end-of-session evaluation summary must contain.
