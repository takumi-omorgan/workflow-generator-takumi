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

Ideas tagged for the next major release of the kit. Originally
organised by Layer (foundational decisions → installation → planning
→ delivery → docs); those layer headings were retired once their
entries shipped. New v-next entries can be appended directly here.

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

### 19. Split to public distribution repo at external release

**Status:** idea
**Target:** v-next
**Captured:** 2026-04-19

**Context / trigger:** Today the repo is a single public tree containing both user-facing assets (`skills/`, `templates/`, `bin/`, `docs/`, `examples/projects/`, README, CHANGELOG) and development-only artefacts (`Design/adr/`, `notes/`, MVP/build-out plan docs, transcripts). When the kit is ready to be announced externally, users shouldn't have to wade through the development history to find what they install. GitHub has no per-folder visibility, so splitting means two repos. Current plan: flip this repo private during development and publish the clean public repo at external-release time.

**Sketch of the idea:** Keep this repo (`workflow-generator`) private as the full development source of truth. Create a separate public repo (working title `workflow-kit`) containing only the user-facing paths: `skills/`, `templates/`, `bin/`, `docs/`, `examples/projects/`, `README.md`, `CHANGELOG.md`, `LICENSE`. A GitHub Action on tag push in this repo runs a sync job: checks out a fresh tree of the allowed paths, commits to the public repo's `main` with a "Release vX.Y.Z" message, tags it, and pushes. Users clone the public repo; the installer's hard-coded clone path in `README.md` and `docs/install.md` updates to point there. Issues and discussions on the public repo stay public-side; internal planning stays here.

**Options in mind:**
- **Two repos with a sync Action on tag push** — recommended. One-way flow, clean public history (one commit per release), full private history preserved here.
- **Subtree split via `git subtree split` / `git-filter-repo`** — preserves some file history in the public repo. More complex; multi-path splits need composition.
- **Single repo with `.gitattributes export-ignore`** — only affects `git archive` / source-tarball downloads. Files are still visible in the GitHub UI and to anyone who clones. Rejected because it's privacy-by-convention, not enforcement.
- **Release-asset-only distribution** — attach a tarball to each GitHub Release, repo stays private. Breaks the current clone-based install model.

**Open questions:** Which paths go to the public repo — just the four listed, or also `generic-project-workflow.md` and the ADR index (many projects publish their ADRs deliberately)? How are CHANGELOG entries authored — copied verbatim, or regenerated with public-facing links rewritten? Where do user-filed issues land (public repo, triaged manually into this one)? Does the sync Action publish pre-release tags (alpha/beta), or only stable? Does the public repo accept PRs, or is it output-only with contribution through this repo?

**Consequences to think through:** Easier: users see a pristine, minimal repo; internal ADRs, prompts, feature-ideas, and working notes stay in the development process, not in the distribution. Harder: one more repo to set up, one sync Action to maintain, tag-alignment between repos needs discipline (broken sync = version skew between dev tags and public tags). Maintenance: the sync Action is small (~50 lines) but any change to the public-paths list requires updating it. Ecosystem impact: external issues and stars accrue only on the public repo; this repo's issue tracker stays internal.

**Dependency note:** Blocked by #18 (License) — the public repo needs a license before external release. Interacts with the plugin-distribution future entry — if the kit later ships as a Claude Code plugin, the public repo becomes the plugin source rather than a clone-install target.

---

### 31. Cross-skill design-question carry-forward

**Status:** ready-for-adr
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** v3.3.0 baseline eval — research-tracker fixture (see `runs/kit-v3.3.0/baseline-verdict.md` § "Cross-skill chain handoff")

**Context / trigger:** Research-tracker demonstrated organically a property the kit aspires to but doesn't currently codify: **end-to-end design-coherence loop closure across the implementation skill chain**. On issues #4 + #5 (the depth-scaled note templates), the full round-trip happened: `/claude-issue-executor 4` raised two design-agreement questions in eval-summary follow-ups → `/pr-review-packager #16` preserved them in PR body's "Notes for #5" → `/prepare-issue 5` carried them into the prompt as a load-bearing section → `/claude-issue-executor 5` MADE both decisions with documented reasoning → `/pr-review-packager #17` surfaced the decisions in PR body with ✅ checkmarks. **Audit-trail-grade visibility — anyone reading the PR sequence can trace the design-coherence work.** This emerged from the kit's existing skill behaviors composing well; no skill-spec hook required it. Codifying it as a deterministic property (with skill-spec hooks for design-question carry-forward across the executor → packager → prepare-issue boundary) would promote this from happy-accident to kit promise.

**Sketch of the idea:** Add three skill-spec hooks across the implementation chain:

1. **`claude-issue-executor`** — eval-summary's "Follow-ups" section gains a structured `design-questions:` subfield (machine-readable list of open design-coherence questions raised during the issue, each with a target-issue reference). Skill spec requires populating it when the executor's plan touches a load-bearing constraint shared with another upcoming issue.
2. **`pr-review-packager`** — when generating the PR body, scans the executor's eval-summary for `design-questions:` entries; preserves them in a dedicated "Notes for #N" section in the PR body for each target issue. Already happens organically on research-tracker; making it spec-mandated removes the dependence on chain-aware authoring.
3. **`prepare-issue`** — when generating a prompt for issue #N, scans recently-merged PRs for "Notes for #N" sections; extracts and embeds them in a "Two design-agreement points carried forward from PR #M" subsection of the new prompt. Currently happens organically when `/prepare-issue` is run after the relevant PR merges; spec-mandate makes it deterministic.

