# Changelog

All notable changes to this project.

## v3.1.0 — PRD template for offline drafting (2026-04-26)

Range: `v3.0.0..v3.1.0`

**MINOR** per [ADR-026](Design/adr/adr-026-kit-versioning-policy.md): a new template is an additive change. Existing target projects adopt it without modifying anything they already have.

### Features

- Ship [`templates/prd-template.md`](templates/prd-template.md) — a canonical PRD shape mirroring `prd-normalizer`'s 11 fields one-to-one, so users can draft a PRD offline (by hand or via any external LLM) and hand the result to `prd-normalizer` as a near-pass-through ([`cd675e7`](https://github.com/olivermorgan2/workflow-generator/commit/cd675e7), [#32](https://github.com/olivermorgan2/workflow-generator/issues/32), [ADR-027](Design/adr/adr-027-prd-template.md)).

### Docs

- Wire the new template into `templates/README.md`, `skills/prd-normalizer/SKILL.md`, and `skills/idea-to-prd/SKILL.md` so the standard-PRD intake path now has an explicit drafting starting point ([`9e78182`](https://github.com/olivermorgan2/workflow-generator/commit/9e78182), [#32](https://github.com/olivermorgan2/workflow-generator/issues/32), [ADR-027](Design/adr/adr-027-prd-template.md)).

### Process

- Mark feature-ideas #16 (PRD template for external-LLM drafting) `shipped`, link to ADR-027. Audit-trail prompt for the work landed under `prompts/issue-032-prd-template.md` ([`fb30bed`](https://github.com/olivermorgan2/workflow-generator/commit/fb30bed)).

## v3.0.0 — kit hygiene and licensing (2026-04-26)

Range: `v2.0.0..v3.0.0`

This is a **MAJOR** release per [ADR-026](Design/adr/adr-026-kit-versioning-policy.md): renames a placeholder and parser-relevant heading in the MVP scoping framework.

### Breaking changes

- Rename MVP scoping headings: `### In v1` / `### Not in v1` → `### In scope` / `### Out of scope` across the kit's templates, skills, examples, and worked projects ([`726ddac`](https://github.com/olivermorgan2/workflow-generator/commit/726ddac), [#28](https://github.com/olivermorgan2/workflow-generator/issues/28), [ADR-024](Design/adr/adr-024-mvp-vocabulary-versus-v1.md)).
- Rename README-template placeholders: `{{IN_V1_BULLETS}}` → `{{IN_SCOPE_BULLETS}}` and `{{NOT_IN_V1_BULLETS}}` → `{{OUT_OF_SCOPE_BULLETS}}` ([`726ddac`](https://github.com/olivermorgan2/workflow-generator/commit/726ddac), [#28](https://github.com/olivermorgan2/workflow-generator/issues/28), [ADR-024](Design/adr/adr-024-mvp-vocabulary-versus-v1.md)).
- **Migration:** projects scaffolded from v2.0.0 with hand-rolled local overrides of `templates/readme-template.md` need the placeholder rename. Projects that have a `Design/mvp.md` filled with `### In v1` / `### Not in v1` headings need the heading rename for `workflow-docs` and `issue-planner` to parse them correctly. No backwards-compat shim — the kit had not shipped externally before v3.

### Features

- Auto-sync the ADR index in `Design/adr/README.md` via `bin/sync-adr-index`. Marker fences (`<!-- adr-index:start -->` / `<!-- adr-index:end -->`) wrap the generated table; editorial text outside is preserved. Wired into `adr-writer`, `claude-issue-executor`, `pr-review-packager`, and `release` skills. Installer copies the script into target projects' `.claude/bin/` ([`cbca260`](https://github.com/olivermorgan2/workflow-generator/commit/cbca260), [#27](https://github.com/olivermorgan2/workflow-generator/issues/27), [ADR-023](Design/adr/adr-023-auto-sync-adr-index.md)).

### Decisions and policy

- License the kit under **MIT** with copyright `(c) 2026 Oliver Morgan`. The kit's MIT license covers the kit itself (templates, skills, scripts, docs); user-built projects (their `Design/mvp.md`, source code, etc.) are the user's own work and not subject to the kit's license. Optional `--license=mit --license-holder=NAME` installer flag documented for users who want a starter LICENSE in their target project ([`8b16d5a`](https://github.com/olivermorgan2/workflow-generator/commit/8b16d5a), [#29](https://github.com/olivermorgan2/workflow-generator/issues/29), [ADR-025](Design/adr/adr-025-license.md)).
- Document the kit's semver versioning policy. Explicit MAJOR/MINOR/PATCH classifications for a templates-and-skills "API". The v3 release validates against this policy as MAJOR ([`3397070`](https://github.com/olivermorgan2/workflow-generator/commit/3397070), [#30](https://github.com/olivermorgan2/workflow-generator/issues/30), [ADR-026](Design/adr/adr-026-kit-versioning-policy.md)).
- Drop kit-self "v1" version qualifiers from kit-scope decisions. Supersession is now the single mechanism for scope changes; kit-scope statements stay valid across releases. ADR-002 superseded by ADR-022 ([`6a1b28e`](https://github.com/olivermorgan2/workflow-generator/commit/6a1b28e), [#26](https://github.com/olivermorgan2/workflow-generator/issues/26), [ADR-022](Design/adr/adr-022-drop-version-qualifiers-from-kit-scope.md)).

### Docs

- Earlier removal of "v1" qualifiers from user-facing docs and ADR references ([`813939a`](https://github.com/olivermorgan2/workflow-generator/commit/813939a)).
- Add v-next feature-ideas entries: license selection (#18) and split to public distribution repo (#19) ([`0e0219b`](https://github.com/olivermorgan2/workflow-generator/commit/0e0219b), [`b749fc7`](https://github.com/olivermorgan2/workflow-generator/commit/b749fc7)).

### Process

- Retroactive audit trail for the v3 batch: 5 GitHub issues (#26-#30) and 5 canonical session-brief prompts under `prompts/`. Going forward every kit change goes through the formal `ADR → issue → prompt → executor` flow regardless of size ([`ca6af6d`](https://github.com/olivermorgan2/workflow-generator/commit/ca6af6d)).

### Chores

- Move dogfooding `link-skills` tool to dotfiles repo; document the dogfooding convention in `CLAUDE.md`; stop tracking `.obsidian/` ([`40857ab`](https://github.com/olivermorgan2/workflow-generator/commit/40857ab), [`147aaa3`](https://github.com/olivermorgan2/workflow-generator/commit/147aaa3), [`28f2277`](https://github.com/olivermorgan2/workflow-generator/commit/28f2277)).
- Add CHANGELOG.md for the v1→v2 range ([`c542fc7`](https://github.com/olivermorgan2/workflow-generator/commit/c542fc7)).

## v2.0.0 — v-next feature set (2026-04-19)

Range: `v1.0.0..v2.0.0`

### Features

- add claude-issue-executor skill ([`518f292`](https://github.com/olivermorgan2/workflow-generator/commit/518f29266b3a37f972f8df2adc2b17d9f32bdce1), [#16](https://github.com/olivermorgan2/workflow-generator/issues/16), [ADR-006](Design/adr/adr-006-claude-code-execution-model.md), [ADR-014](Design/adr/adr-014-claude-issue-executor-skill.md))
- add /release skill ([`64ec763`](https://github.com/olivermorgan2/workflow-generator/commit/64ec763d4861d5754b1f56c9b63a4080edb6ef19), [#19](https://github.com/olivermorgan2/workflow-generator/issues/19), [ADR-016](Design/adr/adr-016-changelog-and-release-notes-skill.md), [ADR-017](Design/adr/adr-017-release-skill.md))
- add /workflow-docs skill ([`d3015bf`](https://github.com/olivermorgan2/workflow-generator/commit/d3015bfdfa009c94959f6503ee5c7289a856cbae), [#20](https://github.com/olivermorgan2/workflow-generator/issues/20), [ADR-018](Design/adr/adr-018-workflow-docs-skill.md))
- add pr-review-packager skill ([`b4afd4f`](https://github.com/olivermorgan2/workflow-generator/commit/b4afd4f6589920459d1a23a0a6fda181d99c009a), [#17](https://github.com/olivermorgan2/workflow-generator/issues/17), [ADR-015](Design/adr/adr-015-pr-review-packager-skill.md))
- add issue-planner skill ([`0cf5765`](https://github.com/olivermorgan2/workflow-generator/commit/0cf5765d7bd33b67f69d5ee2b73cf7dce5529c4c), [#14](https://github.com/olivermorgan2/workflow-generator/issues/14), [ADR-011](Design/adr/adr-011-issue-planner-skill.md), [ADR-012](Design/adr/adr-012-github-projects-integration.md))
- add /changelog skill ([`063fb32`](https://github.com/olivermorgan2/workflow-generator/commit/063fb32ee53b12f09dee959e87ae0628eb50ad9c), [#18](https://github.com/olivermorgan2/workflow-generator/issues/18), [ADR-016](Design/adr/adr-016-changelog-and-release-notes-skill.md))
- add install-workflow-kit script ([`bdfb349`](https://github.com/olivermorgan2/workflow-generator/commit/bdfb349d47276823d8f7e929c33a040c7d62af8a), [#13](https://github.com/olivermorgan2/workflow-generator/issues/13), [ADR-009](Design/adr/adr-009-installer-script.md), [ADR-010](Design/adr/adr-010-optional-with-docs-flag.md))
- add /prepare-issue skill ([`cd8fd3b`](https://github.com/olivermorgan2/workflow-generator/commit/cd8fd3bfbd5ae1e51db2da7e7d4907f1939660c9), [#15](https://github.com/olivermorgan2/workflow-generator/issues/15), [ADR-013](Design/adr/adr-013-prepare-issue-skill.md))
- expand CLAUDE.md starter template ([`f06f3cc`](https://github.com/olivermorgan2/workflow-generator/commit/f06f3cc65d2a4afe7124cb5e2fa1ed0c6de0cf90), [#11](https://github.com/olivermorgan2/workflow-generator/issues/11), [ADR-007](Design/adr/adr-007-claude-md-starter-template.md))
- add dedicated prompts/ folder and template ([`43dcf65`](https://github.com/olivermorgan2/workflow-generator/commit/43dcf652eac8d8bd093ca1677528151eabd1d2e9), [#12](https://github.com/olivermorgan2/workflow-generator/issues/12), [ADR-008](Design/adr/adr-008-dedicated-prompts-folder.md))

### Fixes

- remove stray merge-conflict markers from install.md ([`ac51c3d`](https://github.com/olivermorgan2/workflow-generator/commit/ac51c3d061d5f06e3b0fb769d2b62f8328a6a033), [#13](https://github.com/olivermorgan2/workflow-generator/issues/13), [ADR-008](Design/adr/adr-008-dedicated-prompts-folder.md))

### Docs

- polish status + surface workflow-guide; move v-next entry ([`7092f6f`](https://github.com/olivermorgan2/workflow-generator/commit/7092f6fe5b1d6ad85782d1d04d7ce58eed8176c5), [#17](https://github.com/olivermorgan2/workflow-generator/issues/17), [ADR-018](Design/adr/adr-018-workflow-docs-skill.md))
- add worked project gallery ([`47a4cff`](https://github.com/olivermorgan2/workflow-generator/commit/47a4cffa9fc81e5fd0ca6149091c72cef8122009), [#23](https://github.com/olivermorgan2/workflow-generator/issues/23), [ADR-021](Design/adr/adr-021-example-projects.md))
- add end-to-end workflow guide ([`a20869e`](https://github.com/olivermorgan2/workflow-generator/commit/a20869eaaa56b903871b9e68d1b4d31252e6994d), [#22](https://github.com/olivermorgan2/workflow-generator/issues/22), [ADR-020](Design/adr/adr-020-workflow-guide.md))
- add Claude Code guide ([`0e43dfe`](https://github.com/olivermorgan2/workflow-generator/commit/0e43dfee799a99e53a034e22f9152e0c13b09743), [#21](https://github.com/olivermorgan2/workflow-generator/issues/21), [ADR-019](Design/adr/adr-019-claude-code-guide.md))
- clarify install steps and drop ADR refs from At a glance ([`61f94d6`](https://github.com/olivermorgan2/workflow-generator/commit/61f94d625cd811c6674b4020cb0ce6a8becbe0a5))
- clarify working-directory step in Quick start ([`177ede9`](https://github.com/olivermorgan2/workflow-generator/commit/177ede974c2456aaace3d2993e16878033283da5))
- rewrite Quick start for clarity ([`a03d0c0`](https://github.com/olivermorgan2/workflow-generator/commit/a03d0c0c4bcf47bce7e29dee944b6b394e91d8b6))

### Other

- Update feature-ideas.md statuses to reflect accepted ADRs ([`c344cfa`](https://github.com/olivermorgan2/workflow-generator/commit/c344cfa203ed5f18e631b56b925427675b638326), [#24](https://github.com/olivermorgan2/workflow-generator/issues/24))
- Accept ADRs 007-021 and add issue prompts for v-next ([`dc2869d`](https://github.com/olivermorgan2/workflow-generator/commit/dc2869d2a2a2d964388f5512695e7189c8449df3))
- Add proposed ADRs 007-021 for v-next feature set ([`ab00f92`](https://github.com/olivermorgan2/workflow-generator/commit/ab00f92c4922b1ea34e2de3a39f0a2ace8839650), [ADR-007](Design/adr/adr-007-claude-md-starter-template.md), [ADR-008](Design/adr/adr-008-dedicated-prompts-folder.md), [ADR-009](Design/adr/adr-009-installer-script.md), [ADR-010](Design/adr/adr-010-optional-with-docs-flag.md), [ADR-011](Design/adr/adr-011-issue-planner-skill.md), [ADR-012](Design/adr/adr-012-github-projects-integration.md), [ADR-013](Design/adr/adr-013-prepare-issue-skill.md), [ADR-014](Design/adr/adr-014-claude-issue-executor-skill.md), [ADR-015](Design/adr/adr-015-pr-review-packager-skill.md), [ADR-016](Design/adr/adr-016-changelog-and-release-notes-skill.md), [ADR-017](Design/adr/adr-017-release-skill.md), [ADR-018](Design/adr/adr-018-workflow-docs-skill.md), [ADR-019](Design/adr/adr-019-claude-code-guide.md), [ADR-020](Design/adr/adr-020-workflow-guide.md), [ADR-021](Design/adr/adr-021-example-projects.md))
- Reorder feature ideas by ADR dependency into 5 layers ([`20d9bfb`](https://github.com/olivermorgan2/workflow-generator/commit/20d9bfb0f9d2ed2100881fa82f8423961b28a514))
- Add branch naming convention, draft PR guidance, and GitHub Flow alignment ([`db9ae79`](https://github.com/olivermorgan2/workflow-generator/commit/db9ae79b728184200598fe8973de89da0651b703))
