#!/usr/bin/env python3
"""export_paths.py — shared public-export path classification (issue #16).

Single source of truth, imported by both the verifier
(check-public-export.py) and the transformer (export-transform.py), so the
exclusion boundary and the "link points into an excluded path" rule never
drift apart.

The boundary is ROOT-ANCHORED to the kit's own private/source paths. Nested
example-project content (examples/projects/*/design/**) is deliberately NOT
excluded — those are illustrative kit output and still ship — which is why
classification works on a path RELATIVE TO THE EXPORT ROOT, not on substring
matches like "design/adr".
"""

import os
import re

# A tree-relative POSIX path is an excluded private/source path iff it
# matches one of these. Used both to assert excluded paths are absent and to
# decide whether a markdown link points into private/source material.
_ROOT_DESIGN_REPORT = re.compile(r"design/[^/]+\.md$")
_PROMPT_NON_TEMPLATE = re.compile(r"prompts/(?!_template\.md$)[^/]+$")

# Kit-private root directories that never ship. Shared by is_excluded() and
# the .gitignore scrub/check so the boundary cannot drift.
# knowledge/ is the source repo's internal knowledge layer (project brief,
# risks, open questions, review findings) — private to development, like
# notes/ and archive/, and replaced publicly by docs/.
PRIVATE_ROOT_DIRS = ("notes", "archive", ".hermes", "knowledge")

# Version-pin classification, shared by the transform (which rewrites stale
# tags on pin-context lines) and the verifier (which asserts none survive):
# a vN.N.N literal counts as a PIN only on lines that actually pin a
# release/download/branch — prose that legitimately references historical
# versions (e.g. a changelog narrative) is not a pin.
VERSION_TAG_RE = re.compile(r"\bv\d+\.\d+\.\d+\b")
PIN_CONTEXT_RE = re.compile(
    r"releases/download|--branch=|release download|WORKFLOW_KIT_VERSION")


def is_excluded(relpath):
    """relpath: POSIX path relative to the export root."""
    rp = relpath.strip("/")
    if rp == "design/adr" or rp.startswith("design/adr/"):
        return True
    if rp.startswith("design/prd-addenda/") or rp == "design/prd-addenda":
        return True
    if _ROOT_DESIGN_REPORT.fullmatch(rp):
        return True
    for d in PRIVATE_ROOT_DIRS:
        if rp == d or rp.startswith(d + "/"):
            return True
    if rp == "ai-review/config.json" or rp.startswith("ai-review/artifacts/"):
        return True
    if _PROMPT_NON_TEMPLATE.fullmatch(rp):
        return True
    return False


# The public-export tooling is SOURCE-REPO ONLY: it produces and verifies the
# public artifact and is not part of it (a published distribution does not
# re-publish itself). Shipping it would also be self-referential — the verifier
# would flag its own leak-pattern literals, and the transform would scrub the
# verifier's own source-owner constants. So the export prunes this set and
# reconciles kit.json / self-test / docs to match.
EXPORT_TOOLING_PATHS = (
    "bin/check-public-export",
    "bin/export-public",
    "bin/export-eval",
    "bin/lib/check-public-export.py",
    "bin/lib/export-changelog.py",
    "bin/lib/export-transform.py",
    "bin/lib/export-eval-check.py",
    "bin/lib/export-reconcile.py",
    "bin/lib/export_paths.py",
    "bin/export-eval-fixtures",
    "docs/publishing.md",
)


# Sections of shipping files that are private/dogfooding-only. The export
# transform removes each section (heading line through the line before the
# next "## " heading, or EOF) so the personal-path scrub never has to chew
# through them line by line; verifier check I asserts none survive. Both
# sides share this constant so the removal rule and the contract never
# drift apart.
PRIVATE_SECTION_HEADINGS = (
    ("CLAUDE.md", "## Source-repo contributor notes"),
    ("CLAUDE.md", "## Developing the kit on itself"),
    ("docs/install.md", "## Contributor / kit-developer setup"),
)


def heading_anchor(heading):
    """GitHub-style anchor slug for a markdown heading (or heading prefix).

    Used to scrub and to detect intra-doc links to removed private sections:
    the transform drops whole lines that link to a removed heading's anchor,
    and verifier check I flags any such anchor reference that survives.
    A PRIVATE_SECTION_HEADINGS entry may be a prefix of the real heading, so
    consumers match by substring containment of the prefix slug."""
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def is_export_tooling(relpath):
    rp = relpath.replace("\\", "/").lstrip("./")
    for t in EXPORT_TOOLING_PATHS:
        if rp == t or rp.startswith(t + "/"):
            return True
    return False


def is_export_fixture(relpath):
    """The export verifier's own eval fixtures (bin/export-eval-fixtures/**)
    are synthetic test inputs that deliberately embed leak strings and
    orphaned links. They are SOURCE-ONLY: bin/export-public prunes them from
    the public artifact along with the rest of the export tooling (see
    EXPORT_TOOLING_PATHS). This guard exists so the verifier and the
    transformer stay inert over trees that still contain them — e.g. when
    either is run over the source repo itself — instead of corrupting the
    fixtures or raising false-positive leaks."""
    rp = relpath.replace("\\", "/").lstrip("./")
    return rp == "bin/export-eval-fixtures" or rp.startswith("bin/export-eval-fixtures/")


# A .gitignore line (pattern or comment) references a kit-private root when
# it names notes/, archive/, or .hermes — patterns for source-only tooling
# outputs (and the comments documenting them) must not ship. The guard before
# each name keeps words that merely end in a root name (e.g. "footnotes/")
# from matching.
_GITIGNORE_PRIVATE_RE = re.compile(
    r"(?:^|[^\w.-])(?:%s)" % "|".join(
        re.escape(d) + ("" if d.startswith(".") else "/")
        for d in PRIVATE_ROOT_DIRS))


def gitignore_line_is_private(line):
    """True if a .gitignore line references a kit-private root that never
    ships in the public export. Used by the transform (to scrub the line or
    its whole block) and by the verifier (to flag any survivor)."""
    return bool(_GITIGNORE_PRIVATE_RE.search(line))


def classify_link(target):
    """Return the link's target kind: 'external', 'anchor', 'absolute',
    or 'relative'. Only 'relative' links make a claim about a path inside the
    export tree."""
    t = target.strip()
    if not t:
        return "empty"
    low = t.lower()
    if low.startswith(("http://", "https://", "mailto:", "tel:", "ftp://", "//")):
        return "external"
    if t.startswith("#"):
        return "anchor"
    if t.startswith("/"):
        return "absolute"
    return "relative"


def link_target_relpath(md_file_relpath, target):
    """Resolve a relative markdown link target against the linking file's
    directory and return the export-root-relative POSIX path (or None if the
    link escapes the tree). md_file_relpath is the linking .md file relative
    to the export root; target is the raw link target (anchors/queries are
    stripped here)."""
    target_path = re.split(r"[#?]", target, 1)[0].strip().strip("<>")
    if not target_path:
        return None
    base_dir = os.path.dirname(md_file_relpath)
    resolved = os.path.normpath(os.path.join(base_dir, target_path))
    resolved = resolved.replace(os.sep, "/")
    if resolved.startswith("../") or resolved == "..":
        return None  # escapes the export root
    return resolved
