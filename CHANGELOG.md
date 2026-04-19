# Changelog

All notable changes to this project.

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
