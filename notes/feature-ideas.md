# Feature Ideas Notepad

Lightweight capture for feature ideas that may graduate into ADRs.

**How to use:**
- Entries are ordered by ADR dependency — foundational decisions first, then features that build on them.
- Keep entries short — a few sentences per field is plenty.
- When an idea is ripe, hand the block to the `adr-writer` skill to produce a full ADR in `docs/adr/` using `templates/adr-template.md`.
- Mark status inline: `idea` → `ready-for-adr` → `adr-drafted` (link the ADR) → `shipped` or `dropped`.
- Mark target inline: `v-next` (already a Phase 2 candidate or promised in docs) vs `future` (later consideration, bigger scope or reopens an ADR).

---

## Entry template

```markdown
### {{Short title}}

**Status:** idea
**Target:** v-next | future
**Captured:** {{YYYY-MM-DD}}

**Context / trigger:** {{What problem or opportunity prompted this? What's missing today?}}

**Sketch of the idea:** {{One paragraph on what it would look like.}}

**Options in mind:** {{Any alternatives worth weighing, or "TBD".}}

**Open questions:** {{What would you need to decide before writing the ADR?}}

**Consequences to think through:** {{Likely tradeoffs, things that get harder, maintenance burden.}}
```

---

## v-next Entries

Ordered by ADR dependency. Features later in the list depend on decisions made earlier.

### Layer 1: Foundational decisions

These change the target project's layout or core artifacts. Decide first — other features reference them.

---

### 1. `CLAUDE.md` starter template

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-007](../Design/adr/adr-007-claude-md-starter-template.md)

**Context / trigger:** `docs/install.md:102` states the template "will be added in Issue #4" and users currently hand-write a minimal `CLAUDE.md` from a stub. Worth confirming Issue #4 is still open and tracked before duplicating.

**Sketch of the idea:** Ship `templates/claude-md-template.md` with placeholders for project name, stack, workflow rules, and GitHub conventions, rendered during install per `docs/install.md:96-104`.

**Options in mind:** Static template with `{{placeholders}}`; interactive skill that prompts for values; adopt a community template and trim.

**Open questions:** Is Issue #4 still the tracking issue? What fields are mandatory vs optional? Should it differ for solo vs small-team projects?

**Consequences to think through:** Removes a documented "stub" gap; needs periodic refresh as kit conventions evolve.

**Dependency note:** Unblocks the installer script (which renders this template) and the `workflow-docs` skill (which reads it).

---

### 2. Dedicated `prompts/` folder for issue session briefs

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-008](../Design/adr/adr-008-dedicated-prompts-folder.md)

**Context / trigger:** Filled issue prompts (`issue-N-prompt.md`) currently live in `notes/` alongside freeform working notes, making `notes/` a mixed bag that's hard to scan. The prompts are structured, numbered session briefs — they deserve their own space.

**Sketch of the idea:** Move filled issue prompts into a dedicated `prompts/` directory at project root (or `Design/prompts/` to group with PRDs/ADRs). Use richer naming mirroring the ADR convention: `issue-NNN-short-title.md`. Keep the blank template as `prompts/_template.md`. `notes/` reverts to freeform working notes only.

**Options in mind:**
- `prompts/` at project root — clean separation, easy to find.
- `Design/prompts/` — groups all structured planning artifacts under one tree (PRD → ADR → prompt traceability in one place).
- Keep in `notes/prompts/` subfolder — minimal change, but `notes/` still owns the namespace.

**Open questions:** Does moving prompts out of `notes/` break any existing skill references? Should the install step scaffold `prompts/` alongside `Design/adr/` and `notes/`? Does `docs/repo-structure.md` need a v2 revision to reflect the new layout?

**Consequences to think through:** Easier: scanning session briefs without wading through scratch notes; naming convention gives at-a-glance context. Harder: target project layout changes — `docs/repo-structure.md`, install guide, and README all need updating. Maintenance: one more directory to scaffold on install.

