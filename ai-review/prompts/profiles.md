<!--
  Review profiles for AI PR review (Milestone M5, Issue 26, ADR-051).
  bin/review-pr appends exactly one of these blocks (selected by the
  config `profile` or the --profile flag) after the rubric, to tune the
  comment threshold. Default: balanced.
-->

# Review profiles

Exactly one profile is active per review. It changes the **threshold** for
what is worth raising — not the rubric's priorities.

## strict

Surface everything the rubric covers, including `category: "style"` nitpicks
(formatting, naming, import order), each marked low severity. Still classify
honestly: nitpicks are `non-blocking`, never `blocking`. Inline comments are
allowed for high-confidence located findings of any category. Use this when
the author explicitly wants a thorough, opinionated pass.

## balanced (default)

Surface correctness, security, data-loss, regression, compatibility, and
test-coverage findings, plus high-value maintainability and docs issues.
**Omit pure style nitpicks.** Inline only high-confidence located findings;
keep speculative or unlocated findings in the top-level summary. This is the
default and fits most PRs.

## lightweight

Surface only **blocking** findings — correctness, security, data-loss,
regression, and compatibility defects with a concrete failure mode — plus at
most a one-line summary of anything else. Do not raise non-blocking
suggestions, questions about taste, style, or maintainability. Use this for
fast, low-noise gating on small or routine PRs.
