# Feature Ideas — Ledger

Append-only record of feature ideas that have shipped or been
dropped. Entries are moved here from `notes/feature-ideas.md` once
they reach a terminal status (`shipped` or `dropped`), so the active
file stays scannable.

For active ideas (status `idea`, `ready-for-adr`, or `adr-drafted`),
see [`notes/feature-ideas.md`](../notes/feature-ideas.md). The entry
format is documented there.

---

### 1. `CLAUDE.md` starter template

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-007](../design/adr/adr-007-claude-md-starter-template.md)

**Context / trigger:** `docs/install.md:102` states the template "will be added in Issue #4" and users currently hand-write a minimal `CLAUDE.md` from a stub. Worth confirming Issue #4 is still open and tracked before duplicating.

**Sketch of the idea:** Ship `templates/claude-md-template.md` with placeholders for project name, stack, workflow rules, and GitHub conventions, rendered during install per `docs/install.md:96-104`.

**Options in mind:** Static template with `{{placeholders}}`; interactive skill that prompts for values; adopt a community template and trim.

**Open questions:** Is Issue #4 still the tracking issue? What fields are mandatory vs optional? Should it differ for solo vs small-team projects?

**Consequences to think through:** Removes a documented "stub" gap; needs periodic refresh as kit conventions evolve.

**Dependency note:** Unblocks the installer script (which renders this template) and the `workflow-docs` skill (which reads it).

---

---

### 2. Dedicated `prompts/` folder for issue session briefs

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-008](../design/adr/adr-008-dedicated-prompts-folder.md)

**Context / trigger:** Filled issue prompts (`issue-N-prompt.md`) currently live in `notes/` alongside freeform working notes, making `notes/` a mixed bag that's hard to scan. The prompts are structured, numbered session briefs — they deserve their own space.

**Sketch of the idea:** Move filled issue prompts into a dedicated `prompts/` directory at project root (or `design/prompts/` to group with PRDs/ADRs). Use richer naming mirroring the ADR convention: `issue-NNN-short-title.md`. Keep the blank template as `prompts/_template.md`. `notes/` reverts to freeform working notes only.

**Options in mind:**
- `prompts/` at project root — clean separation, easy to find.
- `design/prompts/` — groups all structured planning artifacts under one tree (PRD → ADR → prompt traceability in one place).
- Keep in `notes/prompts/` subfolder — minimal change, but `notes/` still owns the namespace.

**Open questions:** Does moving prompts out of `notes/` break any existing skill references? Should the install step scaffold `prompts/` alongside `design/adr/` and `notes/`? Does `docs/repo-structure.md` need a v2 revision to reflect the new layout?

**Consequences to think through:** Easier: scanning session briefs without wading through scratch notes; naming convention gives at-a-glance context. Harder: target project layout changes — `docs/repo-structure.md`, install guide, and README all need updating. Maintenance: one more directory to scaffold on install.

**Dependency note:** Must be decided before `/prepare-issue` and `claude-issue-executor`, which write to and read from this location.

---

---

### 3. Installer script

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-009](../design/adr/adr-009-installer-script.md)

**Context / trigger:** `docs/install.md:169` explicitly flags "an installer script" as a Phase 2 candidate. Current install is a documented `mkdir -p` + `cp -R` flow users run manually (`README.md:71-76`); friction scales with how often users set up new projects.

**Sketch of the idea:** Ship a small script (e.g. `bin/install-workflow-kit`) that runs the copy steps, scaffolds `design/adr/`, `prompts/`, and `notes/`, renders `CLAUDE.md` from the template, and makes the initial commit. Keep the manual flow documented as a fallback so nothing is hidden.

**Options in mind:** Bash script in the kit repo; a one-liner `curl | bash`; a setup skill the user runs after a minimal manual copy; do nothing.

**Open questions:** What language (bash vs node)? Where does it live in the kit? Does it need a `--with-docs` flag once that exists?

**Consequences to think through:** Easier onboarding; one more script to maintain and test across macOS/Linux; risk of hiding steps users should understand on first install.

**Dependency note:** Depends on `CLAUDE.md` template (#1) and `prompts/` folder decision (#2) to know what to scaffold.

---

---

### 4. Optional `--with-docs` flag on install

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-010](../design/adr/adr-010-optional-with-docs-flag.md)

**Context / trigger:** The install currently copies only `skills/` (and later `CLAUDE.md`) into the target project. `docs/` explains how the kit itself works — useful to some users who want it local and searchable in their project, unnecessary for users who prefer to read it in the source repo.

**Sketch of the idea:** Add an optional `--with-docs` step (or flag, once an installer script exists) that copies `docs/` into the target project under e.g. `docs/workflow-kit/`. Default: off. Document it as an opt-in line in `docs/install.md` and the README quick start.

**Options in mind:**
- Opt-in flag, default off — lean install, docs available on request.
- Always copy docs — zero-decision install, but duplicates content into every project.
- Never copy docs — current behaviour; users read the source repo.

