<!--
  Review quality rubric for AI PR review (Milestone M5, Issue 26, ADR-051).
  Sent to the model after the system prompt. Defines what to look for, how
  to classify, and what NOT to comment on. The profile block (profiles.md)
  tunes the comment threshold on top of this.
-->

# AI PR review rubric

Review for **risk that would survive merge**, in this priority order. Spend
attention top-down; do not let low-priority categories crowd out the high.

## Priority order (what to look for)

1. **Correctness** — logic errors, wrong conditionals, off-by-one, unhandled
   error paths, broken control flow, incorrect API usage.
2. **Security** — injection, missing authz/authn checks, unsafe
   deserialization, secret/credential exposure, unsafe shell/SQL/HTML.
3. **Data loss** — destructive operations without guards, migrations that
   drop or corrupt data, non-idempotent writes, missing backups/rollback.
4. **Regression** — changes that break existing behaviour or callers;
   removed handling; altered defaults with downstream impact.
5. **API / contract compatibility** — breaking changes to public
   signatures, response shapes, CLI flags, env vars, or file formats
   without a versioning or migration story.
6. **Test coverage** — new behaviour or bug fixes landing without tests;
   tests that assert nothing; happy-path-only coverage of risky logic.
7. **Maintainability** — genuinely confusing structure, dead code, copy-paste
   that will rot, names that mislead. Only when it impairs a future reader,
   not as taste.
8. **Docs impact** — code changes that invalidate docs/README/help text, or
   docs changes that are inaccurate or give commands that do not work.

## Classification

- **blocking** — must be fixed before merge: a correctness/security/
  data-loss/regression/compat defect with a concrete failure mode. Always
  include a `suggestion`.
- **non-blocking** — a worthwhile improvement that should not hold the merge.
- **question** — something you genuinely cannot determine from the diff and
  need the author to clarify. Phrase as a question.
- **praise** — a notably good decision worth reinforcing. Use sparingly and
  never inline-spam; at most one or two per review.

## Confidence and commentability

- `confidence: high` only when the diff alone is sufficient evidence.
- A finding is `commentable: true` **only** when it is high-confidence, has
  a `file` + `line` present in the diff, and is not pure praise. Everything
  else belongs in the top-level summary.
- When unsure of the exact line, set `line: null` and `commentable: false`.

## What NOT to do

- Do not comment on formatting, import order, or naming taste unless the
  active profile is `strict` and you mark them `category: "style"`.
- Do not restate what the diff obviously does.
- Do not flag pre-existing issues outside the diff.
- Do not pad the review. An empty `findings` array is the right answer for a
  clean change.
- Do not invent code-level bugs in a docs-only diff.
