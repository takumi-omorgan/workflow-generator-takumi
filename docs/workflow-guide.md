# Workflow Guide — Idea to Shipped Release

A practical walkthrough of the full Claude Code Workflow Kit flow, from a
rough idea to a tagged release. Follow this guide end-to-end the first
time you use the kit; after that, treat it as a cheat sheet.

**Who this is for:** a solo developer or small team who has installed
the kit into a new target project and wants to ship a feature without
piecing the flow together from individual skill docs.

**What you end up with:** a working, tested, merged feature on `main`
with an accompanying ADR, issue, PR, and (at milestone boundaries) a
tagged GitHub Release.

This guide is the condensed, action-oriented companion to the detailed
[`generic-project-workflow.md`](../generic-project-workflow.md). Where
the reference doc explains *why*, this guide focuses on *what to run
next*. Skills are referenced by their slash name (e.g. `/idea-to-prd`);
each one has its own `SKILL.md` under `.claude/skills/<name>/` in your
target project with the full interface spec.

---

## 1. Prerequisites

You should have already:

- Installed Git, GitHub CLI, and Claude Code, and authenticated `gh`.
- Created the target project on GitHub and cloned it locally.
- Copied the kit's skills into `.claude/skills/` and rendered
  `CLAUDE.md` at the project root.

If any of that is missing, stop here and complete
[`docs/install.md`](install.md) first. The rest of this guide assumes
you are sitting inside the target project's root with Claude Code open.

---

## 2. The happy path, one pass

One pass = one feature shipped. Steps (a) through (c) are usually done
once per MVP scoping round. Steps (d) through (g) loop per issue. Steps
(h) and (i) close out a release.

### 2.a From idea or PRD to MVP

Pick the skill that matches what you have in hand:

| You have… | Run | You produce |
|---|---|---|
| A rough idea, no doc | `/idea-to-prd` | A lightweight PRD in `Design/` |
| A standard or custom PRD | `/prd-normalizer` | A normalized PRD in the kit's internal format |
| A normalized PRD | `/prd-to-mvp` | An MVP scope statement: in-scope, out-of-scope, success signals |

Run them in sequence if you have a rough idea: `/idea-to-prd` →
`/prd-normalizer` (if you later want to reshape it) → `/prd-to-mvp`.

**What unblocks next:** a written MVP statement that scopes the first
release. You now know what decisions you need to lock in.

### 2.b Design decisions to ADRs

For each meaningful architectural choice surfaced by the MVP — a library
pick, an integration, a data model, a deployment target — write an ADR.

- **Run:** `/adr-writer`
- **What you see:** a drafted ADR in `Design/adr/adr-NNN-<short-title>.md`
  following the kit's template (context, options, decision, consequences).
- **What you produce:** one accepted ADR per decision.

One ADR per decision. If the skill drafts several, accept them one at a
time — each ADR should stand alone.

**What unblocks next:** a small set of accepted ADRs that define the
backlog's shape.

### 2.c Plan to backlog

Turn the MVP plus ADRs into a tracked GitHub backlog.

- **Run:** `/issue-planner`
- **What you see:** a batch of drafted issues (title, body, labels,
  milestone, ADR reference) presented for your approval before any are
  created.
- **What you produce:** GitHub issues created via `gh issue create`,
  plus a GitHub Project board (per ADR-012) organising them.

The skill is GitHub-first: issues live on GitHub, not in local files.
The Project board gives you a kanban view of the backlog.

**What unblocks next:** a list of issue numbers you can work through
one at a time.

### 2.d One issue at a time to a prompt

Before writing any code, generate a per-issue Claude Code session
prompt.

- **Run:** `/prepare-issue <issue-number>`
- **What you see:** the skill pulls the issue body and its linked ADR
  via `gh`, reads the relevant build-out plan section, and fills the
  prompt template.
- **What you produce:** `prompts/issue-NNN-<short-title>.md` (per
  ADR-008), ready to paste into a fresh Claude Code session.

This is a deliberate handoff — the prompt is written but execution
starts separately, so you get a review checkpoint between planning and
building.

**What unblocks next:** a prompt file you can kick off whenever you
have time to build.

### 2.e Prompt to implementation

Open a fresh Claude Code session and hand it the prompt.

- **Run:** `/claude-issue-executor <path-to-prompt>`
- **What you see:** the skill enters plan mode, proposes a step-by-step
  plan, and waits for your approval. Only after you approve does it
  create a feature branch and start implementing.
- **What you produce:** a branch with incremental commits (each
  referencing the ADR and issue number), tests written alongside code,
  and an evaluation summary at the end.

This is the plan-first execution model (ADR-006). The evaluation
summary is your quality gate — it lists files changed, test results,
and any manual verification steps. Do not skip reading it.

**Branch naming:** the skill creates branches following the kit's
convention (see [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)) —
e.g. `add-auth-middleware` or `NN-add-auth-middleware`.

**What unblocks next:** a working, tested branch ready for PR.

### 2.f Branch to PR

Package the branch into a reviewable pull request.

- **Run:** `/pr-review-packager`
- **What you see:** the skill drafts a PR body using the kit's PR
  template — summary, ADR link, file-level changelog, test results,
  `Closes #NN` trailer — and shows it to you before creating the PR.