**Open questions:**
- Target path inside the project: `docs/workflow-kit/` (namespaced) vs top-level `docs/` (risk of collision with the project's own docs)?
- Should the copied docs be pinned to the kit version at install time, or refreshed on re-install?
- Does this warrant an ADR, or is it small enough to add as a documented install option?

**Consequences to think through:**
- Easier: offline/in-repo access to kit docs for users who want it; helpful for teams onboarding to the workflow.
- Harder: docs drift — copied docs can fall behind the source repo between kit updates.
- Maintenance: one more install permutation to test and document.

**Dependency note:** Extension of the installer script (#3). Decide alongside it or immediately after.

---

---

### 5. `issue-planner` skill

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-011](../design/adr/adr-011-issue-planner-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:87` as a skill that should exist in target projects, but has no source in `skills/`. After `/prd-to-mvp` produces the MVP spec and build-out plan, users currently create GitHub issues manually. No existing GitHub issue tracks this skill.

**Sketch of the idea:** A skill that reads `design/mvp.md` and `design/build-out-plan.md`, generates a set of GitHub issues via `gh issue create`, each referencing the relevant ADR(s), tagged with labels, and assigned to the appropriate milestone. Bridges the gap between planning output and execution backlog.

**Options in mind:** Skill that creates issues directly via `gh`; skill that drafts issue markdown files for review before creation; hybrid that drafts, lets user approve, then creates.

**Open questions:** How to handle re-runs — skip existing issues, update them, or error? Should it create milestones too? How tightly should issue structure follow the build-out plan phases?

**Consequences to think through:** Easier: eliminates manual issue creation; ensures consistent issue format and ADR linkage. Harder: automated issue creation is hard to undo if the output is wrong. Maintenance: must stay in sync with `issue-template.md` and the build-out plan format.

**Dependency note:** First skill in the execution chain. GitHub Projects integration (#6) extends this.

---

---

### 6. GitHub Projects integration

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-012](../design/adr/adr-012-github-projects-integration.md)

**Context / trigger:** The kit tracks work via milestones + labels + issues but has no integration with GitHub Projects (the kanban board feature). Users get a flat issue list with no visual workflow view of status across milestones. GitHub Projects provides Todo → In Progress → Done columns, custom fields, and board/table views out of the box.

**Sketch of the idea:** Extend the `issue-planner` skill (or add a companion step) to create a GitHub Project via `gh project create`, configure status columns matching the kit's workflow phases, and add generated issues to the board. Optionally set custom fields for ADR references and milestone phase. Could also be a standalone `/setup-project` skill that runs once after issue creation.

**Options in mind:**
- Bake into `issue-planner` — issues land on the board as they're created (recommended, lowest friction).
- Standalone `/setup-project` skill — creates the board and imports existing issues (more flexible, works retroactively).
- Document-only — tell users how to set it up manually, no automation.

**Open questions:** Should the board be per-milestone or one board for the whole project? Which default columns — Todo/In Progress/Done, or something matching the kit's phases (Planning/Implementation/Review/Shipped)? Does `gh project` support everything needed, or are there API gaps?

**Consequences to think through:** Easier: visual workflow tracking without leaving GitHub; natural complement to milestones and labels. Harder: GitHub Projects API via `gh` is newer and less stable than issues/milestones; adds another resource to manage. Maintenance: board structure must stay in sync with the workflow model; if phases change, columns need updating.

**Dependency note:** Extends `issue-planner` (#5). Could share an ADR about the issue management model.

---

---

### 7. `/prepare-issue` skill for auto-filling issue prompts

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-013](../design/adr/adr-013-prepare-issue-skill.md)

**Context / trigger:** Users currently fill the issue prompt template manually — copying context from the GitHub issue body, linked ADRs, and the build-out plan phase into the blank form. This is repetitive, error-prone, and the biggest friction point between "issue exists" and "Claude Code session is briefed."

**Sketch of the idea:** A `/prepare-issue` skill that takes a GitHub issue number, pulls the issue body and linked ADR(s) via `gh`, reads the relevant build-out plan phase from `design/build-out-plan.md`, auto-fills the prompt template, and writes the result to `prompts/issue-NNN-short-title.md`. Optionally outputs the filled prompt ready for direct use in a Claude Code session.

**Options in mind:**
- Skill that writes the file and prints it (recommended — leaves session start to the user).
- Skill that writes the file and immediately starts execution (more opinionated, less control).
- Script instead of skill — loses Claude Code integration but works outside Claude.

**Open questions:** How does the skill resolve "linked ADRs" — parse issue body for `ADR-NNN` references, or require explicit input? Should it validate that the issue exists and is open before proceeding? Does it depend on the `prompts/` folder idea landing first, or should it work with the current `notes/` layout too?

**Consequences to think through:** Easier: eliminates manual copy-paste; enforces consistent prompt quality; closes the gap in the skill chain between `issue-planner` and `claude-issue-executor`. Harder: adds a runtime dependency on `gh` being authenticated (already a prerequisite). Maintenance: needs to stay in sync with the prompt template format — if the template changes, the skill must update.

**Dependency note:** Depends on `prompts/` folder decision (#2). Reads issues created by `issue-planner` (#5). Output consumed by `claude-issue-executor` (#8).

---

---

### 8. `claude-issue-executor` skill

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-014](../design/adr/adr-014-claude-issue-executor-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:89` as a skill for target projects, but no source exists in `skills/`. This is the execution counterpart to `/prepare-issue` — once the prompt is filled, this skill drives the actual Claude Code implementation session. No GitHub issue tracks it.

**Sketch of the idea:** A skill that takes a prepared issue prompt (from `prompts/issue-NNN-*.md`), enters plan mode, proposes an implementation plan for approval, then executes: creates a feature branch, implements incrementally with commits referencing the ADR and issue, writes tests alongside code, and produces an evaluation summary at the end. Enforces the plan-first, test-alongside discipline from ADR-006.

**Options in mind:** Full orchestration skill (recommended — strongest enforcement of the execution model); lightweight skill that just sets up the branch and context then hands off to the user; no skill, rely on the prompt alone (current v1 approach).

**Open questions:** How much autonomy should the skill have — full auto-implement or pause-at-each-step? Should it call `/prepare-issue` first if no prompt file exists? How does it handle failures mid-session (partial commits, failing tests)?

**Consequences to think through:** Easier: consistent, disciplined execution sessions; less user judgment needed on workflow steps. Harder: over-automation risks — users may lose understanding of what's happening. Maintenance: tightly coupled to the execution model in ADR-006; changes there require skill updates.

**Dependency note:** Depends on `/prepare-issue` (#7) output. Could share an ADR with `/prepare-issue` about the execution model extension.

---

---

### 9. `pr-review-packager` skill

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-015](../design/adr/adr-015-pr-review-packager-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:89` as a target project skill, but no source in `skills/`. After implementation, users manually create PRs and fill the PR template. No GitHub issue tracks it. Note: overlaps with Claude Code's built-in `/review` skill, but serves a different purpose — packaging the PR rather than reviewing it.

**Sketch of the idea:** A skill that, after implementation is complete on a feature branch: creates a PR via `gh pr create`, fills the PR body from `templates/pr-template.md` with the correct `Closes #N`, ADR references, and a summary of changes, and optionally runs a self-review checklist before submission. Completes the workflow from "code done" to "PR ready for review."

**Options in mind:** Skill that creates the PR end-to-end (recommended); skill that drafts the PR body for review then creates on approval; leave it manual and rely on the PR template alone.

**Open questions:** Should it run tests before creating the PR? Should it invoke `/review` as a pre-flight check? How does it determine which issue to link — from the branch name, the prompt file, or user input?

**Consequences to think through:** Easier: consistent, well-linked PRs every time; enforces the traceability chain (commit → issue → ADR). Harder: automated PR creation is visible to collaborators immediately — mistakes are public. Maintenance: must stay in sync with `pr-template.md` format.

**Dependency note:** Consumes output of `claude-issue-executor` (#8). Independent of changelog/release skills below.

---

---

### 10. Auto-generated changelog / release notes skill

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-016](../design/adr/adr-016-changelog-and-release-notes-skill.md)

**Context / trigger:** V1's commit convention (`<verb> <what> (ADR-NNN, #issue)`) makes `git log` highly readable, but there's no way to produce a polished changelog or release notes for stakeholders who don't use git. A maintained commit log would drift from reality; an auto-generated one stays accurate with zero upkeep.

**Sketch of the idea:** Add a `/changelog` skill (or script) that parses git history between two refs (e.g. tags, SHAs, or "since last release"), groups commits by verb/ADR/issue, and outputs a formatted changelog or release notes document. Leverages the existing commit message format — no new conventions required.

**Options in mind:** Claude Code skill that reads `git log` and formats output; a standalone shell script; a GitHub Action that generates release notes on tag push; all three layered.

**Open questions:** Output format — markdown file committed to repo, GitHub Release body, or both? Should it filter out chore/refactor commits by default? How does it handle squash-merged PRs where individual commits are lost?

**Consequences to think through:** Easier: stakeholder-ready release communication with no manual writing; validates that the commit convention is being followed (bad messages produce bad changelogs). Harder: squash merges and rebases can break the git-history-as-source assumption. Maintenance: minimal — the skill reads existing data rather than maintaining state.

**Dependency note:** Independent of the execution chain. `/release` (#11) depends on this.

---

---

### 11. `/release` skill for version tagging and GitHub Releases

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-017](../design/adr/adr-017-release-skill.md)

**Context / trigger:** The kit has no skills for versioning, releasing, or tagging. Projects built with the kit reach "merge to main" but have no structured path from there to a tagged release with release notes. The `/changelog` skill (also logged) generates the content, but there's nothing to orchestrate the actual release.

**Sketch of the idea:** A `/release` skill that: determines the next semver version (based on ADR impact or user input), runs the `/changelog` skill to generate release notes, creates a git tag, pushes it, and creates a GitHub Release via `gh release create`. Optionally updates `design/build-out-plan.md` phase status to mark a milestone as shipped. Could also define a semver convention section in `CLAUDE.md` or the workflow guide (e.g. new ADR = minor, superseded ADR = potentially major, bug fixes = patch).

**Options in mind:**
- Full skill that handles tag + changelog + GitHub Release end-to-end (recommended).
- Lightweight script that just tags and delegates release notes to `/changelog`.
- Document the convention only and leave execution manual.

**Open questions:** Should the skill auto-determine the version bump from commit/ADR analysis, or always prompt the user? Does it depend on `/changelog` landing first, or should it have its own minimal release-notes generation? How does it interact with the build-out plan milestones — one release per milestone, or independent?

**Consequences to think through:** Easier: closes the workflow loop from idea to shipped release; pairs naturally with `/changelog`. Harder: semver decisions are judgment calls — automating them risks incorrect bumps. Maintenance: must stay in sync with `/changelog` output format and `gh release` API changes.

**Dependency note:** Depends on `/changelog` (#10). Final step in the delivery chain.

---

---

### 12. `workflow-docs` skill

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-018](../design/adr/adr-018-workflow-docs-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:88` as the skill that generates `README.md` and `design/ai-summary.md` for target projects. No source exists in `skills/`, and no GitHub issue tracks it.

**Sketch of the idea:** A skill that reads the project's PRD, MVP spec, ADRs, and `CLAUDE.md` to generate a project `README.md` (from `templates/`) and `design/ai-summary.md` (from `templates/ai-summary-template.md`). Should be re-runnable to refresh docs as the project evolves.

**Options in mind:** Single skill generating both files; two separate skills (one per doc); fold into the installer script as a post-install step.

**Open questions:** When should this run — once at project setup, or after every major ADR change? Should it diff against existing README content to avoid clobbering manual edits?

**Consequences to think through:** Easier: target projects get polished docs from day one without manual writing. Harder: generated README may not match the project's voice or tone. Maintenance: templates need to evolve with the kit.

**Dependency note:** Reads `CLAUDE.md` (#1) and ADRs. Can be built independently but best specified after the full skill set is known.

---

---

### 13. Write `docs/claude-code-guide.md`

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-019](../design/adr/adr-019-claude-code-guide.md)

**Context / trigger:** `docs/install.md:154` references `docs/claude-code-guide.md` as "a later issue" — it's already promised to users reading the install guide but doesn't exist yet.

**Sketch of the idea:** Write the missing doc covering how to actually use Claude Code with the kit — plan mode, skill invocation via `/skill-name`, the approve-then-implement loop, common pitfalls. Pitch: the connective tissue between "install completed" and "first skill run."

**Options in mind:** Single doc (recommended); fold it into the planned `docs/workflow-guide.md`; leave it at per-skill `SKILL.md` files and drop the reference.

**Open questions:** Does it overlap with the planned workflow guide? Should it assume Claude Code familiarity or start from zero?

**Consequences to think through:** Closes a known documentation gap; one more doc to keep in sync as Claude Code itself evolves.

**Dependency note:** Best written after skills (#5-#11) are built so it can reference real skill names and behaviours.

---

---

### 14. End-to-end workflow guide doc

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-020](../design/adr/adr-020-workflow-guide.md)

**Context / trigger:** Users installing the kit can see the pieces (skills, templates, ADRs) but there's no single doc that walks through the full flow the kit creates end-to-end. `docs/install.md:214` already references a planned `docs/workflow-guide.md` ("end-to-end flow from idea to deploy — coming in a later issue"), and `generic-project-workflow.md` at the repo root (~29 KB) looks like source material waiting to be distilled.

**Sketch of the idea:** Add `docs/workflow-guide.md` covering one pass of the happy path: idea → PRD (via `idea-to-prd` / `prd-normalizer`) → MVP scope (`prd-to-mvp`) → ADRs (`adr-writer`) → GitHub issues → feature branches → PRs → merge. Link into it from the README and `docs/install.md`. Use `generic-project-workflow.md` as the raw source and trim to the 80% case. Must include a "when you don't need an ADR" section — the issue template (`templates/issue-template.md:15`) supports ADR-less issues via an HTML comment, but nothing else in the workflow acknowledges this path. The guide should explicitly cover bug fixes, chores, dependency bumps, CI/CD tweaks, and doc improvements as legitimate ADR-free work that still flows through the same issue → branch → PR → merge process.

**Options in mind:**
- One time-boxed guide covering the happy path only (recommended).
- Multi-doc split (one per phase: planning, implementation, review, release) — more thorough but heavier to maintain.
- Leave it at the skill-level `SKILL.md` files — lightest, but users lack a connective narrative.

**Open questions:**
- Where does `generic-project-workflow.md` live once the guide is written — delete, archive under `notes/`, or keep as an appendix?
- Does the guide belong in the kit's own `docs/` (about the kit), or should a trimmed copy also land in target projects so teams have a local reference?
- Should each phase link to the exact skill that drives it, for direct `/skill-name` invocation from inside the guide?

**Consequences to think through:**
- Easier: new users get a single source of truth for how the kit's pieces fit together; reduces "which skill do I run next?" friction.
- Harder: one more doc to keep in sync as skills evolve — guide can drift from reality.
- Maintenance: needs a review pass whenever a skill's interface changes or an ADR supersedes another.
- Deferred: phase-specific deep dives, troubleshooting flows, and team/multi-repo variants — explicitly out of scope for v1 of this doc.

**Dependency note:** The capstone doc — should be written last, after all skills and structural decisions are final, so it describes the real workflow.

---

---

### 15. Example / starter projects gallery

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-021](../design/adr/adr-021-example-projects.md)

**Context / trigger:** `examples/` currently covers the three PRD intake paths but no full worked projects. New users lack end-to-end references showing the kit in use from install to shipped PR.

**Sketch of the idea:** Add a handful of small, complete example projects (e.g. CLI utility, simple web app, data pipeline) with full histories — PRDs, ADRs, issues, PRs — so users can trace the whole flow.

**Options in mind:** In-repo under `examples/`; separate companion repo linked from the README; curated list of external projects using the kit.

**Open questions:** In-repo bloat vs discoverability tradeoff? Who owns keeping examples current?

**Consequences to think through:** Strong onboarding aid; examples rot as the kit evolves; repo size grows meaningfully if kept in-tree.

**Dependency note:** Needs the full v-next workflow (skills + docs) to exist before examples can demonstrate it end-to-end.

---

---

### 16. PRD template for external-LLM drafting

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-027](../design/adr/adr-027-prd-template.md)

**Context / trigger:** `templates/` ships `mvp-template.md`, `build-out-plan-template.md`, `adr-template.md`, `issue-template.md`, `pr-template.md`, `claude-md-template.md`, `ai-summary-template.md`, `readme-template.md` — but no `prd-template.md`. Users who draft PRDs in external LLMs (Perplexity, ChatGPT) have no paste-in skeleton matching the kit's canonical 11-field shape from `skills/prd-normalizer/SKILL.md:46-63`. Only `examples/standard-prd-example.md` hints at shape, and it's an 8-section illustrative example rather than a reusable template. A provisional `templates/prd-template.md` was added locally to unblock drafting today, ahead of formalization — this entry records the work that's still owed.

**Sketch of the idea:** Ship `templates/prd-template.md` with `{{UPPER_SNAKE}}` placeholders matching the 11 canonical fields (product name, one-line description, problem, target users, goal, user stories, core capabilities, non-goals, constraints and preferences, success signals, open questions). Document the flow: paste the template into an external LLM → get a filled PRD → save to `design/prd.md` → run `prd-normalizer` (near-no-op if filled faithfully). Update `templates/README.md` index and add a reference from `docs/install.md` or the forthcoming `docs/workflow-guide.md` (#14).

**Options in mind:**
- 11-field canonical shape (recommended — closest to `prd-normalized.md`, fast-path through the normalizer).
- 8-section standard shape matching `examples/standard-prd-example.md` — more familiar to users with prior PRD experience but forces a full normalization pass.
- Ship both shapes with guidance on when to use each.
- Do nothing — users derive shape from the example.

**Open questions:** Does the template duplicate enough of `examples/standard-prd-example.md` that the example should be trimmed or cross-linked? Should the template ship with an accompanying "prompt for your LLM" snippet that briefs the external model on the format and hard-required fields? Does `prd-normalizer` need a fast-path for inputs already in the canonical shape (treat as pass-through after self-check)?

**Consequences to think through:** Easier — lower friction for users who draft PRDs in external LLMs; downstream skills receive cleaner inputs. Harder — one more template to keep in lockstep with `prd-normalizer`'s canonical field list; drift would silently break the fast-path. Maintenance — low: a static skeleton with placeholder hints, versioned alongside the normalizer's field list.

**Dependency note:** Independent of the execution-chain skills (#5–#11). Consumed as input by the already-shipped `prd-normalizer`. Best referenced from `docs/workflow-guide.md` (#14) once that lands. Does not block any other entry.

---

---

### 18. License selection and `LICENSE` file

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-19
**ADR:** [ADR-025](../design/adr/adr-025-license.md)

**Context / trigger:** The repo has no `LICENSE` file and the README currently says "not yet specified" (added 2026-04-19 alongside v2.0.0). GitHub visibly flags missing licenses on the repo homepage, and without one the default copyright applies — downstream users technically cannot redistribute, modify, or fork the kit. For a kit whose whole purpose is to be installed into other projects, this is a soft blocker on external adoption. Separately: target projects scaffolded via the installer also ship without a license, pushing the same problem one layer down.

**Sketch of the idea:** Pick a license for the kit itself, add `LICENSE` at repo root, and update the README to reference it. Consider whether the installer (ADR-009) should optionally scaffold a `LICENSE` into target projects too — either a fixed default (MIT) or a `--license=<spdx>` flag that renders the appropriate template from `templates/licenses/`.

**Options in mind:**
- **MIT for the kit** — shortest, most permissive, matches most developer-tooling repos. One `LICENSE` file, no template plumbing.
- **Apache-2.0 for the kit** — permissive + explicit patent grant + NOTICE file convention. Slightly heavier but safer for anything that might ship code rather than docs.
- **GPL-3.0 for the kit** — copyleft; forces downstream derivatives to stay open. Likely over-scoped for a workflow toolkit.
- **No license, state explicitly "all rights reserved"** — current behaviour in effect; keep closed until ready.
- **Add license scaffolding for target projects** — separate decision, can pair with any choice above via `bin/install-workflow-kit --license=MIT` and `templates/licenses/mit.txt` etc.

**Open questions:** MIT or Apache-2.0 for the kit itself? Should the installer scaffold a `LICENSE` into target projects at all, or leave that choice to the user? If it does, is there a default, or is `--license` required? Does the kit-level license choice constrain target-project license choices (it shouldn't for permissive licenses, but worth confirming)? Where does copyright attribution live — a single author line or a `CONTRIBUTORS` file?

**Consequences to think through:** Easier: unblocks external sharing and adoption; removes GitHub's "missing license" banner; answers a question every serious user will ask within minutes of opening the repo. Harder: once chosen and shipped, changing the license later requires coordinating with anyone who has redistributed the kit. Maintenance: near-zero for the kit itself (one file); if installer scaffolds target licenses, that's one template per supported license to keep current.

**Dependency note:** Independent of other v-next entries. Should land before any public announcement or external contribution campaign. Interacts with #17 (Strong README template) — the README License section is already placeholder-linked to this entry.

---

---

### 20. Auto-sync `design/adr/README.md` index

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-26
**ADR:** [ADR-023](../design/adr/adr-023-auto-sync-adr-index.md)

**Context / trigger:** The ADR index in `design/adr/README.md` has drifted out of sync with the filesystem repeatedly — at one point listing only ADR-001 through ADR-006 while the directory contained 21 ADRs. Index drift means readers can't find ADRs by title or check status without scanning the directory directly. Status transitions (e.g., supersession) compound the problem: ADR-002 was superseded by ADR-022 and the index needed a manual update for the new row. Today, every ADR add or status change requires the author to also edit the README.

**Sketch of the idea:** A `bin/sync-adr-index` regenerator that scans `design/adr/adr-*.md`, parses title and status from each, and rewrites a marker-fenced (`<!-- adr-index:start -->` / `<!-- adr-index:end -->`) region of `design/adr/README.md`. Editorial text outside the fence is preserved. The script is idempotent and ships with the kit so target projects get the same behaviour. The ADR-touching skills (`adr-writer`, `claude-issue-executor`, `pr-review-packager`, `release`) call it before commit/PR/tag. Optional belt-and-braces: a git pre-commit hook installed by `install-workflow-kit` that runs the script if any `design/adr/adr-*.md` is staged.

**Options in mind:**
- **Skill-level only** — only adr-writer regenerates. Simple, but skips manual-edit and out-of-band cases.
- **Script + skill integrations** — recommended. Deterministic, reusable, idempotent. Catches the common Claude-driven paths.
- **Script + skill integrations + git hook** — adds a backstop for manual commits where Claude isn't involved. Hooks are bypassable (`--no-verify`) and fragile across machines, so this is belt-and-braces, not load-bearing.
- **Generated whole-file README** — fully regenerated each run; manual editorial cannot live in the file. Rejected: the index already coexists with explanatory prose.

**Open questions:** Should the script also detect and warn about supersession cycles or orphaned `superseded by ADR-NNN` references? Should it sort by ADR number only, or group by status (accepted, superseded, deprecated)? Does the optional git hook get installed by default or behind a flag?

**Consequences to think through:** Easier: index drift becomes structurally impossible for skill-driven flows; ADR adds and status changes don't need a separate manual edit. Harder: a small script to maintain; if its parser breaks the regeneration is wrong silently (mitigation: idempotent + diffable + run in CI). Maintenance: marker fences must stay intact in the README. The script is shell-only, no new runtime deps.

**Dependency note:** Touches several existing skills (`adr-writer`, `claude-issue-executor`, `pr-review-packager`, `release`) and `bin/install-workflow-kit`. No prior ADR blocks this; it implements a hygiene rule on top of ADR-005 (documentation architecture).

---

---

### 21. Replace MVP "v1" vocabulary with version-neutral language

**Status:** shipped
**Target:** v-next
**Captured:** 2026-04-26
**ADR:** [ADR-024](../design/adr/adr-024-mvp-vocabulary-versus-v1.md)

**Context / trigger:** The kit's MVP scoping framework uses "In v1 / Not in v1" as the canonical headings — appearing in `templates/mvp-template.md`, `templates/readme-template.md`, the `prd-to-mvp` / `idea-to-prd` / `prd-normalizer` skills, `issue-planner`, `workflow-docs`, and example projects. ADR-022 just removed kit-self "v1" qualifiers because they were misleading after the kit shipped v2.0.0. The same wording survives in the MVP framework with a different meaning ("the target project's first release"), and a reader can reasonably ask whether the two uses should align. There is also a collision risk: a target project at its own v2 still has "In v1" headings in its MVP doc.

**Sketch of the idea:** Decide whether to keep the current MVP vocabulary as-is (it's a deliberate scoping device, not a kit-version leak) or rebrand to version-neutral phrasing — e.g., `In MVP / Not in MVP`, `In scope / Out of scope`, `Initial release / Deferred`. A rebrand touches ~7 skills, 3 templates, the example projects, and any CHANGELOG/README references; backwards compat for already-installed kits would need a migration note.

**Options in mind:**
- **Keep "In v1 / Not in v1"** — recommended. The framing is well-understood, integrates with PRD → MVP → issue planning naming, and parallels common SaaS/product practice. The "v1" here is the project's first cut, not a kit version.
- **`In MVP / Not in MVP`** — clearest about *what* it is (MVP scope), no version-shaped collision. Slight redundancy ("MVP" already in the file/section names).
- **`In scope / Out of scope`** — most generic, works for non-MVP scoping too. Loses the "first cut, more later" connotation that "v1" gives.
- **`Initial release / Deferred`** — explicit about the temporal axis. Wordier in headings.

**Open questions:** If we rebrand, do we migrate existing target-project MVP docs or just change going forward? Does the term need to match whatever appears in the PRD template (currently uses "v1" too)? Is there a survey of how downstream users actually use these headings before changing?

**Consequences to think through:** Keep: zero migration work, vocabulary is stable, but the cosmetic confusion-with-kit-version persists for new readers. Rebrand: cleaner separation, but touches a lot of files; existing example-project text needs updating; old installed kits drift from the new convention until rebuilt.

**Dependency note:** Standalone. If accepted, sequence after ADR-022 (already shipped) so the kit-self cleanup is the precedent for the MVP-vocab cleanup.

---

---

### 22. More detailed planning workflow

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-031](../design/adr/adr-031-deeper-planning-workflow.md)

**Context / trigger:** The current planning chain (`idea-to-prd` → `prd-normalizer` → `prd-to-mvp` → `adr-writer` → `issue-planner`) produces a working backlog quickly, but for non-trivial projects the depth of planning between "MVP scoped" and "issues created" is thin. There's no structured place for: deeper requirements decomposition, risk/assumption logs, sequencing rationale beyond a flat build-out plan, or a research/spike phase before ADRs are drafted. A reference repo will be supplied with patterns worth borrowing.

**Sketch of the idea:** Introduce an optional, deeper planning layer between MVP scoping and ADR drafting. Possible artefacts: a structured planning doc (requirements, risks, assumptions, sequencing), a research/spike skill that captures findings before they harden into ADRs, and a richer build-out plan format that can express phased delivery (see #23). Skill(s) would be opt-in for larger projects so small ones still get the lightweight current flow.

**Options in mind:**
- **New `/planning` skill that produces a `design/planning.md`** sitting between `mvp.md` and `adr-writer` — captures requirements decomposition, risks, assumptions, open questions, and sequencing rationale.
- **Extend `prd-to-mvp`** to optionally emit a deeper planning section rather than a separate skill — fewer skills, but conflates two concerns.
- **A research/spike skill** that produces `design/spikes/NNN-topic.md` for areas needing investigation before an ADR can be written.
- **Adopt patterns from a reference repo** the user will supply — defer specifics until reviewed.

**Open questions:** What's the canonical artefact name and shape — single `planning.md` or a small directory? Does it replace, augment, or live alongside `build-out-plan.md`? At what project size does the extra step pay for itself? Should `issue-planner` learn to read it, or stay sourced from `mvp.md` + `build-out-plan.md` only? Which patterns from the reference repo are worth importing wholesale vs adapting?

**Consequences to think through:** Easier — large projects get a structured gap-filler between scoping and execution; risks/assumptions are first-class instead of buried in ADR context; spikes have a home. Harder — one more optional artefact and skill to teach; risk of process bloat for small projects; must stay opt-in. Maintenance — templates and skills have to stay aligned with whatever planning shape is chosen; downstream skills (`adr-writer`, `issue-planner`) may need to read the new artefact.

**Dependency note:** Pairs naturally with #23 (implementation phases) — phased delivery is one of the things a deeper planning layer should be able to express. Reference repo to be supplied; review before committing to a shape.

---

---

### 23. Implementation phases in PRD review and planning

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-032](../design/adr/adr-032-implementation-phases.md)

**Context / trigger:** Today's flow treats the MVP as a single scope cut: everything is either `In scope` or `Out of scope`, and `build-out-plan.md` is a flat list of work. For large projects, that's too coarse — useful work often falls into multiple ordered phases (e.g. foundation → core feature → polish → scale), each potentially with its own ADRs and acceptance criteria. There's no first-class place to express "this is in scope, but it's phase 2, not phase 1," and `issue-planner` has nothing to key milestones off beyond the flat plan.

**Sketch of the idea:** Add explicit implementation-phase structure to the PRD-review and planning artefacts. `prd-to-mvp` (or a new planning skill, see #22) would produce a phased build-out plan: each phase has a name, goal, scope bullets, the ADRs it depends on, and an exit criterion. ADRs can be tagged with the phase they belong to, so `adr-writer` and the index know which phase a decision serves. `issue-planner` reads phases and creates GitHub milestones (one per phase), assigning issues accordingly. Small projects keep using a single implicit phase — the structure is opt-in via a `--phases` flag or by the user filling phase headings in the template.

**Options in mind:**
- **Phases in `build-out-plan.md`** — extend the existing template with `## Phase N: <name>` sections; least disruption, reuses the artefact users already know.
- **Separate `design/phases.md`** — phases as a first-class doc; cleaner separation but adds another file.
- **Phases as a field on ADRs and issues only** — no new artefact, just metadata; lightest, but loses the narrative "what each phase is for."
- **Phases captured during PRD review** (in `prd-normalizer` / `prd-to-mvp`) so they're decided early rather than retrofitted onto the build-out plan.

**Open questions:** Where do phases live canonically — PRD, MVP doc, build-out plan, or a new file? Are phases strictly ordered or can they overlap? Should each phase produce its own release (ties to `/release` and the changelog)? How does this interact with GitHub milestones (one milestone per phase = recommended starting point)? Does `workflow-docs` surface phases in the generated README/roadmap section?

**Consequences to think through:** Easier — large projects get an honest delivery plan with explicit gates; ADRs and issues inherit phase context for traceability; release planning has a natural unit. Harder — more shape to learn for users with small projects (mitigation: opt-in / single-phase default); existing skills (`prd-to-mvp`, `issue-planner`, `workflow-docs`, `release`) all need phase-awareness; example projects need a phased version. Maintenance — phase metadata has to stay consistent across PRD, plan, ADRs, issues, milestones; drift between them silently breaks the traceability chain.

**Dependency note:** Pairs with #22 (deeper planning workflow) — phases are a likely output of that planning layer. Touches `prd-to-mvp`, `adr-writer`, `issue-planner`, `workflow-docs`, and `/release`. Decide alongside #22 so the artefact shape is settled before skills learn to read it.

---

---

### 24. `discuss-phase` style clarification step before ADRs

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-033](../design/adr/adr-033-clarify-step.md)

**Context / trigger:** Inspired by the GSD project's [`discuss-phase`](https://github.com/gsd-build/get-shit-done/blob/main/commands/gsd/discuss-phase.md) command, which surfaces "gray areas" — undecided implementation questions — before the planner runs, so downstream agents don't stall on ambiguity. Today our kit jumps from MVP scoping straight to `adr-writer`, which means ambiguity gets resolved either inside ADR drafts (mixing decisions with discovery) or during issue execution (too late, costs a session). A focused clarification step would catch the gray areas earlier.

**Sketch of the idea:** A `/clarify` (or `/discuss-scope`) skill that reads the current `design/prd-normalized.md` and `design/mvp.md`, scouts the codebase (if any), and surfaces a checklist of unresolved implementation questions for user selection and deep-dive resolution. Output is appended to a `design/decisions.md` (or per-phase `design/phases/N-context.md` if #23 lands) capturing settled decisions in a form ADR-writer and issue-planner can consume without re-asking. Skips areas already locked by accepted ADRs.

**Options in mind:**
- **New `/clarify` skill** that produces `design/decisions.md`, run between `prd-to-mvp` and `adr-writer` — recommended, narrow scope, opt-in.
- **Extend `prd-to-mvp`** to emit a clarification section — fewer skills but conflates scoping with decision capture.
- **Per-phase clarification** tied to #23, producing `design/phases/N-context.md` per phase — more structured but blocked on the phase shape.
- **Do nothing** — keep relying on ADRs to surface ambiguity. Cheap but leaves the gap.

**Open questions:** Does this artefact graduate into ADRs once a decision is hardened, or stay as standing context? How does it interact with the existing ADR supersession model — clarifications are below ADR-weight by design? Should it be re-runnable to add gray areas as they're discovered mid-project, or one-shot per planning round?

**Consequences to think through:** Easier — ADRs stay decision-only; planner and executor have a single place to look for "what was settled informally"; reduces context-window pressure during execution. Harder — one more artefact and skill; risk of duplication with ADRs if the line isn't drawn cleanly. Maintenance — small: append-only doc, no parser dependencies.

**Dependency note:** Stands alone; complements #22 (deeper planning) and #23 (phases) but doesn't depend on either. Best landed before #22 so the deeper-planning skill can build on a clarified scope.

---

---

### 25. Plan-checker quality gate for ADRs and issue prompts

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-034](../design/adr/adr-034-plan-checker.md)

**Context / trigger:** Inspired by GSD's [`gsd-plan-checker`](https://github.com/gsd-build/get-shit-done/blob/main/agents/gsd-plan-checker.md) agent, which validates a phase plan on 8 dimensions (atomicity, requirements coverage, dependencies, context fit, etc.) and iterates up to 3 times until pass. Our kit produces ADRs (via `adr-writer`) and issue prompts (via `prepare-issue`), but neither has a structured quality check before they're accepted. Bad ADRs and thin prompts are caught only at execution time, when the cost of fixing them is highest.

**Sketch of the idea:** A `/check-plan` skill (or a `--check` flag on `adr-writer` / `prepare-issue`) that runs a checklist against the artefact: ADR has clear context/decision/consequences, references the right ADRs, doesn't conflict with accepted ones; issue prompt has acceptance criteria, links the right ADRs, fits the build-out plan phase, scope is single-PR-sized. Returns a pass/fail with specific revisions needed. Iterates with the user (or autonomously, capped at 3 rounds) until pass.

**Options in mind:**
- **Standalone `/check-plan` skill** invoked by users or chained from `adr-writer` and `prepare-issue` — recommended, reusable.
- **Inline check inside each producing skill** — simpler call site, but couples the checker to each producer.
- **Two checkers** (one for ADRs, one for prompts) — more focused criteria but doubles the surface.
- **Linter-style script** instead of a skill — fast, deterministic on structural rules, but can't reason about content quality.

**Open questions:** What's the right dimension list for ADRs vs prompts (GSD's 8-dim list is plan-specific)? How many iteration rounds before giving up? Should the checker block commit/PR if it fails, or just warn? Where do failed-and-revised drafts live — overwrite or version?

**Consequences to think through:** Easier — fewer execution-time surprises; ADR/prompt quality stops depending on the author's discipline; new kit users get scaffolding-grade quality from day one. Harder — slower drafting loop (mitigation: cap iterations, allow `--skip-check`); checklist drift if ADR/prompt templates evolve without updating the checker. Maintenance — checklist criteria need a source of truth that ages with the templates.

**Dependency note:** Hooks into `adr-writer` and `prepare-issue`. Independent of #22/#23 but pairs naturally — phased plans (#23) are obvious targets for a checker.

---

---

### 26. `STATE.md` and session-continuity artefacts for long projects

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-035](../design/adr/adr-035-state-md-session-continuity.md)

**Context / trigger:** Inspired by GSD's `STATE.md` (current position: which phase, plans completed, blockers), `HANDOFF.json`, and `continue-here.md` artefacts. Today our kit relies entirely on git state, GitHub issue status, and the prompt files in `prompts/` to convey "where are we?" That's enough for a fresh session on a single issue, but for projects spanning many issues and phases, it leaves the user (and any new Claude session) reconstructing context from scratch every time. No cross-session memory beyond what's in git.

**Sketch of the idea:** Ship a small `design/state.md` (or `notes/state.md`) that captures: current phase (if #23 lands), in-flight issues, recently completed work, known blockers, and a "continue here" pointer to the next prompt. Updated by `/prepare-issue` (sets the in-flight issue), `claude-issue-executor` (marks progress), and `pr-review-packager` (closes out an issue). A companion `/resume` skill reads it and briefs the next session. Optional `/pause` skill writes a richer handoff for context-window-exhausting sessions.

**Options in mind:**
- **Single `design/state.md` updated by existing skills** — recommended, lightweight, reuses skills already in the chain.
- **Standalone `/resume` and `/pause` skills** with no shared state file — simpler but loses the cross-skill traceability.
- **Per-issue state in `prompts/issue-NNN-state.md`** — granular but fragmented; harder to see "the project's overall position."
- **Do nothing** — keep relying on git + issue board. Cheap but limits the kit's usefulness on multi-month projects.

**Open questions:** Does `state.md` get committed (audit trail) or gitignored (per-developer scratchpad)? How does it stay in sync if multiple sessions touch it? Is this redundant with GitHub Projects (#6) once a board exists? What's the minimum field set — phase + in-flight issue + last-PR is probably enough.

**Consequences to think through:** Easier — fresh sessions catch up in seconds, not minutes; project status visible at a glance without `gh` calls; pause/resume across context resets has a clean home. Harder — drift if updates aren't enforced; risk of becoming a stale mirror of GitHub. Maintenance — small if append-only; bigger if it tries to be a single source of truth.

**Dependency note:** Touches `prepare-issue`, `claude-issue-executor`, `pr-review-packager`. Pairs with #23 (phases) — `state.md` becomes much more useful when there's phase context to track. Could be a thin v0 (just current-issue + last-completed) before #23 lands, then enriched.

---

---

### 27. Granularity / density control for phased plans

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-036](../design/adr/adr-036-granularity-control.md)

**Context / trigger:** Inspired by GSD's `granularity` setting (`coarse` 3-5 phases, `standard` 5-8, `fine` 8-12) on `new-project`. Without an explicit knob, phase decomposition becomes a judgment call that varies project-to-project, making example projects and the workflow guide harder to write consistently. A small modifier on #23 (implementation phases) lets users dial the planning depth to match project size.

**Sketch of the idea:** When #23 lands, give `prd-to-mvp` (or the deeper planning skill from #22) a `--granularity={coarse|standard|fine}` flag that targets phase count. `coarse` for small projects (one or two phases is fine), `standard` for typical multi-month builds, `fine` for large scope where each phase wants its own milestone. Default: `standard`. The choice is recorded in `build-out-plan.md` so re-runs and downstream skills are consistent.

**Options in mind:**
- **Three-tier `--granularity` flag** — recommended, matches GSD, easy to teach.
- **Free-form `--phases=N`** — exact control but harder to recommend defaults.
- **Auto-pick from project size** (e.g. issue count estimate) — clever but unreliable on the first pass.
- **No knob** — let the user shape phases manually after seeing the default. Simplest; maybe sufficient.

**Open questions:** Does granularity also affect issue density per phase (more phases = fewer issues each)? Is the right default different for software vs non-software projects (the kit is workflow-agnostic per ADR-028)? Does this need its own ADR or fold into #23's?

**Consequences to think through:** Easier — example projects and the workflow guide can prescribe defaults; users get sane starting points without designing the phase shape themselves. Harder — one more option to document; risk of users tuning granularity instead of fixing real scope issues. Maintenance — minimal; just a parameter passed through skills.

**Dependency note:** Modifier on #23 (implementation phases). Lands as a follow-up, not a blocker. Could be deferred entirely if #23 ships with a single sensible default.

---

---

### 28. Milestone lifecycle commands (audit, summary, complete)

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-037](../design/adr/adr-037-milestone-lifecycle.md)

**Context / trigger:** Inspired by GSD's `audit-milestone`, `milestone-summary`, and `complete-milestone` commands, which formalize the boundary between phases and treat a milestone as a first-class delivery unit. Our kit's closest analogue is `/release`, but a release covers a tag-and-publish step, not the wider "did we actually finish what this milestone promised?" check. If #23 (phases) lands, milestones become the natural multi-phase grouping — and need lifecycle ops of their own.

**Sketch of the idea:** Three small skills layered on top of #23: `/audit-milestone` (verifies all phases in the milestone are complete, all issues closed, all ADRs referenced have linked PRs); `/milestone-summary` (generates a milestone retrospective: what shipped, ADRs adopted, lessons learned, deferred work); `/complete-milestone` (closes the milestone, archives the milestone-scoped state, optionally invokes `/release`). Acts as the bridge between phase-level execution and project-level releases.

**Options in mind:**
- **Three discrete skills** as above — recommended; each is small and composable.
- **Single `/finish-milestone` skill** that does audit + summary + complete in sequence — fewer commands but less composable.
- **Fold into `/release`** — simplest but conflates "milestone done" with "release tagged" (they may differ — e.g. multiple milestones per release).
- **Manual checklist in the workflow guide** — no automation, just docs. Cheap but abandons the kit's automation principle.

**Open questions:** Is one milestone == one release the default, or are they decoupled? Where does the milestone summary live — `design/milestones/N-summary.md`, the GitHub milestone description, or both? Does `/audit-milestone` block `/complete-milestone` on failure, or just warn?

**Consequences to think through:** Easier — large projects get visible delivery checkpoints; retrospectives become routine artefact, not a manual exercise; release notes have richer source material. Harder — three more skills to maintain; only valuable if #23 (phases) and milestone groupings actually exist. Maintenance — tightly coupled to whatever milestone shape #23 settles on.

**Dependency note:** Depends on #23 (implementation phases) for the milestone concept. Pairs with `/release` (no overlap; `/release` cuts the tag, these manage the multi-phase scope above). Defer until #23 ships and at least one project has run a real milestone end-to-end.

---

---

### 29. Tighten the prompt step: auto-chain into executor, allow `--no-prompt` for trivial issues

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-038](../design/adr/adr-038-tighten-prompt-step.md)