**Options in mind:**

- **All three hooks together** — recommended; full chain-handoff loop deterministic. Strongest property.
- **`claude-issue-executor` + `pr-review-packager` only** (skip `prepare-issue` integration) — packager preserves the carry-forward in PR history, but operator-facing visibility ends there. Loses the deterministic propagation into the next issue's prompt.
- **Codify in CLAUDE.md / workflow guide only, no skill-spec change** — relies on author / assistant discipline to follow the pattern. Lightest, but exactly the gap this entry exists to close.
- **A standalone "design-coherence" skill** invoked from the chain — adds a layer; rejected as redundant with the existing skills' natural surface area for this work.

**Open questions:** What's the canonical schema for `design-questions:` entries — title + target-issue reference + one-paragraph context, or richer? How does this interact with `--no-prompt` mode from #29 (ADR-038) — `--no-prompt` issues skip `/prepare-issue` entirely, breaking the propagation. Probably acceptable since `--no-prompt` is for trivial issues that wouldn't have design-coherence questions anyway, but worth explicit. Should the propagation surface in `claude-issue-executor`'s plan-mode prompt itself, or only in the prompt artefact? How does this interact with #25 (plan-checker quality gate) — design-coherence checks would be a natural consumer of the structured `design-questions:` output.

**Consequences to think through:** Easier — design-coherence work that today depends on chain-aware authoring becomes deterministic regardless of who's at the keyboard; cross-issue continuity is operator-visible in PR history without needing manual notes-for-future-self. Harder — three skills now share a structured-data contract, which becomes load-bearing for cross-skill handoff; spec drift between the three would silently break the loop. Maintenance — the `design-questions:` schema is new shared surface area; needs a single source of truth (likely in the workflow guide) and changes require updates across three skill specs in lockstep. Also — over-eager population of `design-questions:` could clutter PR bodies on issues that don't actually have cross-issue design coupling; spec needs a clear "when to populate / when not to" rule.

**Alignment note for the ADR:** Likely supersedes or extends [ADR-038](../Design/adr/adr-038-tighten-prompt-step.md) (auto-chain). The existing auto-chain decision was about *whether* `/prepare-issue` runs automatically; this entry is about *what content* is plumbed through the chain. Likely sequenced after #25 (plan-checker) since plan-checker would consume the structured output.

**Dependency note:** Touches `claude-issue-executor` (ADR-014), `pr-review-packager` (ADR-026?), `prepare-issue` (ADR-013). Pairs with #29 (ADR-038), #25 (plan-checker). Independent of the milestone-lifecycle work (#28).

---

### 32. Auto-mode permission contract — close the strict-mode bypass loophole

**Status:** ready-for-adr
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** v3.3.0 baseline eval — F24 calibration trajectory across all three fixtures (see `runs/kit-v3.3.0/baseline-verdict.md` § "F-finding cluster status")

