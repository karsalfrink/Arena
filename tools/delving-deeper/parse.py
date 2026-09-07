#!/usr/bin/env python3
"""Parse the Delving Deeper reference rules (SingleFile HTML capture) into
tables.json (monster stat tables) and descriptions.json (monster prose).

Everything is located by heading text, never by absolute table/heading index.
Only the Python standard library is used.

Usage:  python3 parse.py [delving-deeper-rules.html]
"""
import html
import json
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else "delving-deeper-rules.html"

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

UNICODE_MAP = {
    "−": "-",    # minus sign
    "–": "-",    # en dash
    "—": "-",    # em dash
    "½": "1/2",  # one half
    "⅓": "1/3",
    "¼": "1/4",
    "×": "x",    # multiplication sign
    " ": " ",    # nbsp
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "…": "...",
}


def normalize(text):
    """Unescape entities, strip tags, map Unicode to ASCII, collapse space."""
    text = re.sub(r"<br\s*/?>", " ", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    for k, v in UNICODE_MAP.items():
        text = text.replace(k, v)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def anchor_of(fragment):
    m = re.search(r'href=["\']?#([\w-]+)', fragment)
    return m.group(1) if m else None


def id_of(tag_open):
    m = re.search(r'id=["\']?([\w-]+)', tag_open)
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# Locate the monster chapter
# ---------------------------------------------------------------------------

with open(SRC, encoding="utf-8") as fh:
    doc = fh.read()


def find_h2(title, start=0):
    m = re.compile(r"<h2[^>]*>\s*" + re.escape(title) + r"\s*</h2>").search(doc, start)
    if not m:
        sys.exit("Could not find <h2>%s</h2>" % title)
    return m.start()


monsters_start = find_h2("Monsters")
explanation_start = find_h2("Explanation of Monsters", monsters_start)
treasures_start = find_h2("Treasures", explanation_start)

chapter = doc[monsters_start:treasures_start]

# ---------------------------------------------------------------------------
# Tables (located by <h4> caption text)
# ---------------------------------------------------------------------------

TABLE_RE = re.compile(r"<h4[^>]*>(.*?)</h4>\s*<table.*?</table>", re.S)
ROW_RE = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S)
CELL_RE = re.compile(r"<t([dh])[^>]*>(.*?)</t[dh]>", re.S)


def find_tables():
    tables = {}
    for m in TABLE_RE.finditer(chapter):
        caption = normalize(m.group(1))
        rows = []
        for r in ROW_RE.finditer(m.group(0)):
            cells = []
            for c in CELL_RE.finditer(r.group(1)):
                cells.append({"kind": c.group(1), "text": normalize(c.group(2)),
                              "anchor": anchor_of(c.group(2))})
            rows.append(cells)
        tables.setdefault(caption, []).append(rows)
    return tables


raw_tables = find_tables()


def get_tables(caption):
    if caption not in raw_tables:
        sys.exit("Missing table caption: %s" % caption)
    return raw_tables[caption]


# --- Table 3.1 Summary of Monsters (plus continuations) ---------------------

SUMMARY_COLS = ["name", "number_appearing", "number_in_lair", "ac", "move",
                "hd", "lair_pct", "treasure", "align"]


def parse_summary():
    out = []
    group = None          # (group_name, group_anchor)
    all_rows = []
    for t in get_tables("Table 3.1 Summary of Monsters"):
        all_rows.extend(t)
    for t in get_tables("Table 3.1 (Continued) Summary of Monsters"):
        all_rows.extend(t)
    for cells in all_rows:
        if not cells or cells[0]["kind"] == "th":
            continue
        texts = [c["text"] for c in cells]
        if len(cells) == 1:                       # group header row
            group = (texts[0], cells[0]["anchor"])
            continue
        if len(cells) != len(SUMMARY_COLS):
            sys.exit("Unexpected summary row: %r" % texts)
        if texts[0] == "Type":
            continue  # repeated header row rendered with <td> cells
        anchor = cells[0]["anchor"]
        # Decide whether this row still belongs to the current group:
        # href-less rows always do; anchored rows do if the anchor is
        # prefixed by the group anchor (e.g. giants-hill under giants).
        if group is not None:
            if anchor is not None and not anchor.startswith(group[1] + "-"):
                group = None
        rec = dict(zip(SUMMARY_COLS, texts))
        rec["group"] = group[0] if group else None
        rec["anchor"] = anchor
        rec["qualified_name"] = (
            "%s, %s" % (group[0], rec["name"]) if group else rec["name"])
        out.append(rec)
    return out


summary = parse_summary()

# --- Generic small tables ---------------------------------------------------


def parse_simple(caption, cols, skip_header_rows=None):
    """Parse a single table whose data rows have len(cols) cells.
    Header (th) rows and footnote rows are skipped."""
    tables = get_tables(caption)
    if len(tables) != 1:
        sys.exit("Expected one table for %s, found %d" % (caption, len(tables)))
    out = []
    for cells in tables[0]:
        if not cells or cells[0]["kind"] == "th":
            continue
        texts = [c["text"] for c in cells]
        if len(texts) != len(cols):
            continue  # footnote / colspan row
        if texts[0] in ("Type", "Age"):
            continue  # header row rendered with <td> cells
        out.append(dict(zip(cols, texts)))
    return out