**Context / trigger:** The kit's per-issue prompt artefact (`prompts/issue-NNN-*.md`, ADR-008 + ADR-013) is a load-bearing piece of the audit trail and the natural anchor for several v-next ideas (#25 plan-checker, #26 state.md). But a fair question came up — is the prompt strictly necessary now that Claude Code has plan mode? Honest read: dropping it loses the per-session brief (which ADRs apply, which build-out-plan phase, acceptance criteria, scope boundary, clarifications gathered post-ADR), the audit trail (one prompt per issue, committed alongside the work), and the re-runnable-with-the-same-brief property. The cost is already near-zero thanks to `/prepare-issue` auto-filling from the issue + ADRs + plan. So the right move is to keep the artefact and lower its ceremony, not remove it.

**Sketch of the idea:** Two small changes:
1. **Auto-chain `/prepare-issue` into `claude-issue-executor`** so the prompt is a side effect of starting work, not a separate command. The executor checks for `prompts/issue-NNN-*.md`; if absent, calls `/prepare-issue` first; if present and stale (issue body changed since), regenerates with confirmation.
2. **`--no-prompt` mode on the executor** for one-line bug fixes, chores, dependency bumps, CI tweaks, doc fixes — the ADR-less path the workflow guide already acknowledges (`templates/issue-template.md:15`). Skips prompt generation, runs from the issue body alone. Documented criteria for when this is appropriate (single-PR scope, no design decisions, no ADR linkage).

