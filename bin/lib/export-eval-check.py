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

When CHANGELOG_HELPER is set, one synthetic `helper:export-changelog`
result is appended: it drives lib/export-changelog.py over an inline
sample changelog (via stdin) and asserts the notes/public extraction
behavior the export pipeline and publication runbook rely on.

Environment (set by bin/export-eval):
    CHECKER           path to bin/check-public-export
    FIXTURES          fixtures root directory
    CHANGELOG_HELPER  path to lib/export-changelog.py (optional)
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

CHANGELOG_HELPER = os.environ.get("CHANGELOG_HELPER")
if CHANGELOG_HELPER:
    SAMPLE = (
        "# Changelog\n\n"
        "## v2.0.0 — current (2026-01-02)\n\n"
        "Range: `v1.0.0..v2.0.0`\n\n"
        "- current entry\n\n"
        "## v1.0.0 — old (2026-01-01)\n\n"
        "- old entry\n"
    )

    def run_helper(mode, version):
        proc = subprocess.run(
            [sys.executable, CHANGELOG_HELPER,
             "--mode", mode, "--version", version, "-"],
            input=SAMPLE, capture_output=True, text=True)
        return proc.returncode, proc.stdout

    problems = []
    rc, out = run_helper("notes", "v2.0.0")
    if rc != 0:
        problems.append("notes mode exited %d, expected 0" % rc)
    elif out != "- current entry\n":
        problems.append("notes mode emitted %r, expected the section body only"
                        % out)
    rc, out = run_helper("public", "v2.0.0")
    if rc != 0:
        problems.append("public mode exited %d, expected 0" % rc)
    else:
        heads = [ln for ln in out.split("\n") if ln.startswith("## v")]
        if not out.startswith("# Changelog\n"):
            problems.append("public mode output must start with '# Changelog'")
        if heads != ["## v2.0.0 — current (2026-01-02)"]:
            problems.append("public mode must keep exactly the requested "
                            "section heading, got %r" % heads)
        if "Range:" in out or "old entry" in out:
            problems.append("public mode must drop Range: lines and other "
                            "version sections")
    rc, _ = run_helper("notes", "v9.9.9")
    if rc != 1:
        problems.append("missing version exited %d, expected 1" % rc)

    results.append({
        "name": "helper:export-changelog",
        "ok": not problems,
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
