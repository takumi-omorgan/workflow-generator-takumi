#!/usr/bin/env python3
"""fences-eval-check — run the marker-fence golden fixtures (ADR-054).

Exercises bin/lib/fences-fixtures/* through the real `bin/fence` CLI (proving
the CLI path and atomic write) for the transform ops, and the fences module
directly for round-trip identity and error cases. Byte-for-byte comparison
against each fixture's expected.md is the byte-stability proof for the one
destructive failure mode in the kit (silent fence corruption).

Prints a result JSON object {status, outputs, errors, text}; bin/fences-eval
renders it into the standard envelope. Exit 0 = all pass, 1 = a fixture failed.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fences  # noqa: E402

FIXTURES = os.path.join(HERE, "fences-fixtures")
FENCE_CLI = os.path.join(os.path.dirname(HERE), "fence")


def run_cli(args, cwd=None):
    proc = subprocess.run([FENCE_CLI] + args, capture_output=True, text=True, cwd=cwd)
    return proc.returncode, proc.stdout, proc.stderr


def check_fixture(name):
    """Return (ok, [problems])."""
    d = os.path.join(FIXTURES, name)
    op = json.load(open(os.path.join(d, "op.json"), encoding="utf-8"))
    input_path = os.path.join(d, "input.md")
    with open(input_path, encoding="utf-8") as fh:
        original = fh.read()
    problems = []
    kind = op["op"]

    if kind == "roundtrip":
        dialect = fences.DIALECTS[op["dialect"]]
        text = original
        for span in fences.list_zones(text, dialect):
            body = fences.read_zone(text, dialect, span.zone)
            text = fences.replace_zone(text, dialect, span.zone, body)
        if text != original:
            problems.append("round-trip changed the file (expected byte-identity)")
        return (not problems), problems

    if op.get("expectError"):
        rc, out, _ = run_cli([kind, "--file", input_path, "--dialect", op["dialect"],
                              "--format", "json"])
        if rc != 1:
            problems.append("expected exit 1 (malformed), got %d" % rc)
        try:
            env = json.loads(out)
            if env.get("status") != "error":
                problems.append("expected status 'error', got %r" % env.get("status"))
        except Exception as e:
            problems.append("envelope not parseable: %s" % e)
        return (not problems), problems

    # Transform op: copy input to a temp file, drive the real CLI, diff bytes.
    tmpdir = tempfile.mkdtemp(prefix="fences-eval.")
    try:
        target = os.path.join(tmpdir, "work.md")
        shutil.copyfile(input_path, target)
        args = [kind, "--file", target]
        if kind != "collapse":
            args += ["--dialect", op["dialect"]]
        if "zone" in op:
            args += ["--zone", op["zone"]]
        if "body" in op:
            args += ["--body", op["body"]]
        elif "bodyFile" in op:
            args += ["--body-file", os.path.join(d, op["bodyFile"])]
        rc, out, err = run_cli(args)
        if rc != 0:
            problems.append("CLI exit %d (stderr: %s)" % (rc, err.strip()))
            return False, problems
        with open(target, encoding="utf-8") as fh:
            actual = fh.read()
        exp_path = os.path.join(d, "expected.md")
        with open(exp_path, encoding="utf-8") as fh:
            expected = fh.read()
        if actual != expected:
            problems.append("output != expected.md")
        # Idempotency: applying the same op again is a no-op for replace.
        if kind == "replace":
            rc2, _, _ = run_cli(args)
            with open(target, encoding="utf-8") as fh:
                again = fh.read()
            if again != expected:
                problems.append("re-applying replace was not idempotent")
        return (not problems), problems
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def unit_invariants():
    """A few in-process assertions independent of fixtures."""
    problems = []
    t = "a\n<!-- state:x:start -->\n<!-- state:x:end -->\nb\n"
    # empty body stays adjacent / round-trips
    if fences.replace_zone(t, fences.STATE, "x", fences.read_zone(t, fences.STATE, "x")) != t:
        problems.append("empty-zone round-trip not identity")
    # collapse preserves single trailing newline
    if fences.collapse_blank_lines("x\n\n\n") != "x\n":
        problems.append("collapse did not normalise trailing blanks")
    # upsert adds a missing zone
    up = fences.upsert_zone("head\n", fences.STATE, "new", "body")
    if "state:new:start" not in up or "body" not in up:
        problems.append("upsert_zone did not insert a new zone")
    return problems


def main():
    if not os.path.isdir(FIXTURES):
        print(json.dumps({"status": "error", "outputs": {},
                          "errors": [{"code": "no-fixtures", "message": FIXTURES}],
                          "text": "fences-eval: no fixtures directory"}))
        return 2
    results = []
    for name in sorted(os.listdir(FIXTURES)):
        if not os.path.isdir(os.path.join(FIXTURES, name)):
            continue
        ok, problems = check_fixture(name)
        results.append({"name": name, "ok": ok, "problems": problems})
    unit_problems = unit_invariants()

    passed = sum(1 for r in results if r["ok"]) + (0 if unit_problems else 1)
    total = len(results) + 1  # +1 for the unit-invariants bundle
    failed = [r for r in results if not r["ok"]]
    status = "ok" if (not failed and not unit_problems) else "fail"

    lines = []
    for r in results:
        lines.append("  %s %s" % ("PASS" if r["ok"] else "FAIL", r["name"]))
        for p in r["problems"]:
            lines.append("      - " + p)
    lines.append("  %s unit-invariants" % ("PASS" if not unit_problems else "FAIL"))
    for p in unit_problems:
        lines.append("      - " + p)
    header = "fences-eval: %s — %d/%d checks passed" % (status, passed, total)
    text = header + "\n" + "\n".join(lines)

    outputs = {"passed": passed, "total": total,
               "fixtures": results, "unitProblems": unit_problems}
    print(json.dumps({"status": status, "outputs": outputs, "errors": [], "text": text}))
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