**Options in mind:**
- **Both changes together** — recommended; reduces ceremony for trivial work, preserves discipline for ADR-driven work.
- **Auto-chain only** — keeps the artefact mandatory; cheapest change but doesn't address the "this is overkill for a typo fix" case.
- **`--no-prompt` only** — leaves the manual two-step (`prepare` then `execute`) for everyone else.
- **Replace the prompt with prompt-mode-only** — strips out the artefact entirely. Rejected: loses the audit trail, the session-rerun guarantee, and the anchor for #25 / #26.

**Open questions:** What counts as "stale" for prompt regeneration — issue-body changed, linked ADR changed, or both? Does `--no-prompt` work need to leave any breadcrumb (e.g. a one-line note in the commit) for traceability? Should `--no-prompt` be opt-in by user flag, or auto-detected when the issue lacks ADR references?

**Consequences to think through:** Easier — fewer manual steps for the common case; trivial issues stop carrying ADR-shaped ceremony; prompt artefact remains the anchor for downstream features. Harder — auto-chain hides a step users may want to see (mitigation: log the prep step prominently); `--no-prompt` is a slippery slope if its criteria aren't tight (mitigation: documented checklist). Maintenance — small; both changes live inside `claude-issue-executor` and only touch its argument handling.

**Alignment note for the ADR:** When this graduates to an ADR, explicitly check the prompt step is still pulling its weight against everything else landing in v-next — #22 (deeper planning), #23 (phases), #24 (clarify), #25 (plan-checker), #26 (state.md), #28 (milestone lifecycle). The prompt is the connective tissue between ADRs and execution; if any of those features start producing artefacts that overlap with what the prompt captures (e.g. phase-context files from #23, decisions doc from #24), the prompt's content shape should be revisited so the kit isn't carrying duplicate context across files.