**Dependency note:** Must be decided before `/prepare-issue` and `claude-issue-executor`, which write to and read from this location.

---

### Layer 2: Installation

How projects get set up. Depends on knowing the final layout from Layer 1.

---

### 3. Installer script

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-009](../Design/adr/adr-009-installer-script.md)

**Context / trigger:** `docs/install.md:169` explicitly flags "an installer script" as a Phase 2 candidate. Current install is a documented `mkdir -p` + `cp -R` flow users run manually (`README.md:71-76`); friction scales with how often users set up new projects.

**Sketch of the idea:** Ship a small script (e.g. `bin/install-workflow-kit`) that runs the copy steps, scaffolds `Design/adr/`, `prompts/`, and `notes/`, renders `CLAUDE.md` from the template, and makes the initial commit. Keep the manual flow documented as a fallback so nothing is hidden.

**Options in mind:** Bash script in the kit repo; a one-liner `curl | bash`; a setup skill the user runs after a minimal manual copy; do nothing.

**Open questions:** What language (bash vs node)? Where does it live in the kit? Does it need a `--with-docs` flag once that exists?

**Consequences to think through:** Easier onboarding; one more script to maintain and test across macOS/Linux; risk of hiding steps users should understand on first install.

**Dependency note:** Depends on `CLAUDE.md` template (#1) and `prompts/` folder decision (#2) to know what to scaffold.

---

### 4. Optional `--with-docs` flag on install

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-010](../Design/adr/adr-010-optional-with-docs-flag.md)

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

### Layer 3: Planning-to-execution bridge

These form a chain: issues are created → prompts are prepared → sessions are executed. Each depends on the prior step.

---