- **What you produce:** a PR opened via `gh pr create`, with a clean
  body and the linked issue set to auto-close on merge.

For work that is not yet done, open as a draft PR (`gh pr create
--draft`) to get early feedback; convert with `gh pr ready <number>`
when implementation and tests are complete.

**What unblocks next:** a PR you can self-review and merge.

### 2.g Merge, then loop back

Review the diff on GitHub, resolve any CodeRabbit or human review
comments, then merge.

```bash
gh pr merge <number> --squash --delete-branch
git checkout main
git pull
```

- Squash merge is the default — it keeps `main`'s history clean.
- Use a regular merge only when the per-commit history of the branch
  carries real value.
- Delete the branch on merge so the repo stays tidy.

**Loop back to step 2.d** for the next issue. Keep going until the
milestone's issues are all merged.

### 2.h Tagged release

Once a milestone's issues are all merged to `main`, cut a release.

| Step | Run | Produces |
|---|---|---|
| 1. Draft release notes | `/changelog` | Markdown grouped by verb, ADR, and issue, written to stdout, `CHANGELOG.md`, or a GitHub Release body |
| 2. Tag and publish | `/release` | Semver-bumped annotated git tag, pushed to origin, GitHub Release created via `gh release create` |

`/release` calls `/changelog` internally, so you can run it directly
once you are happy with the tag and bump (patch / minor / major). It
can also mark the milestone phase complete in your build-out plan.

**What unblocks next:** a tagged, published release that stakeholders
can read and that future `/changelog` runs will pick up as the lower
bound.

### 2.i Docs sync

Before closing out the release, regenerate the docs that summarise the
current state of the project.

- **Run:** `/workflow-docs`
- **What you see:** the skill reads the PRD, MVP spec, accepted ADRs,
  and `CLAUDE.md`, then re-renders `README.md` and
  `Design/ai-summary.md` from the kit's templates.
- **What you produce:** an updated `README.md` and
  `Design/ai-summary.md` committed to `main`.

Re-run this whenever the project's shape has changed meaningfully — new
ADRs accepted, a major feature shipped, a pivot in scope. The `ai-summary.md`
in particular is what you paste into external AIs for second-opinion
design reviews.

---

## 3. When you don't need an ADR

Not every change is an architectural decision. Bug fixes, chores,
dependency bumps, CI/CD tweaks, and doc-only changes generally do not
warrant an ADR — forcing one creates ceremony without insight.

**ADR-free changes still follow the same GitHub flow:**

| Stage | ADR-driven work | ADR-free work |
|---|---|---|
| Decision | Write ADR, accept | Skip |
| Issue | `/issue-planner` or manually via `gh issue create` | Manually via `gh issue create` |
| Branch | Feature branch from `main` | Feature branch from `main` |
| Prompt | `/prepare-issue <N>` | `/prepare-issue <N>` (still fills the template; ADR section is marked "none") |
| Build | `/claude-issue-executor` | `/claude-issue-executor` |
| PR | `/pr-review-packager` | `/pr-review-packager` |
| Merge | `gh pr merge --squash` | `gh pr merge --squash` |

So: still need an issue. Still need a branch. Still need a PR. You just
skip `/adr-writer` and mark the ADR section of the issue as "none".

The kit's issue template explicitly supports this — see the HTML
comment under the `## ADR` heading in
[`templates/issue-template.md`](../templates/issue-template.md): *"If
no ADR applies, write 'none' and say why."*

**Examples of ADR-free work:**

| Change | Why no ADR |
|---|---|
| Bug fix in an existing module | Restoring intended behaviour, not deciding new architecture |
| Dependency version bump | Unless it forces a behaviour change, it's a chore |
| CI/CD tweak (add a lint step, change a runner) | Operational, not architectural |
| README typo fix, docs rephrasing | Doc-only |
| Refactor with no behaviour change | Unless it reshapes the architecture, it's cleanup |
| Config tweak (log level, timeouts) | Tuning, not deciding |

If you are unsure, err on the side of writing an ADR — they are cheap,
and a rejected ADR is still useful as a record of what was considered.
See `generic-project-workflow.md` §4.2 for the full "when to write an
ADR" table.

---

## 4. Where to go deeper

| You want to… | Go to |
|---|---|
| See the full reference workflow with every option and edge case | [`generic-project-workflow.md`](../generic-project-workflow.md) |
| Learn how to run Claude Code skills from inside a target project | `docs/claude-code-guide.md` (coming in a later issue) |
| Understand a specific skill's interface, inputs, and outputs | `.claude/skills/<name>/SKILL.md` in your target project, or [`skills/README.md`](../skills/README.md) in the kit |
| Revisit a design decision that shaped this workflow | [`Design/adr/`](../Design/adr/) |
| Set up GitHub labels, milestones, and branch protection | [`docs/github-setup.md`](github-setup.md) |
| Fill a Claude Code session prompt by hand | [`docs/issue-prompt-guide.md`](issue-prompt-guide.md) |

If the flow above doesn't match the skills you have installed, check
[`skills/README.md`](../skills/README.md) for the current inventory —
some skills land in later milestones and the guide lists the full v-next
set.
