---
name: claude-issue-executor
description: Drive a disciplined implementation session from a prepared issue prompt — plan-first, branch, incremental commits, tests alongside, evaluation summary. Use when running the implementation session for an issue whose prompt artefact already exists; use /prepare-issue first if no prompt is on disk.
permission-category: 2  # operator-acknowledged-bypass — significant-task plan-mode gate per workflow-guide §7
inputs:
  - name: "prompt-or-issue"
    required: false
    description: "Path to prompts/issue-NNN-*.md, or the issue number"
  - name: "--no-prompt"
    required: false
    description: "Run without a prepared prompt file"
outputs:
  - artefact: "(branch + commits)"
    description: "Feature branch, incremental commits, tests alongside"
  - artefact: "notes/eval-issue-NNN.md"
    description: "Evaluation summary"
next:
  - skill: pr-review-packager
    when: "implementation is complete"
---

# claude-issue-executor

Run a full implementation session for one GitHub issue from a prepared
prompt: parse it, propose a plan and **block for explicit approval**, branch
from `main`, implement in incremental ADR/issue-referencing commits with
tests alongside, and write an evaluation summary. Orchestrator only.

Reference (rationale, examples, exact state/receipt commands, test-runner
list):
[`docs/skills/claude-issue-executor.md`](../../docs/skills/claude-issue-executor.md).
Co-installed companions read as needed: [`plan-mode.md`](plan-mode.md)
(significance, `--no-prompt`), [`reference.md`](reference.md) (edge cases,
alignment, design-questions), [`example.md`](example.md).

## When to use

After `/prepare-issue` wrote `prompts/issue-NNN-*.md`. If none exists, stop
and tell the user to run `/prepare-issue` (or hand-author one matching
`prompts/_template.md`). Does **not** create prompts, PRs, or ADRs, or modify
GitHub issues.

## Invocation

`/claude-issue-executor <prompt-path | issue-number>`

- **Path** → use it as the prompt.
- **Issue number** → resolve `prompts/issue-NNN-*.md`. If absent, auto-invoke
  `/prepare-issue NNN` (log it) and proceed. If present but **stale** (older
  than the issue's `updatedAt` or a linked ADR), ask whether to regenerate —
  default yes, never silent; on `n`, note it.
- **No argument** → list candidates from `prompts/` (fallback
  `notes/issue*-prompt.md`) and ask which.
- **`--no-prompt`** → run without a prompt (`plan-mode.md`); use the issue
  body directly and append `issue executed without prompt per ADR-038` to the
  first commit.

## Prompt validation

Confirm the prompt has these sections (case-insensitive heading or bold
label): **Context, ADR, GitHub Issue, Goal, Requirements, Scope and
constraints, Instructions for you**. Extract the **ADR number** and **issue
number** (`#N`) for commits and the branch name. If any is missing, **stop**,
report it, and ask whether to fix (via `/prepare-issue`) or proceed without —
never invent. (Skipped under `--no-prompt`.)

## The plan gate (load-bearing — ADR-006)

Every session follows this exact sequence:

1. Resolve and validate the prompt; confirm the working tree is clean (else
   stop — commit/stash/discard) and you are on `main` (or agree to switch);
   read `CLAUDE.md` and the ADR.
2. **Produce a step-by-step plan in one message**: proposed branch name;
   every file to create/modify with a one-line reason; the commit sequence
   (message + files); whether/where tests are written; end verification.
3. **Stop.** Between proposing and approval, call **no** mutating tool
   (Write, Edit, git, tests, any state change) — only read-only calls to
   answer questions. A clarifying question is **not** approval; answer and
   re-present.
4. Proceed only on explicit approval ("yes"/"approved"/"go ahead"); on a
   change request revise and return to step 2; on denial stop and offer to
   revise or hand back.

Route plan-mode by significance (`plan-mode.md`): significant → harness plan
mode; borderline → ask once; trivial → chat gate alone (category-2).

## After approval

1. **Branch** from `main` (`git checkout -b <branch>`).
2. **Implement, committing incrementally** per the commit model. If a new
   significant boundary appears mid-session (scope grows past what was
   classified), pause and re-flag plan-mode; never silently cross it.
3. **Verify:** run the project's tests if any exist, plus any verification in
   the prompt's evaluation section.
4. **Update `design/state.md`** if present (ADR-035/048): with `bin/fence
   replace` (never by hand), rewrite the `in-flight` zone (keep
   `Issue`/`Prompt`, set `Branch`, `Status: verified`) and the `next-action`
   zone (→ `pr-review-packager`). Never touch `recent`. Skip an absent file;
   on a broken fence, note it in follow-ups and suggest `/pause`. Exact
   commands: reference.
5. **Evaluation summary** (below): print it and write it to
   `notes/eval-issue-NNN.md` (zero-padded).
6. **Handoff:** suggest `/pr-review-packager`; never invoke it — the human
   review checkpoint before the PR is deliberate.

## Commit model

- One logical change per commit; tests land in the **same** commit as the
  code they cover.
- Message: `<verb>(<scope>): <what> (ADR-NNN, #issue)` — verb ∈
  feat/fix/docs/refactor/test/chore, scope = primary folder. ADR-NNN and
  #issue come from the **prompt**, never invented.
- Before any commit touching `design/adr/adr-*.md`, run `bin/sync-adr-index`
  and stage `design/adr/README.md` alongside (ADR-023).
- **Test-alongside:** if the project has a test runner (detection list in
  the reference), write tests alongside; else say so in the summary and use
  documentation-style verification.

## Evaluation summary

One structured message, mirrored **byte-for-byte** to
`notes/eval-issue-NNN.md` (what `/pr-review-packager` reads):

- **What changed** — files created/modified, by purpose.
- **Commits** — messages in order, SHAs when known.
- **Verification** — runner/build output, or a walk-through if no tests.
- **Follow-ups** — out-of-scope notes; never silently defer in-scope work. A
  design question affecting an upcoming issue → append a `### design-questions`
  YAML block (ADR-040 schema; rules in `reference.md`) that
  `bin/validate-carry-forward` checks.
- **Commands to reproduce** — shell lines.
- **Next step** — `/pr-review-packager`.

`--no-prompt` runs note the bypass for the audit trail.

## Receipts and alignment

Cat-2 mutating skill: idempotency receipts keyed by **issue number**
([`docs/receipts.md`](../../docs/receipts.md)). **Before** branch/commit
work, check for a `completed` receipt — if found, the work already landed, so
stop and report. **On completion** write a `completed` receipt (branch + any
PR); on interruption a `partial`/`failed` one naming what remains.
Best-effort, gitignored, never blocks handoff (exact commands: reference).
Before finishing, run the seven-item alignment checklist (`reference.md`) and
report any unchecked box rather than hiding it.