**Dependency note:** Touches `claude-issue-executor` (ADR-014) and `prepare-issue` (ADR-013). Independent of #22/#23 but should be sequenced after the shape of #24 and #26 is at least sketched, so the prompt's content boundary is settled before this lands.

---

---

### 30. Require Claude Code plan mode (harness-level) for significant tasks in `claude-issue-executor`

**Status:** shipped
**Shipped:** v3.3.0
**Target:** v-next
**Captured:** 2026-04-30
**ADR:** [ADR-039](../design/adr/adr-039-plan-mode-for-significant-tasks.md)

**Context / trigger:** Today `claude-issue-executor` enforces "plan-first" via a chat-level protocol: it proposes a written plan and waits for explicit user approval before any mutating tool call. That's a *convention* the executor follows, not a *guarantee* the harness enforces. Claude Code also ships a harder mechanism — plan mode (toggled with shift+tab shift+tab) — that locks the assistant out of all mutating tools at the harness level until the user explicitly exits plan mode with approval. The two are complementary, but the kit currently only uses the soft one. During the v-next planning batch implementation, the user noted this gap and asked for the harder enforcement to become standard for "significant tasks."

**Sketch of the idea:** Update `skills/claude-issue-executor/SKILL.md` (and possibly `prepare-issue` or other gating skills) so plan mode is either entered automatically based on a documented "significant" checklist, OR the user is explicitly asked at session start whether to enter plan mode. The "significant" checklist: modifies 3+ files; edits a `skills/*/SKILL.md`; edits a `templates/*` file; edits `bin/*`; modifies `.claude/settings*.json`; or any other "blast radius beyond a single small fix" property. Trivial work (single typo, single-line doc tweak, status-line edit) explicitly opts out — plan mode is friction-positive there. Document the checklist in the skill and in the workflow guide so the criterion is shared between human and assistant.

