#!/usr/bin/env python3
"""collect-eval-check — offline fixture checker for the collectors (ADR-054).

Drives bin/changelog-collect and bin/pr-context over their fixture trees with
the --git-log-file / --gh-mock offline inputs (mirroring AI-review's --mock),
captures the envelope `outputs`, and compares it byte-for-byte (as normalised
JSON) against each fixture's expected.json. This pins the exact output shape
the changelog and pr-review-packager skills parse — the behavioral contract.

Each fixture directory carries args.json describing how to invoke its tool;
expected.json is the canonical `outputs`. A pr-context fixture tree that does
not exist yet is simply skipped (it lands with bin/pr-context).

Prints a result JSON object {status, outputs, errors, text}; bin/collect-eval
renders it. Exit 0 = all match, 1 = a fixture diverged.
"""

import json
import os
import subprocess
import sys

BIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../bin


def first_diff(a, b, path="$"):
    """Return a human path to the first structural divergence, or None."""
    if type(a) is not type(b) and not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
        return "%s: type %s != %s" % (path, type(a).__name__, type(b).__name__)
    if isinstance(a, dict):
        ka, kb = set(a), set(b)
        if ka != kb:
            return "%s: keys %s != %s" % (path, sorted(ka), sorted(kb))
        for k in a:
            d = first_diff(a[k], b[k], "%s.%s" % (path, k))
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return "%s: length %d != %d" % (path, len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, "%s[%d]" % (path, i))
            if d:
                return d
        return None
    if a != b:
        return "%s: %r != %r" % (path, a, b)
    return None


def changelog_cmd(fixdir, args):
    cmd = [os.path.join(BIN, "changelog-collect"),
           "--from", args["from"], "--to", args["to"]]
    if args.get("origin"):
        cmd += ["--origin", args["origin"]]
    if args.get("includeMerges"):
        cmd += ["--include-merges"]
    cmd += ["--git-log-file", os.path.join(fixdir, "git-log.raw")]
    ghmock = os.path.join(fixdir, "gh-mock")
    if os.path.isdir(ghmock):
        cmd += ["--gh-mock", ghmock]
    cmd += ["--format", "json"]
    return cmd


def prcontext_cmd(fixdir, args):
    cmd = [os.path.join(BIN, "pr-context")]
    if args.get("base"):
        cmd += ["--base", args["base"]]
    if args.get("branch") is not None:
        cmd += ["--branch", args["branch"]]
    cmd += ["--git-log-file", os.path.join(fixdir, "git-log.raw")]
    # Always pin the lookup dirs into the fixture (even when absent) so the
    # collector never reads the real repo's prompts/notes/design dirs.
    for opt, sub in (("--prompts-dir", "prompts"), ("--notes-dir", "notes"),
                     ("--adr-dir", "adr")):
        cmd += [opt, os.path.join(fixdir, sub)]
    cmd += ["--format", "json"]
    return cmd


TOOLS = [
    ("changelog-collect", "changelog-collect-fixtures", changelog_cmd),
    ("pr-context", "pr-context-fixtures", prcontext_cmd),
]


def check_fixture(builder, fixdir):
    args = json.load(open(os.path.join(fixdir, "args.json"), encoding="utf-8"))
    cmd = builder(fixdir, args)
    proc = subprocess.run(cmd, capture_output=True, text=True)
    problems = []
    if proc.returncode not in (0,):
        problems.append("exit %d (stderr: %s)" % (proc.returncode, proc.stderr.strip()))
        return problems
    try:
        env = json.loads(proc.stdout)
    except Exception as e:
        return ["envelope not JSON: %s" % e]
    got = env.get("outputs")
    expected = json.load(open(os.path.join(fixdir, "expected.json"), encoding="utf-8"))
    d = first_diff(expected, got)
    if d:
        problems.append("outputs diverge at " + d)
    return problems


def main():
    results = []
    for tool, root_name, builder in TOOLS:
        root = os.path.join(BIN, root_name)
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            fixdir = os.path.join(root, name)
            if not os.path.isdir(fixdir):
                continue
            if not os.path.exists(os.path.join(fixdir, "args.json")):
                continue
            problems = check_fixture(builder, fixdir)
            results.append({"name": "%s/%s" % (tool, name), "ok": not problems,
                            "problems": problems})

    failed = [r for r in results if not r["ok"]]
    status = "ok" if not failed else "fail"
    passed = len(results) - len(failed)
    lines = ["  %s %s" % ("PASS" if r["ok"] else "FAIL", r["name"]) for r in results]
    for r in results:
        for p in r["problems"]:
            lines.append("      - %s: %s" % (r["name"], p))
    text = "collect-eval: %s — %d/%d fixtures passed\n%s" % (status, passed, len(results), "\n".join(lines))
    outputs = {"passed": passed, "total": len(results), "fixtures": results}
    print(json.dumps({"status": status, "outputs": outputs, "errors": [], "text": text}))
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
