#!/usr/bin/env python3
"""Validate an Arena monster CSV the way Arena's Java loader would, and
cross-check the Delving Deeper file against tables.json.

Checks:
  (a) AC, MV, Lair% parse as Integer.parseInt ("-" means 0); HD matches
      Monster.parseHitDice's regex (\\d+)([x/]\\d+)?([+-]\\d+)?
  (b) Number and Dam match Dice's regex or are a plain integer
  (c) every Special entry matches SpecialAbility.createFromString and names
      a SpecialType enum constant (Flight/Swimming/WebMove are reported
      separately as master-file conventions that Arena ignores)
  (d) AC / HD / Align of each row agree with tables.json via mapping.json
      (only for the Delving Deeper file)
plus column count, single-character Treas/Align/Type/Env, dragon-age
prefixes, duplicate names and the names summons look up.

Usage:  python3 validate.py [csv ...]     (default: the Delving Deeper file)
Exit status is 1 if any error was found.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
DD_CSV = os.path.join(ROOT, "MonsterDatabase-DelvingDeeper.csv")

COLUMNS = ["Monster", "Number", "AC", "MV", "HD", "Lair%", "Treas", "Atk",
           "Dam", "Align", "Type", "EHD", "HDD", "Env", "Source", "Special"]

HD_RE = re.compile(r"(\d+)([x/]\d+)?([+-]\d+)?")           # Monster.parseHitDice
DICE_RE = re.compile(r"([1-9]\d*)?d([1-9]\d*)([/x][1-9]\d*)?([+-]\d+)?")  # Dice(String)
SPECIAL_RE = re.compile(r"(\w+)( \(([-]?\d+))?\)?")         # SpecialAbility.createFromString
INT_RE = re.compile(r"[+-]?\d+")                             # Integer.parseInt (loosely)

MOVEMENT_WORDS = {"Flight", "Swimming", "WebMove"}
TYPE_LETTERS = set("ABFHMSUX")
ENV_LETTERS = set("DWUX")
ALIGN_LETTERS = set("LNC")
DRAGON_AGES = ["Very Young", "Young", "Sub-Adult", "Adult", "Old", "Very Old"]
SUMMONS = {"SummonVermin": "Wolf", "SummonTrees": "Animated Tree"}


def load_enum():
    """Extract the SpecialType constants from SpecialType.java."""
    with open(os.path.join(ROOT, "SpecialType.java"), encoding="utf-8") as fh:
        src = fh.read()
    body = src[src.index("public enum SpecialType {"):]
    body = body[body.index("{") + 1:]
    body = body[:body.index(";")]
    body = re.sub(r"//.*", "", body)
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    return set(re.findall(r"\b[A-Za-z]\w*\b", body))


def java_int(s):
    """Mimic CSVReader.parseInt: '-' -> 0, else Integer.parseInt."""
    if s == "-":
        return 0
    if not INT_RE.fullmatch(s):
        raise ValueError(s)
    return int(s)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.infos = []

    def error(self, row, msg):
        self.errors.append("%s: %s" % (row, msg))

    def warn(self, row, msg):
        self.warnings.append("%s: %s" % (row, msg))

    def info(self, row, msg):
        self.infos.append("%s: %s" % (row, msg))


def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh))
    header, data = rows[0], rows[1:]
    return header, data


# ---------------------------------------------------------------------------
# (a)-(c) format checks
# ---------------------------------------------------------------------------


def check_format(path, enum, rep):
    header, data = read_csv(path)
    if header != COLUMNS:
        rep.error("header", "columns are %r" % header)
    names = []
    unknown_counts = {}
    for i, fields in enumerate(data, start=2):
        # CSVReader trims trailing commas, so a short row is possible.
        if len(fields) != len(COLUMNS):
            rep.error("line %d" % i, "%d fields, expected %d" % (len(fields), len(COLUMNS)))
            continue
        r = dict(zip(COLUMNS, fields))
        name = r["Monster"]
        tag = "%s (line %d)" % (name, i)
        names.append(name)

        # (a) integers and HD
        for col in ("AC", "MV", "Lair%"):
            try:
                java_int(r[col])
            except ValueError:
                rep.error(tag, "%s %r would fail Integer.parseInt" % (col, r[col]))
        if not HD_RE.fullmatch(r["HD"]):
            rep.error(tag, "HD %r: 'Could not parse hit dice descriptor'" % r["HD"])
        elif re.fullmatch(r"\d+-\d+", r["HD"]) and int(r["HD"].split("-")[1]) > 3:
            rep.warn(tag, "HD %r parses as HD minus hp; was a range intended?" % r["HD"])
        # (b) dice
        for col in ("Number", "Dam"):
            v = r[col]
            if not DICE_RE.fullmatch(v) and not INT_RE.fullmatch(v):
                rep.error(tag, "%s %r matches neither the Dice regex nor an integer" % (col, v))
        if not INT_RE.fullmatch(r["Atk"]):
            rep.error(tag, "Atk %r is not an integer" % r["Atk"])
        # single-character columns
        for col, allowed in (("Treas", None), ("Align", ALIGN_LETTERS),
                             ("Type", TYPE_LETTERS), ("Env", ENV_LETTERS)):
            v = r[col]
            if len(v) != 1:
                rep.error(tag, "%s %r must be one character (charAt(0) is used)" % (col, v))
            elif allowed and v not in allowed:
                rep.error(tag, "%s %r not in %s" % (col, v, "".join(sorted(allowed))))
        if r["EHD"] != "?" and not INT_RE.fullmatch(r["EHD"]):
            rep.error(tag, "EHD %r is neither '?' nor an integer" % r["EHD"])
        try:
            float(r["HDD"])
        except ValueError:
            rep.warn(tag, "HDD %r is not a float (parseFloat falls back to 0)" % r["HDD"])
        # (c) specials
        sp = r["Special"]
        if len(sp) > 1:
            for part in sp.split(", "):
                m = SPECIAL_RE.fullmatch(part)
                if not m:
                    rep.error(tag, "Special %r: 'Invalid special ability format'" % part)
                    continue
                nm = m.group(1)
                if nm in enum:
                    continue
                if nm in MOVEMENT_WORDS:
                    unknown_counts[nm] = unknown_counts.get(nm, 0) + 1
                else:
                    rep.error(tag, "Special %r is not a SpecialType constant (silently dropped)" % nm)
        elif sp not in ("-", ""):
            rep.warn(tag, "Special %r has length 1 and is ignored" % sp)
        # dragon naming
        if name.endswith("Dragon"):
            if not any(name.startswith(a) for a in DRAGON_AGES):
                rep.warn(tag, "dragon without an age prefix (age will be rolled randomly)")
        # summons targets
        for special, target in SUMMONS.items():
            if special in sp and target not in [d[0] for d in data]:
                rep.error(tag, "%s needs a row named %r" % (special, target))
    dupes = sorted(set(n for n in names if names.count(n) > 1))
    for d in dupes:
        rep.error(d, "duplicate monster name")
    for nm, cnt in sorted(unknown_counts.items()):
        rep.info("Special", "%s used %d times: master-file convention, "
                 "not a SpecialType; Arena ignores it (shows in MonsterMetrics -u)" % (nm, cnt))
    return data


# ---------------------------------------------------------------------------
# (d) cross-check against tables.json
# ---------------------------------------------------------------------------


def first_int(s):
    m = re.match(r"\s*(-?\d+)", s)
    return int(m.group(1)) if m else 0


def align_char(s):
    return "N" if s.strip() == "Any" else s.strip()[0]


def hd_values(hd):
    """Expected HD strings for a table HD cell: '5-12' -> 5..12, '8/12/16',
    '2+2' -> ['2+2']."""
    if re.fullmatch(r"\d+-\d+", hd):
        lo, hi = map(int, hd.split("-"))
        if hi - lo >= 2:            # a range, not 'n minus hp'
            return [str(v) for v in range(lo, hi + 1)]
    if re.fullmatch(r"\d+(/\d+)+", hd) and int(hd.split("/")[0]) >= 2:
        return hd.split("/")
    return [hd]


def check_tables(data, rep):
    with open(os.path.join(HERE, "tables.json"), encoding="utf-8") as fh:
        tables = json.load(fh)
    with open(os.path.join(HERE, "mapping.json"), encoding="utf-8") as fh:
        mapping = json.load(fh)["monsters"]
    summary = {r["qualified_name"]: r for r in tables["summary"]}
    giants = {r["type"]: r for r in tables["giants"]}
    horses = {r["type"]: r for r in tables["horses"]}
    rocs = {r["type"]: r for r in tables["rocs"]}
    dd_ages = ["Hatchling", "Young", "Adult", "Mature", "Old", "Ancient"]
    color_names = {"Black": "Black", "Blue": "Blue", "Golden": "Gold",
                   "Green": "Green", "Red": "Red", "White": "White"}

    # Build name -> (expected ac, expected hd list, expected align, overrides)
    expected = {}
    for e in mapping:
        src = e.get("source")
        if src == "dragons":
            color = e["color"]
            for idx, det in enumerate(tables["dragons"][color]):
                name = "%s %s Dragon" % (DRAGON_AGES[idx], color_names[color])
                expected[name] = (first_int(det["ac"]), [det["hd"]], align_char(det["align"]), {})
            continue
        if src == "giants":
            det, summ = giants[e["giant"]], summary["Giants, %s" % e["giant"]]
            expected[e["name"]] = (first_int(det["ac"]), [det["hd"]], align_char(det["align"]), {})
            continue
        if src == "horses":
            det = horses[e["horse"]]
            expected[e["name"]] = (first_int(det["ac"]), [det["hd"]], "N", {})
            continue
        if src == "rocs":
            det, summ = rocs[e["roc"]], summary["Rocs, %s" % e["roc"]]
            expected[e["name"]] = (first_int(det["ac"]), [det["hd"]], align_char(summ["align"]), {})
            continue
        summ = summary[e["dd"]]
        overrides = {k: e[k] for k in ("ac", "hd", "align") if k in e}
        exp = (first_int(summ["ac"]), hd_values(summ["hd"]), align_char(summ["align"]), overrides)
        if "expand" in e:
            # every row whose name ends with the template suffix
            suffix = re.sub(r"^\{HD\} ", "", e["expand"].get("name", "")) if e["expand"]["kind"] != "hydra" else "-Headed Hydra"
            for row in data:
                if row[0].endswith(suffix) and (e["expand"]["kind"] == "hydra" or row[0].split(" ", 1)[1] == suffix.split(" ", 1)[-1] or row[0].endswith(" " + suffix)):
                    expected[row[0]] = exp
        else:
            expected[e["name"]] = exp

    for fields in data:
        r = dict(zip(COLUMNS, fields))
        name = r["Monster"]
        if name not in expected:
            rep.error(name, "no tables.json source found via mapping.json")
            continue
        ac, hds, align, overrides = expected[name]
        if int(r["AC"]) != ac:
            if "ac" in overrides and int(r["AC"]) == overrides["ac"]:
                rep.info(name, "AC %s differs from table first value %d (override in mapping.json)" % (r["AC"], ac))
            else:
                rep.error(name, "AC %s but table says %d" % (r["AC"], ac))
        if r["HD"] not in hds:
            if "hd" in overrides and r["HD"] == overrides["hd"]:
                rep.info(name, "HD %s differs from table %s (override in mapping.json)" % (r["HD"], hds))
            else:
                rep.error(name, "HD %s but table allows %s" % (r["HD"], hds))
        if r["Align"] != align:
            if "align" in overrides and r["Align"] == overrides["align"]:
                rep.info(name, "Align %s differs from table %s (override in mapping.json)" % (r["Align"], align))
            else:
                rep.error(name, "Align %s but table says %s" % (r["Align"], align))


# ---------------------------------------------------------------------------


def main(argv):
    paths = argv[1:] or [DD_CSV]
    enum = load_enum()
    print("SpecialType constants found: %d" % len(enum))
    status = 0
    for path in paths:
        rep = Report()
        print("\n== %s" % os.path.relpath(path, ROOT))
        data = check_format(path, enum, rep)
        print("rows: %d" % len(data))
        if os.path.abspath(path) == os.path.abspath(DD_CSV):
            check_tables(data, rep)
        for label, items in (("ERROR", rep.errors), ("WARN", rep.warnings), ("INFO", rep.infos)):
            for it in items:
                print("%s %s" % (label, it))
        print("%d errors, %d warnings, %d infos" % (len(rep.errors), len(rep.warnings), len(rep.infos)))
        if rep.errors:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv))
