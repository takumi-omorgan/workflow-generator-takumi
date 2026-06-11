#!/usr/bin/env python3
"""export-transform.py — apply the public-export TRANSFORM rules in place.

Operates on a staging tree (already archived + pruned by bin/export-public).
Rewrites shipping text files OUTSIDE examples/ so the public artifact carries
no old repo names, stale version pins, personal paths, or orphaned links into
the now-excluded kit ADR set. Example-project content is exempt from blind
rewrites (it is illustrative kit output). Deterministic; prints a one-line
JSON summary on stdout.

Environment (set by bin/export-public):
    DEST, VERSION, PUBLIC_REPO, SOURCE_OWNER, SOURCE_REPO, OLD_PUBLIC_REPO
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_paths import (  # noqa: E402
    PRIVATE_SECTION_HEADINGS, classify_link, heading_anchor, is_excluded,
    is_export_fixture, link_target_relpath,
)

DEST = os.environ["DEST"]
VERSION = os.environ["VERSION"]
PUBLIC_REPO = os.environ["PUBLIC_REPO"]
SOURCE_OWNER = os.environ["SOURCE_OWNER"]
SOURCE_REPO = os.environ["SOURCE_REPO"]
OLD_PUBLIC_REPO = os.environ["OLD_PUBLIC_REPO"]

PUBLIC_SLUG = PUBLIC_REPO.split("/", 1)[1] if "/" in PUBLIC_REPO else PUBLIC_REPO
SOURCE_SLUG = SOURCE_REPO.split("/", 1)[1] if "/" in SOURCE_REPO else SOURCE_REPO

TEXT_EXTS = {".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt"}

# Directories whose contents are exempt from blind rewrites.
EXEMPT_PREFIXES = (os.path.join(DEST, "examples") + os.sep,)

# Ordered substitution rules (longest / most specific first so a broad rule
# never eats a more specific one).
NAME_RULES = [
    (SOURCE_REPO, PUBLIC_REPO),            # takumi-omorgan/workflow-generator-takumi -> public
    (OLD_PUBLIC_REPO, PUBLIC_REPO),        # olivermorgan2/workflow-generator -> public
    (SOURCE_SLUG, PUBLIC_SLUG),            # workflow-generator-takumi -> claude-workflow-kit
    (SOURCE_OWNER, PUBLIC_REPO.split("/", 1)[0]),  # takumi-omorgan -> olivermorgan2
]

# Personal-path scrubs: drop whole lines that reference a personal location
# (these only appear in the kit CLAUDE.md dogfooding section and stray docs).
PERSONAL_LINE_MARKERS = ["~/dotfiles", "~/src/workflow-generator", "/Users/hermes"]

# Markdown links that RESOLVE into an excluded private/source path are
# de-linked to their anchor text (the link checker flags them otherwise).
# This is resolution-based and applies everywhere — including examples/ —
# so examples/README.md's links into the excluded kit design/adr are fixed,
# while example-PROJECT links (which resolve to examples/.../design/adr, not
# excluded) and illustrative placeholders are left intact.
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

# Version pins: any vN.N.N tag literal -> the export version, but only on
# lines that actually pin a release/download/branch (avoid rewriting prose
# that legitimately references historical versions, e.g. a changelog).
TAG_RE = re.compile(r"\bv\d+\.\d+\.\d+\b")
PIN_CONTEXT_RE = re.compile(r"releases/download|--branch=|release download|WORKFLOW_KIT_VERSION")

counts = {"nameRewrites": 0, "versionRewrites": 0, "adrLinksDelinked": 0,
          "personalLinesScrubbed": 0, "privateSectionsRemoved": 0,
          "filesChanged": 0}


def is_exempt(path):
    return any(path.startswith(p) for p in EXEMPT_PREFIXES)


def delink_private(text, md_rel):
    """De-link any markdown link that resolves into an excluded private path.
    Applies to every shipping file, including examples/."""
    def _sub(m):
        anchor, target = m.group(1), m.group(2).strip()
        raw = target.split(" ", 1)[0] if (" " in target and not target.startswith("<")) else target
        if classify_link(raw) == "relative":
            resolved = link_target_relpath(md_rel, raw)
            if resolved is not None and is_excluded(resolved):
                counts["adrLinksDelinked"] += 1
                return anchor
        return m.group(0)
    return LINK_RE.sub(_sub, text)


def remove_private_sections(text, md_rel):
    """Remove whole private/dogfooding sections (PRIVATE_SECTION_HEADINGS)
    from their file: heading line through the line before the next "## "
    heading, or EOF. Removing the section wholesale keeps the personal-path
    line scrub from leaving empty code blocks and broken prose behind.
    Lines linking to a removed heading's anchor are dropped too (the source
    keeps such cross-references on their own line so this stays clean)."""
    headings = [h for (rel, h) in PRIVATE_SECTION_HEADINGS if rel == md_rel]
    if not headings:
        return text, False
    lines = text.split("\n")
    out, i, removed = [], 0, False
    while i < len(lines):
        if any(lines[i].startswith(h) for h in headings):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("## "):
                j += 1
            # drop blank/separator lines left dangling above the heading,
            # then keep exactly one blank line before the next heading
            while out and out[-1].strip() in ("", "---"):
                out.pop()
            if j < len(lines) and out:
                out.append("")
            counts["privateSectionsRemoved"] += 1
            removed = True
            i = j
            continue
        out.append(lines[i])
        i += 1
    anchors = ["#" + heading_anchor(h) for h in headings]
    kept = [ln for ln in out if not any(a in ln for a in anchors)]
    if kept != out:
        removed = True
        out = kept
    return "\n".join(out), removed


def transform_text(text, md_rel, exempt):
    changed = False

    # remove private/dogfooding sections before any line-level scrubbing
    new, removed = remove_private_sections(text, md_rel)
    if removed:
        changed = True
        text = new
        if not text.endswith("\n"):
            text += "\n"

    # de-link orphaned links into excluded private paths (always)
    new = delink_private(text, md_rel)
    if new != text:
        changed = True
        text = new

    # the remaining rewrites are blind substitutions; exempt example bodies
    if exempt:
        return text, changed

    # name rewrites
    for old, repl in NAME_RULES:
        if old and old in text:
            n = text.count(old)
            text = text.replace(old, repl)
            counts["nameRewrites"] += n
            changed = True

    # version-pin rewrites (line-scoped to install/download/branch contexts)
    out_lines = []
    for line in text.split("\n"):
        if PIN_CONTEXT_RE.search(line):
            def _pin(m):
                if m.group(0) != VERSION:
                    counts["versionRewrites"] += 1
                    return VERSION
                return m.group(0)
            newline = TAG_RE.sub(_pin, line)
            if newline != line:
                changed = True
            out_lines.append(newline)
        else:
            out_lines.append(line)
    text = "\n".join(out_lines)

    # personal-path line scrub
    kept = []
    for line in text.split("\n"):
        if any(mark in line for mark in PERSONAL_LINE_MARKERS):
            counts["personalLinesScrubbed"] += 1
            changed = True
            continue
        kept.append(line)
    text = "\n".join(kept)

    return text, changed


for root, dirs, files in os.walk(DEST):
    dirs.sort()
    if ".git" in dirs:
        dirs.remove(".git")
    for name in sorted(files):
        full = os.path.join(root, name)
        md_rel = os.path.relpath(full, DEST).replace(os.sep, "/")
        # the export verifier's own fixtures are opaque test data — never
        # transform them (would corrupt the deliberate leak/link inputs)
        if is_export_fixture(md_rel):
            continue
        ext = os.path.splitext(name)[1]
        known = ext in TEXT_EXTS or name == ".gitignore"
        try:
            with open(full, encoding="utf-8") as fh:
                original = fh.read()
        except (UnicodeDecodeError, OSError):
            continue
        # also process extensionless scripts (bin/*) detected by shebang
        if not known and not original.startswith("#!"):
            continue
        new, changed = transform_text(original, md_rel, is_exempt(full))
        if changed:
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(new)
            counts["filesChanged"] += 1

print(json.dumps(counts, ensure_ascii=False))