**Options in mind:**
- **Auto-enter plan mode for significant tasks** — `claude-issue-executor` evaluates the checklist against the prompt's Scope section and enters plan mode without asking. Strongest enforcement, lowest friction once trusted.
- **Ask the user at session start** — `claude-issue-executor` opens the session by asking "Enter Claude Code plan mode for this task? (yes / no / decide for me based on scope)". Most transparent, preserves user control, accepts the friction of one extra interaction.
- **Hybrid: ask only when the checklist is borderline** — auto-enter for clearly-significant work, auto-skip for clearly-trivial work, ask only when the prompt's scope is ambiguous. Best of both, hardest to specify.
- **Update `claude-issue-executor` only** — the executor is the orchestrator; one place to teach the rule. Recommended.
- **Update both `claude-issue-executor` and `prepare-issue`** — `prepare-issue` is read-only with respect to GitHub, but writes a prompt file; arguably "significant" enough to gate. Likely overkill.
- **A standalone `/plan-mode-on` reminder skill** invoked from other skills — explicit but adds a layer.
- **No skill change, document the convention in the workflow guide only** — relies on author discipline. Lightest, but exactly the gap this entry exists to close.

**Open questions:** Where does the "significant" checklist live canonically — in `skills/claude-issue-executor/SKILL.md`, in `docs/workflow-guide.md`, or both with one as the source of truth? Does plan-mode entry happen *before* the chat plan gate (harness lock first, then proposed plan within the lock), or *as* the chat plan gate (the proposed plan IS the plan-mode plan)? How does this interact with `--no-prompt` mode from #29 — trivial issues should not pay plan-mode friction. Should the rule apply to `pr-review-packager` too? Probably yes for the `gh pr create` step.

