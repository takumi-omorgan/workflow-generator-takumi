# claude-issue-executor — operator reference

Rationale, examples, and background for the `claude-issue-executor` skill.
The agent operates from `skills/claude-issue-executor/SKILL.md` and its
co-installed companions (`plan-mode.md`, `reference.md`, `example.md`); it
never reads this file. Anything needed to produce a correct result lives in
the body or those companions — this file is for the human operator.

## Why this skill exists

It is the enforcement mechanism for the execution model decided in
[ADR-006](../../design/adr/adr-006-claude-code-execution-model.md) and the
orchestration contract decided in
[ADR-014](../../design/adr/adr-014-claude-issue-executor-skill.md). It is
also the **producer** in the cross-skill design-question carry-forward chain
decided in
[ADR-040](../../design/adr/adr-040-cross-skill-design-question-carry-forward.md)
— see [`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040)
for the canonical schema, mirrored machine-readably in
[`schemas/design-questions.v1.yaml`](../../schemas/design-questions.v1.yaml)
and checked by `bin/validate-carry-forward`.

The plan gate is load-bearing: skipping it violates ADR-006 and defeats the
purpose of the skill. The harness-level plan mode
(`shift+tab shift+tab`, [ADR-039](../../design/adr/adr-039-plan-mode-for-significant-tasks.md),
[ADR-038](../../design/adr/adr-038-tighten-prompt-step.md)) runs alongside
the in-session chat gate; the executor instances the **category-2** rule of
the auto-mode permission contract
([`docs/workflow-guide.md` §7](../../docs/workflow-guide.md#7-auto-mode-permission-contract-adr-041)).

## What this skill does not do

- Does not create prompts. That is `/prepare-issue`.
- Does not create pull requests. That is `/pr-review-packager`. This skill
  suggests it in the final summary but never auto-invokes it.
- Does not draft, amend, or accept ADRs. ADRs are authored by `adr-writer`
  and accepted by a human.
- Does not modify GitHub issues, labels, milestones, or the issue body.
- Does not duplicate logic from other skills. It is an orchestrator: prompt
  parsing, plan gate, branching, commits, tests, summary, handoff.

## Branch naming (examples)

Derive the branch name from the prompt filename, preferring the short,
descriptive, kebab-case form that matches the repo convention in
[`docs/github-setup.md` section 5](../../docs/github-setup.md#5-branch-naming-and-pull-requests)
— no leading `feature-`, no numeric-only names:

- `prompts/issue-017-pr-review-packager.md` → `pr-review-packager-skill` is
  one acceptable form; so is `issue-017-pr-review-packager`.
- If the prompt filename already matches convention, use it verbatim with
  the `issue-NNN-` prefix stripped when the short title alone is distinctive.
- When in doubt, show the proposed branch name in the plan and let the user
  amend it before approval.

## Commit message examples

```
feat(skills): add claude-issue-executor skill (ADR-014, #16)
docs(skills): wire claude-issue-executor into skills/README.md (ADR-014, #16)
```

The `<verb>` is `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, etc.;
the `<scope>` points at the primary folder touched (`skills`, `docs`,
`templates`, …). ADR-NNN and #issue come from the prompt, not the current
conversation.

## Test-runner detection (full list)

Detect whether the project has a test runner by checking, in order:

- `package.json` → `scripts.test` (Node/JS/TS projects)
- `pytest.ini`, or `pyproject.toml` with a `[tool.pytest.ini_options]`
  section (Python)
- `Cargo.toml` with a `[lib]` or `[[test]]` section (Rust)
- `go.mod` (Go — `go test ./...` is always available)
- any file ending in `*test*.*` in a conventional tests folder

If any is present, write tests as part of the logical commit that introduces
the code they cover. If the project has **no** test runner (common for
docs-only kits like this one), note that in the evaluation summary and rely
on documentation-style verification instead. Tests for a prose-only skill (a
SKILL.md that contains no runnable code) are usually unnecessary; a
walk-through in the evaluation summary is the accepted substitute.

## Plan-mode rhythm and `--no-prompt`

The chat plan-gate in the body is the in-session 8-step rule. Claude Code
also ships a harness-level mechanism (plan mode, `shift+tab shift+tab`) that
locks mutating tools until the user exits. The two run together. When the
executor parses an invocation it classifies the session against a
significance/trivial checklist and routes to one of three plan-mode
branches, then optionally runs in `--no-prompt` mode for trivial issues. The
significance and trivial checklists, the hybrid routing path, auto-mode
behaviour, the alignment-review obligation, and the `--no-prompt` rules live
in the co-installed [`plan-mode.md`](../../skills/claude-issue-executor/plan-mode.md).

## `### design-questions` on-disk shape

When the session raises a design question that affects an upcoming issue,
append a structured block under `## Follow-ups` of the eval summary. The
canonical schema, field semantics, and `target-issue` quoting rule live in
[`docs/workflow-guide.md` §6](../../docs/workflow-guide.md#6-cross-skill-carry-forward-adr-040);
the co-installed
[`reference.md`](../../skills/claude-issue-executor/reference.md#design-questions-populate-rules)
carries the When-to-populate / When-NOT / Empty-case rules. The on-disk
shape only:

````markdown
### design-questions

```yaml
- title: <one-line problem statement>
  target-issue: "#<N>"
  context: |
    <one-paragraph context note>
```
````

## `design/state.md` update — exact commands (ADR-035, ADR-048)

Rewrite each zone with the deterministic splicer rather than editing markers
by hand:

```
bin/fence replace --file design/state.md --dialect state --zone in-flight    --body-file <tmp>
bin/fence replace --file design/state.md --dialect state --zone next-action  --body-file <tmp>
```

- `in-flight` body: keep `Issue` and `Prompt`, set `Branch` to the current
  branch, set `Status: verified`.
- `next-action` body (ADR-048): `skill: pr-review-packager`, `args: n/a`,
  `preconditions: ["branch <name> is ahead of main"]`, `blocked-by: none`.
  Skip this zone entirely if the file predates it.
- The `recent` zone is never touched here — it tracks merged PRs and belongs
  to `/pr-review-packager`.
- A broken fence makes `bin/fence` exit 1 instead of writing; report the
  broken zone in the evaluation summary's follow-ups and suggest `/pause`. An
  absent `design/state.md` is skipped silently.

## Receipts — exact commands (ADR-050)

The skill records an idempotency receipt keyed by the **issue number**
([`docs/receipts.md`](../../docs/receipts.md)):

- **Before** branch/commit work:
  `bin/write-receipt --find --skill claude-issue-executor --key <issue>` (or
  read `.claude/receipts/claude-issue-executor__<issue>.json`). A `completed`
  receipt means the issue's work already landed — stop and report rather than
  re-run on a resumed session.
- **On completion**, write a `completed` receipt recording the branch and any
  PR in `outputs`. On an interrupted run, leave a `partial`/`failed` receipt
  whose `next-action` names what remains.
- Receipts are local, gitignored state; writing one is best-effort and never
  blocks the handoff.

## Edge cases and alignment

The full edge-case list (prompt not found, prompt malformed, dirty working
tree, branch already exists, plan denial, test failures, missing ADR/issue
numbers) and the seven-item alignment checklist live in the co-installed
[`reference.md`](../../skills/claude-issue-executor/reference.md). A worked
session driven by `prompts/issue-017-pr-review-packager.md` is in
[`example.md`](../../skills/claude-issue-executor/example.md).