### 5. `issue-planner` skill

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-011](../Design/adr/adr-011-issue-planner-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:87` as a skill that should exist in target projects, but has no source in `skills/`. After `/prd-to-mvp` produces the MVP spec and build-out plan, users currently create GitHub issues manually. No existing GitHub issue tracks this skill.

**Sketch of the idea:** A skill that reads `Design/mvp.md` and `Design/build-out-plan.md`, generates a set of GitHub issues via `gh issue create`, each referencing the relevant ADR(s), tagged with labels, and assigned to the appropriate milestone. Bridges the gap between planning output and execution backlog.

**Options in mind:** Skill that creates issues directly via `gh`; skill that drafts issue markdown files for review before creation; hybrid that drafts, lets user approve, then creates.

**Open questions:** How to handle re-runs — skip existing issues, update them, or error? Should it create milestones too? How tightly should issue structure follow the build-out plan phases?

**Consequences to think through:** Easier: eliminates manual issue creation; ensures consistent issue format and ADR linkage. Harder: automated issue creation is hard to undo if the output is wrong. Maintenance: must stay in sync with `issue-template.md` and the build-out plan format.

**Dependency note:** First skill in the execution chain. GitHub Projects integration (#6) extends this.

---

### 6. GitHub Projects integration

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-012](../Design/adr/adr-012-github-projects-integration.md)

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

### 7. `/prepare-issue` skill for auto-filling issue prompts

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-013](../Design/adr/adr-013-prepare-issue-skill.md)

**Context / trigger:** Users currently fill the issue prompt template manually — copying context from the GitHub issue body, linked ADRs, and the build-out plan phase into the blank form. This is repetitive, error-prone, and the biggest friction point between "issue exists" and "Claude Code session is briefed."

**Sketch of the idea:** A `/prepare-issue` skill that takes a GitHub issue number, pulls the issue body and linked ADR(s) via `gh`, reads the relevant build-out plan phase from `Design/build-out-plan.md`, auto-fills the prompt template, and writes the result to `prompts/issue-NNN-short-title.md`. Optionally outputs the filled prompt ready for direct use in a Claude Code session.

**Options in mind:**
- Skill that writes the file and prints it (recommended — leaves session start to the user).
- Skill that writes the file and immediately starts execution (more opinionated, less control).
- Script instead of skill — loses Claude Code integration but works outside Claude.

**Open questions:** How does the skill resolve "linked ADRs" — parse issue body for `ADR-NNN` references, or require explicit input? Should it validate that the issue exists and is open before proceeding? Does it depend on the `prompts/` folder idea landing first, or should it work with the current `notes/` layout too?

**Consequences to think through:** Easier: eliminates manual copy-paste; enforces consistent prompt quality; closes the gap in the skill chain between `issue-planner` and `claude-issue-executor`. Harder: adds a runtime dependency on `gh` being authenticated (already a prerequisite). Maintenance: needs to stay in sync with the prompt template format — if the template changes, the skill must update.

**Dependency note:** Depends on `prompts/` folder decision (#2). Reads issues created by `issue-planner` (#5). Output consumed by `claude-issue-executor` (#8).

---

### 8. `claude-issue-executor` skill

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-014](../Design/adr/adr-014-claude-issue-executor-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:89` as a skill for target projects, but no source exists in `skills/`. This is the execution counterpart to `/prepare-issue` — once the prompt is filled, this skill drives the actual Claude Code implementation session. No GitHub issue tracks it.

**Sketch of the idea:** A skill that takes a prepared issue prompt (from `prompts/issue-NNN-*.md`), enters plan mode, proposes an implementation plan for approval, then executes: creates a feature branch, implements incrementally with commits referencing the ADR and issue, writes tests alongside code, and produces an evaluation summary at the end. Enforces the plan-first, test-alongside discipline from ADR-006.

**Options in mind:** Full orchestration skill (recommended — strongest enforcement of the execution model); lightweight skill that just sets up the branch and context then hands off to the user; no skill, rely on the prompt alone (current v1 approach).

**Open questions:** How much autonomy should the skill have — full auto-implement or pause-at-each-step? Should it call `/prepare-issue` first if no prompt file exists? How does it handle failures mid-session (partial commits, failing tests)?

**Consequences to think through:** Easier: consistent, disciplined execution sessions; less user judgment needed on workflow steps. Harder: over-automation risks — users may lose understanding of what's happening. Maintenance: tightly coupled to the execution model in ADR-006; changes there require skill updates.

**Dependency note:** Depends on `/prepare-issue` (#7) output. Could share an ADR with `/prepare-issue` about the execution model extension.

---

### Layer 4: Delivery

Post-implementation: packaging PRs, generating changelogs, cutting releases.

---

### 9. `pr-review-packager` skill

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-015](../Design/adr/adr-015-pr-review-packager-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:89` as a target project skill, but no source in `skills/`. After implementation, users manually create PRs and fill the PR template. No GitHub issue tracks it. Note: overlaps with Claude Code's built-in `/review` skill, but serves a different purpose — packaging the PR rather than reviewing it.

**Sketch of the idea:** A skill that, after implementation is complete on a feature branch: creates a PR via `gh pr create`, fills the PR body from `templates/pr-template.md` with the correct `Closes #N`, ADR references, and a summary of changes, and optionally runs a self-review checklist before submission. Completes the workflow from "code done" to "PR ready for review."

**Options in mind:** Skill that creates the PR end-to-end (recommended); skill that drafts the PR body for review then creates on approval; leave it manual and rely on the PR template alone.

**Open questions:** Should it run tests before creating the PR? Should it invoke `/review` as a pre-flight check? How does it determine which issue to link — from the branch name, the prompt file, or user input?

**Consequences to think through:** Easier: consistent, well-linked PRs every time; enforces the traceability chain (commit → issue → ADR). Harder: automated PR creation is visible to collaborators immediately — mistakes are public. Maintenance: must stay in sync with `pr-template.md` format.

**Dependency note:** Consumes output of `claude-issue-executor` (#8). Independent of changelog/release skills below.

---

### 10. Auto-generated changelog / release notes skill

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-016](../Design/adr/adr-016-changelog-and-release-notes-skill.md)

**Context / trigger:** V1's commit convention (`<verb> <what> (ADR-NNN, #issue)`) makes `git log` highly readable, but there's no way to produce a polished changelog or release notes for stakeholders who don't use git. A maintained commit log would drift from reality; an auto-generated one stays accurate with zero upkeep.

**Sketch of the idea:** Add a `/changelog` skill (or script) that parses git history between two refs (e.g. tags, SHAs, or "since last release"), groups commits by verb/ADR/issue, and outputs a formatted changelog or release notes document. Leverages the existing commit message format — no new conventions required.

**Options in mind:** Claude Code skill that reads `git log` and formats output; a standalone shell script; a GitHub Action that generates release notes on tag push; all three layered.

**Open questions:** Output format — markdown file committed to repo, GitHub Release body, or both? Should it filter out chore/refactor commits by default? How does it handle squash-merged PRs where individual commits are lost?

**Consequences to think through:** Easier: stakeholder-ready release communication with no manual writing; validates that the commit convention is being followed (bad messages produce bad changelogs). Harder: squash merges and rebases can break the git-history-as-source assumption. Maintenance: minimal — the skill reads existing data rather than maintaining state.

**Dependency note:** Independent of the execution chain. `/release` (#11) depends on this.

---

### 11. `/release` skill for version tagging and GitHub Releases

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-017](../Design/adr/adr-017-release-skill.md)

**Context / trigger:** The kit has no skills for versioning, releasing, or tagging. Projects built with the kit reach "merge to main" but have no structured path from there to a tagged release with release notes. The `/changelog` skill (also logged) generates the content, but there's nothing to orchestrate the actual release.

**Sketch of the idea:** A `/release` skill that: determines the next semver version (based on ADR impact or user input), runs the `/changelog` skill to generate release notes, creates a git tag, pushes it, and creates a GitHub Release via `gh release create`. Optionally updates `Design/build-out-plan.md` phase status to mark a milestone as shipped. Could also define a semver convention section in `CLAUDE.md` or the workflow guide (e.g. new ADR = minor, superseded ADR = potentially major, bug fixes = patch).

**Options in mind:**
- Full skill that handles tag + changelog + GitHub Release end-to-end (recommended).
- Lightweight script that just tags and delegates release notes to `/changelog`.
- Document the convention only and leave execution manual.

**Open questions:** Should the skill auto-determine the version bump from commit/ADR analysis, or always prompt the user? Does it depend on `/changelog` landing first, or should it have its own minimal release-notes generation? How does it interact with the build-out plan milestones — one release per milestone, or independent?

**Consequences to think through:** Easier: closes the workflow loop from idea to shipped release; pairs naturally with `/changelog`. Harder: semver decisions are judgment calls — automating them risks incorrect bumps. Maintenance: must stay in sync with `/changelog` output format and `gh release` API changes.

**Dependency note:** Depends on `/changelog` (#10). Final step in the delivery chain.

---

### Layer 5: Documentation and examples

Best written after the skills and structural decisions are settled, so the docs reflect what actually exists.

---

### 12. `workflow-docs` skill

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-17
**ADR:** [ADR-018](../Design/adr/adr-018-workflow-docs-skill.md)

**Context / trigger:** Referenced in `docs/repo-structure.md:88` as the skill that generates `README.md` and `Design/ai-summary.md` for target projects. No source exists in `skills/`, and no GitHub issue tracks it.

**Sketch of the idea:** A skill that reads the project's PRD, MVP spec, ADRs, and `CLAUDE.md` to generate a project `README.md` (from `templates/`) and `Design/ai-summary.md` (from `templates/ai-summary-template.md`). Should be re-runnable to refresh docs as the project evolves.

**Options in mind:** Single skill generating both files; two separate skills (one per doc); fold into the installer script as a post-install step.

**Open questions:** When should this run — once at project setup, or after every major ADR change? Should it diff against existing README content to avoid clobbering manual edits?

**Consequences to think through:** Easier: target projects get polished docs from day one without manual writing. Harder: generated README may not match the project's voice or tone. Maintenance: templates need to evolve with the kit.

**Dependency note:** Reads `CLAUDE.md` (#1) and ADRs. Can be built independently but best specified after the full skill set is known.

---

### 13. Write `docs/claude-code-guide.md`

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-019](../Design/adr/adr-019-claude-code-guide.md)

**Context / trigger:** `docs/install.md:154` references `docs/claude-code-guide.md` as "a later issue" — it's already promised to users reading the install guide but doesn't exist yet.

**Sketch of the idea:** Write the missing doc covering how to actually use Claude Code with the kit — plan mode, skill invocation via `/skill-name`, the approve-then-implement loop, common pitfalls. Pitch: the connective tissue between "install completed" and "first skill run."

**Options in mind:** Single doc (recommended); fold it into the planned `docs/workflow-guide.md`; leave it at per-skill `SKILL.md` files and drop the reference.

**Open questions:** Does it overlap with the planned workflow guide? Should it assume Claude Code familiarity or start from zero?

**Consequences to think through:** Closes a known documentation gap; one more doc to keep in sync as Claude Code itself evolves.

**Dependency note:** Best written after skills (#5-#11) are built so it can reference real skill names and behaviours.

---

### 14. End-to-end workflow guide doc

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-020](../Design/adr/adr-020-workflow-guide.md)

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

### 15. Example / starter projects gallery

**Status:** adr-drafted
**Target:** v-next
**Captured:** 2026-04-16
**ADR:** [ADR-021](../Design/adr/adr-021-example-projects.md)

**Context / trigger:** `examples/` currently covers the three PRD intake paths but no full worked projects. New users lack end-to-end references showing the kit in use from install to shipped PR.

**Sketch of the idea:** Add a handful of small, complete example projects (e.g. CLI utility, simple web app, data pipeline) with full histories — PRDs, ADRs, issues, PRs — so users can trace the whole flow.

**Options in mind:** In-repo under `examples/`; separate companion repo linked from the README; curated list of external projects using the kit.

**Open questions:** In-repo bloat vs discoverability tradeoff? Who owns keeping examples current?

**Consequences to think through:** Strong onboarding aid; examples rot as the kit evolves; repo size grows meaningfully if kept in-tree.

**Dependency note:** Needs the full v-next workflow (skills + docs) to exist before examples can demonstrate it end-to-end.

---

### 16. PRD template for external-LLM drafting

**Status:** ready-for-adr
**Target:** v-next
**Captured:** 2026-04-17

**Context / trigger:** `templates/` ships `mvp-template.md`, `build-out-plan-template.md`, `adr-template.md`, `issue-template.md`, `pr-template.md`, `claude-md-template.md`, `ai-summary-template.md`, `readme-template.md` — but no `prd-template.md`. Users who draft PRDs in external LLMs (Perplexity, ChatGPT) have no paste-in skeleton matching the kit's canonical 11-field shape from `skills/prd-normalizer/SKILL.md:46-63`. Only `examples/standard-prd-example.md` hints at shape, and it's an 8-section illustrative example rather than a reusable template. A provisional `templates/prd-template.md` was added locally to unblock drafting today, ahead of formalization — this entry records the work that's still owed.

**Sketch of the idea:** Ship `templates/prd-template.md` with `{{UPPER_SNAKE}}` placeholders matching the 11 canonical fields (product name, one-line description, problem, target users, goal, user stories, core capabilities, non-goals, constraints and preferences, success signals, open questions). Document the flow: paste the template into an external LLM → get a filled PRD → save to `Design/prd.md` → run `prd-normalizer` (near-no-op if filled faithfully). Update `templates/README.md` index and add a reference from `docs/install.md` or the forthcoming `docs/workflow-guide.md` (#14).

**Options in mind:**
- 11-field canonical shape (recommended — closest to `prd-normalized.md`, fast-path through the normalizer).
- 8-section standard shape matching `examples/standard-prd-example.md` — more familiar to users with prior PRD experience but forces a full normalization pass.
- Ship both shapes with guidance on when to use each.
- Do nothing — users derive shape from the example.

**Open questions:** Does the template duplicate enough of `examples/standard-prd-example.md` that the example should be trimmed or cross-linked? Should the template ship with an accompanying "prompt for your LLM" snippet that briefs the external model on the format and hard-required fields? Does `prd-normalizer` need a fast-path for inputs already in the canonical shape (treat as pass-through after self-check)?

**Consequences to think through:** Easier — lower friction for users who draft PRDs in external LLMs; downstream skills receive cleaner inputs. Harder — one more template to keep in lockstep with `prd-normalizer`'s canonical field list; drift would silently break the fast-path. Maintenance — low: a static skeleton with placeholder hints, versioned alongside the normalizer's field list.

**Dependency note:** Independent of the execution-chain skills (#5–#11). Consumed as input by the already-shipped `prd-normalizer`. Best referenced from `docs/workflow-guide.md` (#14) once that lands. Does not block any other entry.

---

### 17. Strong README template for target projects

**Status:** idea
**Target:** v-next
**Captured:** 2026-04-19

**Context / trigger:** `templates/readme-template.md` (shipped via ADR-018 `/workflow-docs`) covers the essentials — name, overview, scope, how-to-run, key decisions — but is minimal compared to widely-cited conventions like the [Standard README spec](https://github.com/RichardLitt/standard-readme) and [makeareadme.com](https://www.makeareadme.com). Projects using the kit get a functional README, not a polished OSS-quality one. GitHub also visibly flags missing License sections on the repo homepage.

**Sketch of the idea:** Enhance `templates/readme-template.md` (or ship a more opinionated `readme-strong-template.md` alongside) aligned with the Standard README spec. Add optional sections that `/workflow-docs` can fill when source data is available: badges row (license, CI status, version), features bullets (from MVP), roadmap (from build-out plan), contributing, license, acknowledgments. Keep section-omission behaviour so thin projects still get a clean README.

**Options in mind:**
- **Enhance in place** — one template, more optional sections. Simple, one source of truth.
- **Ship two variants** — minimal (current) and strong, selected via `/workflow-docs --template=strong` or installer flag.
- **Post-install tailoring skill** — follow-up skill asks the user which sections they want.

**Open questions:** One opinionated template or a choose-your-own-adventure? What's the right default — lean or full-featured? Include a demo-gif slot even though the kit can't generate one? Does `/workflow-docs` grow to read CI config for badge URLs, or stay artifact-only?

**Consequences to think through:** Easier: target projects look production-ready from day one; closes the "missing License" gap GitHub flags. Harder: more optional sections means more ways `/workflow-docs` can emit empty-ish output when source data is thin. Maintenance: convention-driven bits (badges, license format) drift over time, needs occasional template refresh.

**Dependency note:** Extends `/workflow-docs` (ADR-018). Compatible with the existing marker-based re-run safety.

---

## Future Entries

Features for consideration in later versions. Ordered by theme.

---

### Starter GitHub Actions CI/CD workflows

**Status:** idea
**Target:** future
**Captured:** 2026-04-17

**Context / trigger:** The kit scaffolds GitHub issues, PRs, labels, milestones, and templates into target projects but never sets up CI/CD automation. Target projects have no `.github/workflows/` directory — the automated pipeline that tests and validates PR code is entirely left to the user. For a "GitHub-first delivery workflow" kit, this is a notable gap.

**Sketch of the idea:** Offer a menu of starter GitHub Actions workflows by stack (Node, Python, Go, etc.) that the kit can scaffold into target projects under `.github/workflows/`. Each provides a basic test + lint pipeline triggered on PR and push to main. Alternatively, the workflow guide doc (already logged as v-next) could include a short "set up CI" section pointing users to GitHub's own starter workflow templates rather than shipping custom ones.

**Options in mind:**
- Stack-specific starter workflows shipped with the kit (most useful, most maintenance).
- Docs-only approach: point users to GitHub's built-in starter templates (lightest, no maintenance).
- A `/setup-ci` skill that asks the user their stack and generates a workflow file (middle ground).

**Open questions:** How many stacks to support? Does the kit become responsible for keeping workflows current as Actions runners and action versions evolve? Is this too opinionated for a stack-agnostic planning kit?

**Consequences to think through:** Easier: target projects get CI out of the box; completes the GitHub-first story. Harder: CI pipelines are heavily stack-dependent — generic templates risk being too thin or too opinionated. Maintenance: GitHub Actions versions and runner images evolve independently; starter workflows rot if not updated.

---

### Update / refresh command for installed kits

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** Once the kit is copied into a project, it's frozen at install time. As skills or templates evolve upstream, there's no mechanism to pull updates without manual re-copy — and manual re-copy risks clobbering local customizations.

**Sketch of the idea:** Provide a refresh command (script or skill) that diffs the project's `.claude/skills/` against the kit source, shows what changed, and applies updates with conflict prompts. Pairs naturally with the plugin-distribution idea, which would make this automatic.

**Options in mind:** Standalone refresh script; part of the installer script; only viable via the plugin model.

**Open questions:** How to detect user customization vs stale-upstream? Where does the "kit source" live post-install if the original clone is gone?

**Consequences to think through:** Keeps installed kits current; introduces a merge/conflict surface that didn't exist; may be subsumed by the plugin idea, so worth sequencing after that decision.

---

### Retrofit existing repositories

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** V1's largest exclusion per `README.md:18` and ADR-002. Clear user pull exists — teams with existing codebases want the workflow without starting over, and today they have no path.

**Sketch of the idea:** Add a retrofit flow (skill + docs) that inspects an existing repo, proposes a compatible install (`CLAUDE.md`, `Design/adr/`, `notes/` without overwriting), and maps existing docs/issues into the kit's structure. Would supersede ADR-002.

**Options in mind:** Opinionated retrofit that assumes certain repo conventions; conservative retrofit that only adds files; a separate companion kit scoped to retrofit.

**Open questions:** How much repo variation can a single skill handle? What's the minimum viable retrofit — just docs scaffolding, or also ADR extraction from existing design docs?

**Consequences to think through:** Unlocks a much larger user base; significant scope expansion; ADR-002 needs explicit supersession; testing matrix grows a lot.

---

### Distribute the kit as a Claude Code plugin

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** Current install is a documented multi-step `git clone` + `cp -R` flow (`README.md:71-76`, `docs/install.md:66-111`). Claude Code's plugin system offers `/plugin install …`, automatic updates, versioning, and marketplace discoverability — a much lower-friction path for users. The question is whether that distribution model is compatible with the kit's project-local identity.

**Sketch of the idea:** Package the `skills/` layer as a Claude Code plugin published via a marketplace repo, so users get skills + any future slash commands/hooks/MCP servers with a single `/plugin install` call. Keep project-local scaffolding (`CLAUDE.md`, `Design/adr/`, `notes/`, templates) as a separate setup skill the plugin provides — so the plugin distributes the *tools*, and the tools scaffold the *artifacts* into each new project.

**Options in mind:**
- Hybrid: plugin for skills, setup skill for project artifacts (recommended starting point).
- Full plugin: everything ships via the plugin, project-local copy model is dropped — directly supersedes ADR-001.
- Dual distribution: keep the documented copy flow *and* offer a plugin — maximum compatibility, doubles the surface to maintain.
- Do nothing: keep the copy flow, accept the friction.

**Open questions:**
- How do plugins handle per-project customization of skills? The project-local model today lets users edit `.claude/skills/` freely — does a plugin install preserve that?
- What's the marketplace story — self-hosted marketplace repo, or submit to an existing one?
- Should the plugin version be pinned per project (reproducibility) or always latest (convenience)?
- Does this need ADR-001 formally superseded, or can both models coexist under a new ADR?

**Consequences to think through:**
- Easier: one-command install; versioned updates; discoverability; new skills ship to existing users automatically.
- Harder: reopens ADR-001; introduces a dependency on Claude Code's plugin format and lifecycle; README and install guide need rewriting; terminology collision with the existing "One-time setup (per machine)" heading in `README.md:41`.
- Maintenance: marketplace repo to publish and version; plugin manifest to keep in sync with skill changes; potential need to support both install paths during a transition.
- Deferred: full migration of templates/ADRs/artifacts into the plugin model — start with skills, evaluate after one release cycle.

---

### Team / multi-repo features

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** V1 is explicitly solo-or-small-team, single-repo per `README.md:9-14` and `docs/install.md:171-172`. Larger teams need shared conventions, cross-repo ADR linking, and branch policies the kit doesn't address.

**Sketch of the idea:** Extend the kit with team-oriented primitives: shared-ADR references across repos, team-level `CLAUDE.md` fragments, branch-protection scaffolding, and PR templates tuned to review workflows.

**Options in mind:** Extend current kit with team flags; separate team-edition kit; stay out of scope.

**Open questions:** Where do team conventions live — a separate repo consumed by per-project installs? Does this require the plugin model to be viable?

**Consequences to think through:** Opens a larger market; introduces multi-repo state management the kit currently avoids; strong interaction with the plugin and retrofit ideas.

---

### Non-GitHub provider support (GitLab, Bitbucket)

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** V1 is GitHub-first per ADR-004 and `README.md:19-20`. Teams on GitLab or Bitbucket cannot adopt the kit as-is.

**Sketch of the idea:** Abstract the provider-specific parts (issue creation, PR creation, labels, CLI calls) behind a thin adapter layer and ship GitLab/Bitbucket adapters. Would supersede ADR-004.

**Options in mind:** Full adapter layer; provider-specific forks of the kit; stay GitHub-only and document the choice as permanent.

**Open questions:** Are `glab` and `bb` close enough to `gh` to share skill logic? What breaks first — the skills or the docs?

**Consequences to think through:** Broader reach; meaningful re-architecture of skills that hardcode `gh`; ongoing maintenance across three providers instead of one.

---

### Non-Claude AI tooling support

**Status:** idea
**Target:** future
**Captured:** 2026-04-16

**Context / trigger:** V1 targets Claude Code specifically per ADR-006 and `docs/install.md:176`. Users of Cursor, Aider, Copilot, or other tools can't use the skill-driven flow.

**Sketch of the idea:** Export skills into tool-agnostic prompt bundles that other assistants can consume, or provide adapters that re-implement skill semantics for the most common tools. Would supersede ADR-006.

**Options in mind:** Portable prompt export; per-tool adapters; stay Claude-only and lean into the Claude Code plugin path instead.

**Open questions:** What's the lowest-common-denominator skill spec that still produces useful output? Does this dilute the kit's identity as a Claude Code workflow?

**Consequences to think through:** Expands addressable users; weakens Claude Code-native advantages (plan mode, skills system); meaningful ongoing maintenance across AI tools that evolve independently.

---

## Shipped

---

### Feature ideas notepad

**Status:** shipped
**Captured:** 2026-04-16

**Context / trigger:** The workflow generator has skills for turning PRDs into MVPs and drafting ADRs, but no lightweight place between "rough thought" and "formal ADR." Ideas either get lost or force premature formality.

**Sketch of the idea:** A single `notes/feature-ideas.md` notepad where feature ideas are captured as short structured blocks whose fields align with `templates/adr-template.md`. When an idea is ripe, its block is handed to the `adr-writer` skill to produce a full ADR with minimal rework.