**Consequences to think through:** Easier — harness-level enforcement removes a class of "I forgot to wait" failures; mistakes stop being convention-bound. Harder — plan mode adds friction even for medium-sized tasks; new contributors need to learn when it kicks in. Maintenance — the "significant" checklist must stay current as the kit grows; drift makes the rule fuzzy. Cross-skill coupling — multiple skills now reference the same checklist.

**Alignment note for the ADR:** This entry interacts with #29 (prompt-step tightening). The `--no-prompt` mode from #29 is precisely the trivial-issue case that *shouldn't* trigger plan mode. The two ADRs should be drafted with consistent criteria — the trivial-issue checklist should be a single source of truth referenced from both.

**Dependency note:** Touches `claude-issue-executor` (ADR-014). Pairs with #29. Independent of #22-#28 but useful at any point — could land before any of them.

---

---

### Feature ideas notepad

**Status:** shipped
**Captured:** 2026-04-16

**Context / trigger:** The workflow generator has skills for turning PRDs into MVPs and drafting ADRs, but no lightweight place between "rough thought" and "formal ADR." Ideas either get lost or force premature formality.

**Sketch of the idea:** A single `notes/feature-ideas.md` notepad where feature ideas are captured as short structured blocks whose fields align with `templates/adr-template.md`. When an idea is ripe, its block is handed to the `adr-writer` skill to produce a full ADR with minimal rework.
