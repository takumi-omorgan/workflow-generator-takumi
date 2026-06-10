#!/usr/bin/env python3
"""schema_read — dependency-free readers for the kit's schemas/*.yaml (ADR-054).

The kit deliberately ships no YAML parser; schema constraints are read with
targeted line-based extraction (the same approach bin/validate-kit-json uses).
This module is the single shared home for that extraction so both
bin/validate-carry-forward and bin/validate-schema read the constraints FROM
the schema file rather than keeping a second copy of the rules.

Two readers:

  read_schema(path)  -> (required, patterns, fields, additional)
      The minimal tuple bin/validate-carry-forward has always used. Kept
      byte-for-byte identical to its previous inline definition so extracting
      it changes no behavior.

  load_schema(path)  -> dict
      A richer structured view used by the general validator: unit (object|
      list), item.required, item.additionalFields, and per-field type / const
      / enum / pattern.
"""

import re


def read_schema(path):
    """Return (required, patterns, fields, additional) for a list-of-objects
    schema. Targeted line-based extraction (same dependency-free approach as
    bin/validate-kit-json). Preserved verbatim from validate-carry-forward.
    """
    required, patterns, fields = [], {}, []
    additional = "allow"
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    section = None          # "required" | "fields" | None
    cur_field = None
    for ln in lines:
        if re.match(r"^  required:\s*$", ln):
            section = "required"; continue
        if re.match(r"^  fields:\s*$", ln):
            section = "fields"; cur_field = None; continue
        m = re.match(r"^  additionalFields:\s*(\S+)", ln)
        if m:
            additional = m.group(1).strip(); section = None; continue
        # any other 2-space top-level key under item: ends a section
        if re.match(r"^  [A-Za-z]", ln) and not re.match(r"^   ", ln):
            section = None
        if section == "required":
            m = re.match(r"^    - (.+?)\s*$", ln)
            if m:
                required.append(m.group(1).strip().strip("\"\x27"))
        elif section == "fields":
            m = re.match(r"^    ([A-Za-z][\w-]*):\s*$", ln)
            if m:
                cur_field = m.group(1); fields.append(cur_field); continue
            m = re.match(r"^      pattern:\s*(.+?)\s*$", ln)
            if m and cur_field:
                patterns[cur_field] = m.group(1).strip().strip("\"\x27")
    return required, patterns, fields, additional


def _scalar(raw):
    return raw.strip().strip("\"\x27")


def load_schema(path):
    """Return a structured view of a kit schema:

        {"schema": str|None, "version": str|None, "unit": "object"|"list",
         "required": [...], "additionalFields": "allow"|"forbid",
         "fields": {name: {"type":..., "const":..., "enum":[...], "pattern":...}}}

    Line-based, no YAML dependency. Recognises the two-space `item:` block used
    by every kit schema; per-field attributes live at six-space indent and enum
    members at eight. `description:` blocks are ignored.
    """
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    out = {"schema": None, "version": None, "unit": "object",
           "required": [], "additionalFields": "allow", "fields": {}}
    section = None        # under item: "required" | "fields" | None
    cur_field = None
    in_enum = False
    in_desc = False
    for ln in lines:
        # top-level (col 0) keys
        m = re.match(r"^schema:\s*(.+?)\s*$", ln)
        if m:
            out["schema"] = _scalar(m.group(1)); continue
        m = re.match(r"^version:\s*(.+?)\s*$", ln)
        if m:
            out["version"] = _scalar(m.group(1)); continue
        m = re.match(r"^unit:\s*(\S+)", ln)
        if m:
            out["unit"] = m.group(1).strip(); continue

        # two-space keys under item:
        if re.match(r"^  required:\s*$", ln):
            section = "required"; in_enum = in_desc = False; continue
        if re.match(r"^  fields:\s*$", ln):
            section = "fields"; cur_field = None; in_enum = in_desc = False; continue
        m = re.match(r"^  additionalFields:\s*(\S+)", ln)
        if m:
            out["additionalFields"] = m.group(1).strip(); section = None; continue
        if re.match(r"^  [A-Za-z]", ln) and not re.match(r"^   ", ln):
            # another 2-space item key (e.g. type:) ends the current section
            section = None; in_enum = in_desc = False

        if section == "required":
            m = re.match(r"^    - (.+?)\s*$", ln)
            if m:
                out["required"].append(_scalar(m.group(1)))
            continue

        if section == "fields":
            # a 4-space field name starts a field definition
            m = re.match(r"^    ([A-Za-z][\w-]*):\s*$", ln)
            if m:
                cur_field = m.group(1)
                out["fields"][cur_field] = {"type": None, "const": None,
                                            "enum": None, "pattern": None}
                in_enum = in_desc = False
                continue
            if cur_field is None:
                continue
            fld = out["fields"][cur_field]
            # description blocks: ignore until the next 6-space attr/field
            if re.match(r"^      description:", ln):
                in_desc = True; in_enum = False; continue
            m = re.match(r"^      type:\s*(\S+)", ln)
            if m:
                fld["type"] = m.group(1).strip(); in_enum = in_desc = False; continue
            m = re.match(r"^      const:\s*(.+?)\s*$", ln)
            if m:
                fld["const"] = _scalar(m.group(1)); in_enum = in_desc = False; continue
            m = re.match(r"^      pattern:\s*(.+?)\s*$", ln)
            if m:
                fld["pattern"] = _scalar(m.group(1)); in_enum = in_desc = False; continue
            if re.match(r"^      enum:\s*$", ln):
                fld["enum"] = []; in_enum = True; in_desc = False; continue
            if in_enum:
                m = re.match(r"^        - (.+?)\s*$", ln)
                if m:
                    fld["enum"].append(_scalar(m.group(1)))
                    continue
                # a non-enum-item 6-space line ends the enum
                if re.match(r"^      \S", ln):
                    in_enum = False
            # otherwise (description continuation, blank) ignore
            continue
    return out
