#!/usr/bin/env python3
"""export-changelog.py — extract one version's section from a changelog.

Source-repo-only export tooling (pruned from the public artifact with the
rest of the export tooling; see export_paths.py EXPORT_TOOLING_PATHS).

Modes:
  --mode notes   print the section BODY only (no heading) — feed to
                 `gh release create --notes-file`; the release title
                 supplies the version.
  --mode public  print a curated public changelog: "# Changelog" header,
                 a one-line curation intro, the section (heading + body),
                 and a one-line trailer.

`Range:` lines are dropped in both modes (they reference source-repo tag
ranges that do not resolve in the public repo). Reads FILE, or stdin when
FILE is `-`. Exits 0 on success, 1 if the section is missing or appears
more than once, 2 on invocation error.

Usage: export-changelog.py --mode notes|public --version vX.Y.Z FILE|-
"""

import re
import sys


def fail(code, msg):
    print("export-changelog: %s" % msg, file=sys.stderr)
    sys.exit(code)


def parse_args(argv):
    mode = version = path = None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--mode" and i + 1 < len(argv):
            mode = argv[i + 1]
            i += 2
        elif a == "--version" and i + 1 < len(argv):
            version = argv[i + 1]
            i += 2
        elif a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif path is None:
            path = a
            i += 1
        else:
            fail(2, "unexpected argument: %s" % a)
    if mode not in ("notes", "public"):
        fail(2, "--mode must be notes or public")
    if not version:
        fail(2, "--version is required")
    if not version.startswith("v"):
        version = "v" + version
    if path is None:
        fail(2, "changelog FILE (or -) is required")
    return mode, version, path


def main():
    mode, version, path = parse_args(sys.argv[1:])
    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            fail(2, "cannot read %s: %s" % (path, exc))
    lines = text.split("\n")
    head_re = re.compile(r"^## %s\b" % re.escape(version))
    any_head_re = re.compile(r"^## ")
    starts = [i for i, ln in enumerate(lines) if head_re.match(ln)]
    if len(starts) != 1:
        fail(1, "expected exactly one '## %s' section, found %d"
             % (version, len(starts)))
    start = starts[0]
    end = next((i for i in range(start + 1, len(lines))
                if any_head_re.match(lines[i])), len(lines))
    section = [ln for ln in lines[start:end] if not ln.startswith("Range:")]
    while section and not section[-1].strip():
        section.pop()
    if mode == "notes":
        body = section[1:]
        while body and not body[0].strip():
            body.pop(0)
        print("\n".join(body))
    else:
        out = [
            "# Changelog",
            "",
            "This public changelog is curated from tagged releases.",
            "",
        ] + section + [
            "",
            "Earlier development history is maintained in the source "
            "repository; public releases are curated from tagged releases.",
        ]
        print("\n".join(out))


if __name__ == "__main__":
    main()
