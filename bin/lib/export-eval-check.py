#!/usr/bin/env python3
"""export-eval-check.py — offline fixture harness for check-public-export.

Drives bin/check-public-export over each fixture staging tree under
bin/export-eval-fixtures/ and asserts:
  - the actual exit code matches the fixture's expected exit, and
  - every `mustContain` substring appears somewhere in the reported
    violations (so failing fixtures prove the error names the bad
    file/path/reference, not just that *some* failure occurred).

This is the byte-stability / behavior proof the contract relies on, fully
offline (no git archive, no network), suitable for bin/self-test and CI.

Environment (set by bin/export-eval):
    CHECKER        path to bin/check-public-export
    FIXTURES       fixtures root directory
"""

import json
import os
import subprocess
import sys

CHECKER = os.environ["CHECKER"]
FIXTURES = os.environ["FIXTURES"]


def run_checker(staging, version):
    cmd = [CHECKER, "--staging", staging, "--format", "json"]
    if version:
        cmd += ["--version", version]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError:
        envelope = None
    return proc.returncode, envelope


def violation_blob(envelope):
    """All problem paths+details concatenated, for substring assertions."""
    if not envelope:
        return ""
    parts = []
    for check in envelope.get("outputs", {}).get("checks", []):
        for p in check.get("problems", []):
            parts.append(p.get("path", ""))
            parts.append(p.get("detail", ""))
    return "\n".join(parts)


results = []
fixtures = sorted(
    d for d in os.listdir(FIXTURES)
    if os.path.isfile(os.path.join(FIXTURES, d, "expected.json"))
)

for name in fixtures:
    fdir = os.path.join(FIXTURES, name)
    staging = os.path.join(fdir, "staging")
    with open(os.path.join(fdir, "expected.json"), encoding="utf-8") as fh:
        expected = json.load(fh)

    exp_exit = expected.get("exit", 0)
    version = expected.get("version")
    must = expected.get("mustContain", [])

    if not os.path.isdir(staging):
        results.append({"name": name, "ok": False,
                        "reason": "missing staging/ tree"})
        continue

    actual_exit, envelope = run_checker(staging, version)
    blob = violation_blob(envelope)

    problems = []
    if actual_exit != exp_exit:
        problems.append("expected exit %s, got %s" % (exp_exit, actual_exit))
    if envelope is None:
        problems.append("checker did not emit valid JSON")
    for needle in must:
        if needle not in blob:
            problems.append("expected violation text to mention %r" % needle)

    results.append({
        "name": name,
        "ok": not problems,
        "expectedExit": exp_exit,
        "actualExit": actual_exit,
        "reason": "; ".join(problems) if problems else "ok",
    })

passed = sum(1 for r in results if r["ok"])
total = len(results)
failed = [r for r in results if not r["ok"]]

if total == 0:
    status, exit_code = "no-fixtures", 2
    text = "export-eval: no fixtures found under %s" % FIXTURES
elif failed:
    status, exit_code = "fail", 1
    lines = ["export-eval: FAIL — %d/%d fixtures passed" % (passed, total)]
    for r in failed:
        lines.append("  - %s: %s" % (r["name"], r["reason"]))
    text = "\n".join(lines)
else:
    status, exit_code = "ok", 0
    text = "export-eval: ok — %d/%d fixtures matched expected outcome" % (passed, total)

outputs = {"passed": passed, "total": total, "fixtures": results}
print(json.dumps({"exit": exit_code, "status": status, "outputs": outputs, "text": text},
                 ensure_ascii=False))