**Context / trigger:** ADR-039 (entry #30) shipped harness-level plan mode for significant tasks in `claude-issue-executor`. The v3.3.0 baseline eval calibrated F24 (the executor's plan-mode bypass under "auto mode") across three fixtures: HIGH severity on md-notes (silent bypass), MEDIUM on podcast-pipeline (session-context-dependent), LOW on research-tracker (bypass-but-self-reported in alignment check). **The trajectory is positive but the principle stands**: even at LOW severity, the kit should not allow auto-mode to silently substitute for an explicit operator gate on significant tasks. The same shape appears in F23 (`/pr-review-packager`'s strict-mode-vs-runtime mismatch) and would appear in any future skill with strict-mode contracts. The kit needs an **explicit "permission mode" specification**: what auto-mode is allowed to substitute for, what it isn't, and how operators authorize substitutions when permitted.

**Sketch of the idea:** Promote ADR-039's narrow plan-mode rule into a kit-wide permission contract spanning every skill with strict-mode gates. Two skill-spec changes:

1. **`claude-issue-executor`**: significant-task gate must be triggered by an explicit operator-set toggle, not by auto-mode classifier inference. If auto-mode is active, skill explicitly asks the operator at session start ("Enter plan mode for this task? yes / no / decide-from-scope") rather than auto-entering or auto-skipping. The "yes / decide-from-scope" branches use ADR-039's existing checklist; "no" requires the operator to acknowledge the bypass in writing in the skill's chat output (so the bypass is operator-acknowledged, not silent).
2. **`pr-review-packager`**: extend the same principle to the PR-creation gate. The skill currently asks for explicit yes regardless of auto-mode (which is correct — research-tracker confirmed this across 5 PRs). Codify that this is the canonical pattern for any skill with public/hard-to-reverse actions: auto-mode does NOT substitute for explicit approval on these surfaces.

Plus a documentation change:

3. **Workflow guide gains an "Auto-mode permission contract" section** that lists which skill operations auto-mode can/cannot substitute for. Acts as the canonical reference both operators and skill authors consult.

**Options in mind:**

- **Full permission contract spec** (recommended) — kit-wide rule with named substitutability for each skill operation. Strongest enforcement, clearest spec, biggest documentation surface.
- **Skill-by-skill fix** — patch `/claude-issue-executor` and `/pr-review-packager` independently without a unifying spec. Cheaper to land; risks drift as new skills with strict-mode gates ship.
- **Documentation-only change** — add a "skill authors should ask for explicit yes on hard-to-reverse actions" guideline to the workflow guide and trust authors. Lightest; exactly the gap this entry exists to close (the eval data shows authors comply organically — but the kit needs spec-grade enforcement, not author convention).
- **Reject auto-mode entirely on strict-mode skills** — auto-mode classifier fails closed: any skill operation that the spec marks as "non-substitutable" causes auto-mode to error rather than substitute. Most secure; potentially over-restrictive for genuinely-trivial cases.

**Open questions:** Where does the canonical contract live — in a new ADR, in the workflow guide, or both with one as source of truth? Does the contract need a per-skill "non-substitutable operations" list, or is the rule operation-shape-based ("any operation that affects shared state")? How does this interact with `--no-prompt` mode (#29) — `--no-prompt` is precisely the trivial-issue case where the operator has already authorized minimal-friction execution; should `--no-prompt` implicitly bypass the plan-mode gate, or does the contract require `--no-prompt --skip-plan-mode` explicit? How does the contract surface in skill chat output — every skill prepends a permission-mode banner, or only when about to substitute?

**Consequences to think through:** Easier — operator gets predictable, spec-grade enforcement on hard-to-reverse skill operations regardless of which skill or which auto-mode classifier version they're running; bypass becomes operator-acknowledged rather than silent; F24-class regressions stop being possible. Harder — auto-mode loses some convenience (one extra interaction per significant-task session); skill authors need to consult the contract when adding new operations; spec drift between contract + skill specs would be a new failure mode. Maintenance — the contract is new shared surface area touching every skill with strict-mode gates; needs a single source of truth and changes require updates across multiple skill specs.

**Alignment note for the ADR:** Likely supersedes or extends [ADR-039](../Design/adr/adr-039-plan-mode-for-significant-tasks.md) (entry #30). The existing ADR scoped the rule narrowly to `claude-issue-executor` plan mode; this entry generalizes to a kit-wide permission contract. Should also cross-reference [ADR-014](../Design/adr/adr-014-claude-issue-executor.md) (executor scope) and the future ADR for `/pr-review-packager`'s approval gate.

**Dependency note:** Touches `claude-issue-executor` (ADR-014, ADR-039), `pr-review-packager`, and any future skill with strict-mode gates. Pairs with #29 (ADR-038, `--no-prompt` interaction). Independent of #28 milestone lifecycle but the milestone-lifecycle skills (`/release`, `/complete-milestone`) also have approval gates that this contract would govern.

---

### 33. Project-shape detection in `/release` for non-product projects

**Status:** ready-for-adr
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** v3.3.0 baseline eval — F26 calibration across all three fixtures, with workflow-project severity escalation on research-tracker (see `runs/kit-v3.3.0/baseline-verdict.md` § "Active findings worth fixing before v3.4" #3)

**Context / trigger:** F26 (silent v0.1.0 default on `/release`) reproduced across all three fixtures of the v3.3.0 baseline. md-notes was medium severity (partial-scope honesty), podcast-pipeline mitigated to low via the Caveats section pattern, but research-tracker escalates the severity again because the project explicitly disclaims being a product (PRD has *"I'm not shipping a product"* language; success criteria are user-outcomes not test-pass; build-out plan is markdown-only with no compile/build/deploy step). On a project that isn't a product, `/release` should not pretend to ship one. It currently does — defaults to v0.1.0, generates release notes claiming *"first tagged release of …"*, with no acknowledgement of the workflow-not-product framing in the release body. **Strongest ADR-028-leakage signal in the release surface** across the v3.3.0 baseline.

**Sketch of the idea:** Add **project-shape detection** to `/release`'s preflight. Two changes:

1. **Detection signals** — `/release` scans for non-product project indicators: PRD or normalized-PRD contains *"not [shipping|building] a product"* / *"workflow"* / *"folder of markdown"* language; `Design/build-out-plan.md` Build strategy section says *"There is no compile / build / deploy step"* or equivalent; success criteria are user-outcome strings not test-result strings; no `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` / equivalent in repo root. **Two-or-more signals** trigger the non-product code path.
2. **Non-product release body** — when the non-product path triggers, the release notes lead with a clarifier: *"This is a workflow tag for documentation drift-tracking; the project is not a software product (see PRD for project shape). The version number is for snapshot ordering, not semantic versioning of an API."* Below the clarifier, the standard Features / Chores / Other sections still emit (they're useful regardless), but the framing is workflow-shaped.

Fallback: if the operator wants the standard product-release framing on a borderline-detected project, `--force-product-shape` flag overrides the auto-detection.

**Options in mind:**

- **Auto-detect with override flag** (recommended) — `/release` decides shape from project signals; operator can override with `--force-product-shape` if the auto-detection misclassifies. Strongest UX: the common case (operator doesn't have to think about it) works correctly; the edge case (auto-detection wrong) has an escape hatch.
- **Operator-set flag with no auto-detection** — `/release --workflow-project` opts into the non-product framing. Simpler spec; relies on operator memory.
- **No spec change, document the workflow-project caveat in the workflow guide** — operator manually edits the release body if they want non-product framing. Lightest; exactly the gap this entry exists to close.
- **Detection only, no release-body change** — `/release` flags "this looks like a non-product project — confirm before tagging?" but doesn't change the release body shape. Half-measure.

**Open questions:** What's the minimum signal threshold for the non-product path — two signals, three? How does this interact with `--milestone-phase=N` framing (which is shape-agnostic and useful on both project types)? Does the version-number convention change for non-product projects (e.g. should the kit recommend date-based snapshot tags like `2026.05` instead of semver `0.1.0` for non-product projects)? Where does the canonical "project-shape signals" list live — in `/release`'s SKILL.md, in the workflow guide, or in a new ADR? Should the detection pattern be reused by other release-adjacent skills (`/changelog`, `/audit-milestone`)?

**Consequences to think through:** Easier — non-product projects get release framing that matches their actual shape; F26-class agnostic-framing leak is closed in the release surface; the kit's claim to be workflow-agnostic gets a structural enforcement point (not just author-discipline). Harder — auto-detection has false-positive / false-negative cases (a Python project whose PRD happens to use the word "workflow" might trip detection); detection signals must be tuned conservatively to avoid surprising operators. Maintenance — detection signals are new surface area that needs to evolve as the kit's PRD / build-out templates evolve; signal drift would silently break the rule.

**Alignment note for the ADR:** New ADR, no clear predecessor. Should cross-reference ADR-028 (workflow-agnostic framing — this is one of the rule's structural enforcement points), [ADR-???]( ) for `/release` skill scope (entry #11, ADR currently unnumbered in feature-ideas.md), and the upcoming ADR from #32 (auto-mode permission contract — `/release`'s approval gate is one of the operations that contract governs).

**Dependency note:** Touches `/release` skill and `/changelog` skill. Independent of #31 / #32 / #34 — could land in any order.

---

### 34. Programmatic equivalent of `/check-plan` for in-skill invocation

**Status:** idea
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** v3.3.0 baseline eval — kit-architectural meta-friction reproduced across 5 skills (see `runs/kit-v3.3.0/baseline-verdict.md` § "Active findings worth filing but lower-leverage")

**Context / trigger:** `/check-plan`'s slash-command surface assumes operator invocation. Five skills in the v3.3.0 baseline (`/adr-writer`, `/prepare-issue`, `/changelog` inlined in `/release`, `/milestone-summary` inlined in `/complete-milestone`, plus `/pr-review-packager` for ADR-references checks) document that they should chain `/check-plan` as a sub-step, but **slash-commands aren't invokable from inside another skill's execution**. Every affected skill currently self-flags this with a transparency note (cross-skill consistency on the behavior across all 5) and substitutes the deterministic check logic inline. The substitution works, but the kit-architectural friction is real: the spec says one thing, the runtime can't deliver it, and every skill has to know to substitute. Two paths exist; they have different design implications.

**Sketch of the idea:** Decide between two fix shapes:

1. **Programmatic equivalent.** Ship a non-slash-command interface to `/check-plan`'s logic — likely a Python / bash script under `bin/check-plan` (or a kit-internal helper module) that skills can invoke without the slash-command surface. Skills update their specs to invoke the programmatic version when running as a sub-step; the slash-command form remains for direct operator use.
2. **Formalize inline-substitution as canonical.** Document that skills with `/check-plan` chain points run the deterministic check logic inline rather than invoking the slash-command. Update the affected skill specs to make the inline pattern canonical, not a workaround. No new code; pure documentation change.

**Options in mind:** Already covered in the sketch above. Path 1 is strictly bigger (new code, new entry-point surface, programmatic-vs-slash-command duality to maintain). Path 2 is strictly smaller (documentation-only). The choice depends on whether the kit values *spec-grade enforcement* (path 1: skills always run check-plan logic, deterministically) over *spec-runtime alignment* (path 2: spec matches what the runtime can actually do; no fiction).

**Open questions:** Does `/check-plan`'s logic have any operator-interactive parts (asks-for-confirmation steps) that wouldn't work in a programmatic-only context? If yes, programmatic equivalent needs a non-interactive variant — that's strictly more code. If the inline-substitution pattern becomes canonical (path 2), what's the contract for the inline substitution — every skill writes its own subset of check-plan logic, or there's a shared inline-substitution snippet skills reference? How does this affect future skills with `/check-plan` chain points — they have to know the substitution pattern from day 1.

**Consequences to think through:** **Path 1 (programmatic equivalent):** Easier — skills can deterministically run check-plan logic without operator involvement; spec aligns with runtime. Harder — new code surface, maintenance of two entry points (slash-command + programmatic) that must stay consistent. **Path 2 (inline-substitution canonical):** Easier — no new code; spec matches runtime. Harder — every skill with a check-plan chain point carries its own inline substitution; spec drift between skills would silently break consistency.

**Alignment note for the ADR:** New ADR, depending on path chosen. Path 1 is more architectural (new entry-point surface) and clearly ADR-worthy. Path 2 is more documentation-cleanup; could be a one-paragraph clarification rather than a full ADR. **Decision call before drafting** — recommend the operator decide path 1 vs path 2 before invoking `/adr-writer` on this entry, since the ADR shape differs significantly.

**Dependency note:** Touches every skill with a documented `/check-plan` chain point (`/adr-writer`, `/prepare-issue`, `/changelog`, `/milestone-summary`, `/pr-review-packager`). Independent of #31 / #32 / #33 — could land in any order, but recommend after #32 (the permission contract) since the inline-substitution-vs-programmatic question intersects with auto-mode / strict-mode contracts.

---

### 35. Centralize commit taxonomy across labels, classifier, group order, and examples

**Status:** idea
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** PR #76 review feedback (issue #63 fix for the `infra` verb classifier). Reviewer observed: "Long term, consider centralizing commit taxonomy definitions to avoid future drift between labels, regexes, rendering order, and examples."

**Context / trigger:** Adding `infra` as a recognised commit verb required edits across four separate surfaces, each of which can drift independently:

1. `templates/claude-md-template.md` line 161 — the canonical label set listed in the kit's CLAUDE.md template (`feature, bug, design, infra, security, docs`).
2. `skills/pr-review-packager/SKILL.md` § *Change-summary derivation* regex — the verb classifier that decides which group a commit lands in.
3. Same SKILL.md, group-output order — which group appears where in the rendered PR body.
4. `skills/pr-review-packager/example.md` — worked examples that demonstrate the categorization.

PR #76's fix touched 3 of the 4 (the example.md polish was lost when the duplicate PR #68 was closed in favour of #76). This is the same drift-class problem that ADRs 040 (cross-skill design-questions schema), 041 (auto-mode permission contract), and 043 (programmatic `/check-plan`) closed for other shared schemas — multiple surfaces deriving from one canonical truth, with PR review as the only enforcement until a structural rule lands.

**Sketch of the idea:** Define a single canonical commit-taxonomy artefact that the four consuming surfaces derive from rather than maintain in parallel. Likely shape: a markdown table at `templates/commit-taxonomy.md` (or `skills/pr-review-packager/taxonomy.md`) listing each verb with its label-name, regex match shape, group-output position, and display subheading. The CLAUDE.md template's label list, `pr-review-packager`'s regex, group order, and example.md walkthroughs all reference or derive from this single file. New verbs are added in exactly one place; drift becomes structurally impossible rather than convention-dependent.

**Options in mind:**

1. **Pure documentation reference** — the taxonomy file is the spec; consumers cite it but don't parse it. PR review enforces alignment.
2. **Programmatic surface (bin/-script-invocation precedent per ADR-043)** — `bin/check-commit-taxonomy` parses the file and emits structured taxonomy data. `pr-review-packager` invokes it as a subprocess (same pattern as `bin/check-plan`). CLAUDE.md template references it textually. Drift is caught at runtime by the script.
3. **Hybrid** — markdown taxonomy file + thin parser. The slash-command surfaces remain doc-driven; the bin/ script provides programmatic access for skills.

**Open questions:** Where does the canonical file live — `templates/` (user-facing; relevant when authoring CLAUDE.md) or `skills/pr-review-packager/` (alongside other classifier internals)? Does the centralization belong as a new ADR, or as an extension of ADR-041 (which already classifies verbs implicitly via category-3 PR creation)? Should this also subsume ADR-040's PR-body section grammar question (deferred from issue #72) — both touch "what canonical structures does the kit enforce in PR bodies" — or remain separate?

**Consequences to think through:** Easier — adding a new verb (e.g. a future `security(scope):` if security commits emerge as their own group) becomes a one-file change; CLAUDE.md template and pr-review-packager pick it up automatically; example.md regenerates trivially; PR review enforcement reduces to "did the taxonomy file get updated". Harder — new shared artefact to maintain; new parsing logic in `pr-review-packager` if option 2 or 3; cross-reference burden across the docs that cite the file. Maintenance — the canonical file sits at the boundary between user-facing kit docs and skill-internal classifier logic, so its location affects who is expected to edit it.

**Alignment note for the ADR:** New ADR. Cross-references ADR-041 (permission contract — same drift class, same single-source-of-truth pattern), ADR-043 (programmatic surface precedent), and §6 of `docs/workflow-guide.md` (cross-skill carry-forward — another canonical-schema example). Decision call before drafting: option 1 vs 2 vs 3 above.

**Dependency note:** Best landed *after* #34 (programmatic `/check-plan`) ships, so the `bin/`-script-invocation precedent is established and option 2/3 can lean on it. Touches `templates/claude-md-template.md`, `skills/pr-review-packager/SKILL.md`, `skills/pr-review-packager/example.md`, and (if option 2/3) adds `bin/check-commit-taxonomy`.

---

### 36. Declarative runtime-asset manifest for the installer

**Status:** idea
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** PR #65 review feedback (issue #60 — installer cluster fix). Reviewer's main concern: "The installer is now becoming the de facto package manifest for runtime dependencies. Right now the dependency graph exists in multiple places: skills reference templates implicitly, installer copies templates explicitly, docs describe expectations separately. That creates future drift risk."

**Context / trigger:** PR #65 codified a 12-entry runtime-template allowlist inline in the installer alongside `.github/` PR template, `.gitignore` split, and ADR README seed logic. This works at v3.4.0's asset count but the dependency graph is now spread across three surfaces that can drift independently:

1. Skills reference templates implicitly (e.g. `prd-normalizer` consumes `templates/prd.md`; `prd-to-mvp` consumes `templates/mvp.md`).
2. The installer copies templates explicitly via a hardcoded path list.
3. Docs (`docs/install.md`, `docs/repo-structure.md`, individual skill SKILL.md files) describe expectations in prose.

Adding a new runtime template today requires a five-step ritual: add template → update installer → update docs → update tests → remember staging rules. Manageable at 12 templates, brittle at 30. Same drift-class problem as #35 (commit taxonomy across labels/classifier/group order/examples) — multiple consuming surfaces deriving from one canonical truth, with PR review as the only enforcement.

**Sketch of the idea:** A single declarative manifest at the kit root (e.g. `runtime-assets.yaml` or `runtime-assets.md` per the markdown-table-with-fields precedent of `skills/check-plan/criteria.md`) listing every runtime asset with its source path, install destination, and metadata (required/optional, applies-to-project-shape, since-version). The installer derives its copy logic from the manifest rather than hardcoded lists. Skills reference assets by manifest ID rather than path; docs link to the manifest as the canonical source.

**Options in mind:**

1. **Pure-YAML manifest** — installer parses YAML; concise but requires a YAML dependency in the install path.
2. **Markdown-table manifest** — same shape as `skills/check-plan/criteria.md`; awk/sed-parseable; consistent with the kit's existing structured-data convention. Likely preferred.
3. **Executable manifest** — bash/python script enumerating assets via function calls; most flexible but hardest to lint structurally.
4. **Hybrid** — markdown-table source-of-truth + thin parser script (`bin/list-runtime-assets`) emitting structured output that consumers query. Same pattern as #35 option 3 and ADR-043's `bin/check-plan` precedent.

**Open questions:** Where does the manifest live — repo root (`runtime-assets.md`) or under a kit-self-config directory? Does it cover only the runtime-template allowlist, or also `.github/` assets, the ADR README seed, the `.gitignore` split, and future installer-managed files? How should skills reference assets — by ID (loose coupling) or by absolute path (current implicit pattern)? Does this subsume #35's commit taxonomy as instances of a shared "kit-self structured-data file" pattern, or remain separate?

**Consequences to think through:** Easier — adding a new runtime template becomes a one-file change; installer behaviour becomes auditable from one source; drift risk eliminated structurally rather than convention-dependent; pairs naturally with #37 (required-vs-optional categorization) as a column in the manifest schema. Harder — new artefact + parsing layer in the install path; potential bootstrap problem (the manifest is itself a runtime asset); migration of existing skills' implicit template references to manifest IDs is non-trivial. Maintenance — manifest schema needs versioning if the kit ever ships breaking installer changes.

**Alignment note for the ADR:** New ADR. Same single-source-of-truth pattern as ADR-040 / 041 / 043 and proposed in #35. Cross-references ADR-001 (kit-as-skills installation model — this ADR refines its asset-management story without superseding it). Likely bundled with #37 (asset-categorization split) as one ADR rather than two — both flow from the same architectural question about how the installer derives its behaviour. Decision call before drafting: option 1 vs 2 vs 3 vs 4 above.

**Dependency note:** Best landed after the v3.4.0 fixes settle (PRs #65, #66 in particular, which establish the v3.4.0 asset baseline; and ADR-042 / issue #71 which itself touches installer behaviour for non-product projects — its decisions may shape the manifest schema). Touches the installer script, every skill or doc that lists runtime assets, and the install test fixtures. Likely adds a top-level `runtime-assets.md` plus `bin/list-runtime-assets` if option 4 wins.

---

### 37. Categorize installer assets as required vs optional (fail-fast vs warn-and-continue)

**Status:** idea
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** PR #65 review feedback (issue #60 — installer cluster fix). Reviewer's smaller point: "warn-and-continue on missing-source rather than fail-fast is reasonable for optional helpers, but some of these assets are no longer optional. If a required runtime template is missing from the kit source, the installer may now produce a partially broken target while still reporting success."

**Context / trigger:** PR #65 retains the existing "warn-and-continue on missing-source" installer behaviour for all assets, including the 12 newly-mandatory runtime templates it codifies. The binary "warn-and-continue for everything" was correct when assets were optional convenience helpers; with v3.4.0 codifying mandatory runtime templates as a kit-wide install contract, that policy is now too permissive — a missing required asset can produce a partially broken target while the installer reports success.

**Sketch of the idea:** Introduce two categories of installer assets with distinct missing-source behaviour. **Required**: fail-fast — installer aborts with a clear error and a list of missing assets, target is left clean (or rolled back) so partial-install bugs are impossible. **Optional**: warn-and-continue — current behaviour, fine for convenience helpers like example projects. The 12 runtime templates and `.github/` PR template are required; ADR README seeding may also be required if `Design/adr/` is created. Convenience assets stay optional.

**Options in mind:**

1. **Inline annotation** — every asset reference in the installer carries a `required: true` / `required: false` flag; the existing copy-logic gains a fail-fast branch for required assets.
2. **Per-category file lists** — installer maintains separate required and optional path lists; missing required ⇒ abort.
3. **Manifest-derived (depends on #36)** — required-ness becomes a column in the runtime-asset manifest schema; installer reads it from the manifest. Cleanest if #36 lands.

**Open questions:** Which assets are required vs optional, exactly? The 12 runtime templates and `.github/pull_request_template.md` are clearly required at v3.4.0; is the `Design/adr/README.md` seed required or optional? The `.gitignore` split? Should fail-fast abort the whole install on the first missing asset or accumulate the list and report all missing assets at the end (better UX)? Does this need to interact with install test fixtures that intentionally omit assets — likely a `--allow-missing` debug flag or test-only env var?

**Consequences to think through:** Easier — silent partial-install bugs for required assets become structurally impossible; clearer install-failure UX (one error pointing at one or many missing files vs the current pile of warnings then "success"). Harder — installer needs richer error accumulation and reporting; install-test fixtures that intentionally omit assets need a way to opt out of fail-fast; rollback semantics need a decision (clean target vs partial target with error). Maintenance — required/optional categorization needs to stay current as assets are added; if it falls behind, fail-fast becomes warn-and-continue silently for newly-added required assets.

**Alignment note for the ADR:** Likely bundled with #36 as one ADR rather than two — both flow from the same architectural question about how the installer derives its behaviour. If #36 doesn't land, this can stand alone as a small installer hardening using option 1 or 2. Cross-references ADR-001 (kit-as-skills installation model). Decision call before drafting: option 1 vs 2 vs 3.

**Dependency note:** Best landed alongside or after #36 — option 3 cleanest, options 1/2 viable standalone. Touches the installer script directly and the install test fixtures. May add a `--allow-missing` flag or equivalent for test compatibility.

---

### 38. Ambiguous/hybrid worked example for `/release` project-shape detection

**Status:** idea
**Target:** v-next
**Captured:** 2026-05-06
**Origin:** PR #77 review feedback (issue #71 — project-shape detection in `/release`, ADR-042). Self-review flagged that the worked example covers product-shaped, auto-detected workflow-shaped, and override-path scenarios but not the hybrid case where signals split across the threshold.

**Context / trigger:** `skills/release/example.md` walks four of the five expected scenarios for ADR-042's detection logic — Pace Drift (product), `lit-review-2026` (auto-detected workflow), and the two `--force-*` override variants plus the mutually-exclusive abort. Missing: a hybrid project where signals split (e.g. 2 product-leaning, 2 workflow-leaning). Hybrid repos are exactly where the ≥2-signal threshold is most likely to misclassify, which is why the override flags exist; the example.md gap means operators have to reason about the override decision tree from the spec text alone.

**Sketch of the idea:** Add a fourth top-level variant section to `skills/release/example.md` parallel to the existing variants, walking through a hybrid project end-to-end. Show: (1) the signal scoring on both sides, (2) the deterministic auto-resolved outcome under current rules, (3) at least one override path showing when an operator would reach for `--force-product-shape` vs `--force-workflow-shape` and why, (4) the annotated tag content for both the auto-resolved and overridden paths. Concrete framing: a research repo that ships a small reproducibility CLI, or similar — picked so the signal split is unambiguous.

**Options in mind:**

1. **Inline within `skills/release/example.md`** — extend the existing file with a fourth variant section, matching the style of the three current variants.
2. **Spin out to a sibling `example-hybrid.md`** — keeps `example.md` focused on the canonical path, hybrid case lives separately.
3. **Do nothing** — operators read the override edge-case rows in SKILL.md instead.

**Open questions:** What concrete project framing makes the signal split unambiguous (research-with-CLI seems strongest but may need vetting)? Should the example cover both `--force-product` and `--force-workflow` overrides side-by-side, or just one path? Should it be presented as one hybrid project shown twice (auto vs override) or two slightly-different hybrid projects to keep each variant clean?

**Consequences to think through:** Easier — clearer override guidance for the most error-prone case; reduces operator burden of reasoning about the override decision tree from spec alone. Harder — `example.md` gets longer; some risk of the framing implying "hybrid" is a third shape value when the design is binary `product | workflow` with overrides. Maintenance — if ADR-042's signal list is ever extended (deferred per ADR Consequences), the hybrid example needs to be re-balanced so the split still demonstrates the threshold case.

**Alignment note:** No new ADR required — governed entirely by ADR-042's existing decisions. This is purely a worked-example gap. Likely files directly as a small documentation issue once batched, skipping the ADR step.

**Dependency note:** Self-contained doc work on `skills/release/example.md`. Touches no other files.

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

### AI PR review module for GitHub pull requests

**Status:** ready-for-adr
**Target:** future
**Captured:** 2026-05-06

**Context / trigger:** The Kit currently carries a project from planning through implementation and PR creation, but the review step remains largely manual once the PR is open on GitHub. An optional AI review layer would extend the existing GitHub-first workflow without changing the Kit's core install model or shifting review out of GitHub.[1][2]

**Sketch of the idea:** Add an optional module in the same repo as the Kit that can be installed into target projects. The module runs on `pull_request` events, reviews the PR using a hybrid diff-first approach, and posts a structured review into the GitHub PR as summary comments plus selective high-confidence line comments. Claude Code remains the implementation agent, but a helper can ingest unresolved PR comments and convert them into a remediation prompt for manual follow-up rather than autonomous fixes.[2][3][1]

**Options in mind:**
- Same repo, optional module, install-time opt-in.
- GitHub-only review surface; no separate dashboard or non-GitHub provider support in v1.[2]
- OpenRouter as the provider path, with an OpenAI-family model as the default review model.[4]
- Claude Code helper reads PR comments for remediation, but comments are still addressed manually in v1.[1]

**Open questions:**
- Should the default model be pinned for reproducibility or set to the latest recommended OpenRouter OpenAI model alias?
- What is the cleanest installer flag and target-project layout for the optional module?
- What exact helper interface should Claude Code use to ingest unresolved PR comments?
- Should the first version post only one structured top-level review comment, or allow selective inline comments as well?

**Consequences to think through:**
- Easier: extends the existing PR workflow with a GitHub-native review loop and preserves GitHub as the review inbox.
- Easier: keeps Claude Code focused on implementation while GitHub remains the review surface.[1]
- Harder: introduces a new external API dependency and secret-management path in target projects.
- Harder: review quality will vary depending on how much context is provided beyond the PR change set.

**Dependency note:** Touches the current PR flow centred on `pr-review-packager` and may later intersect with the permission-contract rules for any helper that writes back to GitHub or automates remediation flows.[1]

---

### Full-codebase indexing and retrieval for AI PR review

**Status:** idea
**Target:** future
**Captured:** 2026-05-06

**Context / trigger:** A hybrid diff-first reviewer is the right v1 because it is simpler and cheaper, but some PRs depend on broader architecture, shared contracts, and cross-file patterns that cannot be inferred reliably from the PR alone. Future versions may need a richer way to supply repository context when the PR is complex or high-risk.[3]

**Sketch of the idea:** Add an optional repository-context layer for the AI reviewer. This could include indexing the codebase, retrieving semantically relevant files, linking shared interfaces or configuration files, and selectively expanding context for risky pull requests instead of relying only on the changed lines and nearby files.[3]

**Options in mind:**
- Lightweight retrieval over repository files at review time.
- Pre-built full-codebase indexing with embeddings or other relevance ranking.
- Escalation model: only invoke broader retrieval for risky or cross-cutting PRs.
- Always-on full-repository context, likely too heavy for the Kit's first implementation.

**Open questions:**
- What should trigger retrieval or indexing: file count, path patterns, labels, or explicit user flags?
- Should the context source include only code, or also ADRs, README files, and design notes?
- How much extra context can be included before latency and cost become too high?
- Does this remain an optional module extension, or become a second-tier mode within the same module?

**Consequences to think through:**
- Easier: improves review quality for architectural, cross-cutting, and framework-sensitive changes.[3]
- Harder: adds complexity, processing cost, and more moving parts than a general-user v1 should expose.
- Harder: raises new questions about indexing freshness, storage, and retrieval quality.

**Dependency note:** Deferred by design behind the v1 hybrid diff-first reviewer. Should only be revisited after the basic module, GitHub comment flow, and Claude Code remediation helper are stable.

---

### Advanced model and API-key configuration for AI PR review

**Status:** idea
**Target:** future
**Captured:** 2026-05-06

**Context / trigger:** The simplest v1 for general users is one provider, one required secret, and one recommended default model. More advanced teams may later want to select different models, route different repositories to different models, or manage credentials at repository, environment, or organization level.[5][6]

**Sketch of the idea:** Extend the optional AI PR review module so users can override the default review model, set repository-level or environment-level config variables, and optionally support different API keys or model profiles for different projects or review modes. Keep the secure storage path in GitHub Actions secrets, while allowing non-sensitive model and behavior settings via GitHub Actions variables.[6][5]

**Options in mind:**
- Keep one required secret `OPENROUTER_API_KEY` and one optional variable for model override.[5][6]
- Support multiple model profiles such as default, cheap, deep-review.
- Support organization-level secrets for teams managing several repos.[5]

**Sources** (shared across the three AI-PR-review entries above):

1. `docs/workflow-guide.md` (kit-internal)
2. `docs/install.md` (kit-internal)
3. Graphite — *How AI Models Handle Limited Context: Full Repo vs Diff* — https://graphite.com/guides/ai-code-review-context-full-repo-vs-diff
4. OpenRouter — *GPT-5.5 API Pricing & Providers* — https://openrouter.ai/openai/gpt-5.5
5. GitHub Docs — *Using secrets in GitHub Actions* — https://docs.github.com/actions/security-guides/using-secrets-in-github-actions
6. GitHub Docs — *Store information in variables* — https://docs.github.com/actions/learn-github-actions/variables