dragons_by_type = parse_simple(
    "Table 3.2 Dragons by Type",
    ["type", "habitat", "speaks_common", "magic_using", "breath_shape",
     "breath_type", "resistance"])

dragons_by_age = parse_simple(
    "Table 3.3 Dragons by Age Category",
    ["age", "years", "chance_sleeping", "breath_cone", "breath_line"])

DRAGON_TABLES = {
    "Black": "Table 3.4 Black Dragons",
    "Blue": "Table 3.5 Blue Dragons",
    "Golden": "Table 3.6 Golden Dragons",
    "Green": "Table 3.7 Green Dragons",
    "Red": "Table 3.8 Red Dragons",
    "White": "Table 3.9 White Dragons",
}
dragons = {}
for color, caption in DRAGON_TABLES.items():
    dragons[color] = parse_simple(
        caption, ["age", "ac", "move", "hd", "melee_dam", "align"])

giants = parse_simple(
    "Table 3.10 Giants",
    ["type", "lair", "height", "ac", "move", "hd", "melee_dam", "align"])

horses = parse_simple(
    "Table 3.11 Horses",
    ["type", "cost", "ac", "move", "hd", "carrying_capacity"])

rocs = parse_simple(
    "Table 3.12 Rocs",
    ["type", "wingspan", "ac", "move", "hd", "melee_dam"])

tables = {
    "summary": summary,
    "dragons_by_type": dragons_by_type,
    "dragons_by_age": dragons_by_age,
    "dragons": dragons,
    "giants": giants,
    "horses": horses,
    "rocs": rocs,
}

# ---------------------------------------------------------------------------
# Descriptions (<h5> headings between Explanation of Monsters and Treasures)
# ---------------------------------------------------------------------------

desc_section = doc[explanation_start:treasures_start]

# Sub-sections of the Dragons entry that are not monsters themselves.
NON_MONSTER_HEADINGS = {
    "Sleeping Dragons", "Dragon Breath Weapon", "Dragon Magic",
    "If Multiple Dragons", "Subduing Dragons", "Dragon Treasure",
}

H5_RE = re.compile(r"<h5([^>]*)>(.*?)</h5>", re.S)
HEAD_RE = re.compile(r"<h([345])([^>]*)>(.*?)</h\1>", re.S)
BLOCK_RE = re.compile(r"<(p|li)[^>]*>(.*?)</\1>", re.S)
STOP_RE = re.compile(r"<h[2-5][^>]*>")


def parse_descriptions():
    """Every <h3>/<h4>/<h5> in the section. <h5> entries are monsters (or the
    dragon sub-sections); <h3> entries are group introductions (Dragons,
    Elementals, Giants, ...) whose prose carries rules for the whole group;
    <h4> entries are table captions, some followed by rules text."""
    out = []
    heads = list(HEAD_RE.finditer(desc_section))
    for i, m in enumerate(heads):
        level = int(m.group(1))
        heading = normalize(m.group(3))
        start = m.end()
        # Body runs to the next heading of any level h2-h5.
        nxt = STOP_RE.search(desc_section, start)
        end = nxt.start() if nxt else len(desc_section)
        body = desc_section[start:end]
        # Drop any tables embedded in the body (they are parsed separately).
        body_no_tables = re.sub(r"<table.*?</table>", "", body, flags=re.S)
        paras = [normalize(b.group(2)) for b in BLOCK_RE.finditer(body_no_tables)]
        paras = [p for p in paras if p]
        if level != 5 and not paras:
            continue  # bare table caption
        out.append({
            "heading": heading,
            "level": level,
            "anchor": id_of(m.group(2)),
            "is_monster": level == 5 and heading not in NON_MONSTER_HEADINGS,
            "is_group": level == 3,
            "paragraphs": paras,
            "text": " ".join(paras),
        })
    return out


descriptions = parse_descriptions()

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

with open("tables.json", "w", encoding="utf-8") as fh:
    json.dump(tables, fh, indent=1, ensure_ascii=True)
with open("descriptions.json", "w", encoding="utf-8") as fh:
    json.dump(descriptions, fh, indent=1, ensure_ascii=True)

n_monsters = sum(1 for d in descriptions if d["is_monster"])
n_groups = sum(1 for d in descriptions if d["is_group"])
print("summary rows:      %d" % len(summary))
print("dragon tables:     %s" % ", ".join("%s=%d" % (k, len(v)) for k, v in dragons.items()))
print("giants/horses/rocs: %d/%d/%d" % (len(giants), len(horses), len(rocs)))
print("descriptions:      %d (%d monsters, %d group intros, %d other)"
      % (len(descriptions), n_monsters, n_groups,
         len(descriptions) - n_monsters - n_groups))
empty = [d["heading"] for d in descriptions if not d["paragraphs"]]
if empty:
    print("WARNING: empty descriptions: %s" % empty)
