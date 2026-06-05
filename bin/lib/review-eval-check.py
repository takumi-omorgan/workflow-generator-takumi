#!/usr/bin/env python3
"""Evaluate review-eval fixture runs against their expectations (M5, ADR-051).

Reads $RECORDS (a JSON array of {name, artifact, expectations, reviewExit, pr})
and the duplicate-publish result ($DUP_OK / $DUP_DETAIL). For each fixture it
loads the generated artifact and checks the expectation keys documented in
ai-review/eval/README.md. Prints a JSON result the calling bash renders.
"""
import os
import sys
import json


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check_one(rec):
    problems = []
    if rec.get("reviewExit") != 0:
        problems.append("review-pr exited %s (expected 0)" % rec.get("reviewExit"))
        return problems
    art_path = rec.get("artifact")
    if not art_path or not os.path.isfile(art_path):
        problems.append("no artifact produced")
        return problems
    try:
        art = load(art_path)
    except Exception as e:
        problems.append("artifact unreadable: %s" % e)
        return problems
    try:
        exp = load(rec["expectations"]).get("expect", {})
    except Exception as e:
        problems.append("expectations unreadable: %s" % e)
        return problems

    findings = art.get("findings", [])
    cats = [f.get("category") for f in findings]
    sevs = [f.get("severity") for f in findings]
    n_blocking = sum(1 for f in findings if f.get("classification") == "blocking")
    n_commentable = sum(1 for f in findings if f.get("commentable"))

    if "minBlocking" in exp and n_blocking < exp["minBlocking"]:
        problems.append("blocking %d < minBlocking %d" % (n_blocking, exp["minBlocking"]))
    if "maxBlocking" in exp and n_blocking > exp["maxBlocking"]:
        problems.append("blocking %d > maxBlocking %d" % (n_blocking, exp["maxBlocking"]))
    if "minFindings" in exp and len(findings) < exp["minFindings"]:
        problems.append("findings %d < minFindings %d" % (len(findings), exp["minFindings"]))
    if "maxFindings" in exp and len(findings) > exp["maxFindings"]:
        problems.append("findings %d > maxFindings %d (too noisy)" % (len(findings), exp["maxFindings"]))
    for c in exp.get("requireCategories", []):
        if c not in cats:
            problems.append("missing required category %r" % c)
    for c in exp.get("forbidCategories", []):
        if c in cats:
            problems.append("forbidden category %r present (invented?)" % c)
    if "requireSeverity" in exp and exp["requireSeverity"] not in sevs:
        problems.append("no finding at severity %r" % exp["requireSeverity"])
    if "minCommentable" in exp and n_commentable < exp["minCommentable"]:
        problems.append("commentable %d < minCommentable %d" % (n_commentable, exp["minCommentable"]))
    if "maxCommentable" in exp and n_commentable > exp["maxCommentable"]:
        problems.append("commentable %d > maxCommentable %d" % (n_commentable, exp["maxCommentable"]))
    if "truncated" in exp and bool(art.get("truncated")) != bool(exp["truncated"]):
        problems.append("truncated=%s, expected %s" % (art.get("truncated"), exp["truncated"]))
    return problems


def main():
    records = json.loads(os.environ.get("RECORDS") or "[]")
    dup_ok = os.environ.get("DUP_OK") == "true"
    dup_detail = os.environ.get("DUP_DETAIL", "")

    fixtures = []
    all_pass = True
    for rec in records:
        problems = check_one(rec)
        ok = not problems
        all_pass = all_pass and ok
        fixtures.append({"name": rec.get("name"), "pass": ok, "problems": problems})

    if not records:
        all_pass = False

    overall = all_pass and dup_ok
    outputs = {
        "fixtureCount": len(fixtures),
        "passed": sum(1 for f in fixtures if f["pass"]),
        "fixtures": fixtures,
        "duplicatePrevention": {"pass": dup_ok, "detail": dup_detail},
    }

    lines = ["review-eval: %s — %d/%d fixtures passed" %
             ("ok" if overall else "FAIL", outputs["passed"], outputs["fixtureCount"])]
    for f in fixtures:
        mark = "ok" if f["pass"] else "FAIL"
        lines.append("  [%s] %s" % (mark, f["name"]))
        for p in f["problems"]:
            lines.append("        - %s" % p)
    lines.append("  [%s] duplicate-publish prevention — %s" %
                 ("ok" if dup_ok else "FAIL", dup_detail))

    print(json.dumps({
        "exit": 0 if overall else 1,
        "status": "ok" if overall else "fail",
        "outputs": outputs,
        "text": "\n".join(lines),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
