#!/usr/bin/env python3
"""Build the two Delving Deeper reference PDFs from the monster database.

    python3 tools/delving-deeper/pdf/build.py

Reads MonsterDatabase-DelvingDeeper.csv, MonsterLevelMatrix.csv and
EHDToTable.csv from the repository root, mapping.json (through
generate.py) from the parent directory for the Delving Deeper names, and
families.json and dragon-ehd.tsv (from dragon-ehd.sh) from this directory; writes build/statblocks.json and build/matrices.json, and
compiles statblocks.typ and matrices.typ with Typst into
DD-MonsterStatBlocks.pdf and DD-MonsterMatrices.pdf next to this script.

Needs Python 3 and Typst (https://typst.app, `brew install typst`).
"""

import csv
import json
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CSV = ROOT / "MonsterDatabase-DelvingDeeper.csv"
MATRIX_CSV = ROOT / "MonsterLevelMatrix.csv"
EHD_TABLE_CSV = ROOT / "EHDToTable.csv"
BUILD = HERE / "build"
REPO_URL = "https://github.com/karsalfrink/Arena"
PR_URL = "https://github.com/danielrcollins1/Arena/pull/6"

TYPES = OrderedDict([
    ("A", "Animals"),
    ("B", "Beasts"),
    ("F", "Faerie"),
    ("H", "Humanoids"),
    ("M", "Men"),
    ("S", "Slimes"),
    ("U", "Undead"),
    ("X", "Extraplanar"),
])

NUMBER_WORDS = {
    w: i for i, w in enumerate(
        "Zero One Two Three Four Five Six Seven Eight Nine Ten Eleven Twelve "
        "Thirteen Fourteen Fifteen Sixteen Seventeen Eighteen Nineteen Twenty"
        .split())
}
HD_FAMILY = re.compile(r"^(\w+) Hit Dice (.+)$")
HEADS_FAMILY = re.compile(r"^(\w+)-Headed (.+)$")

EN_DASH = "–"


# ---------------------------------------------------------------- input

def read_rows():
    with open(CSV, newline="") as f:
        return list(csv.DictReader(f))


def read_matrix():
    """MonsterLevelMatrix.csv: rows are dungeon-level thresholds, cells the
    minimum d6 roll for that monster level, '-' if impossible."""
    with open(MATRIX_CSV, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = [r for r in reader if r]
    n_levels = len(header) - 1
    thresholds = [int(r[0]) for r in rows]
    out = []
    for i, r in enumerate(rows):
        lo = thresholds[i]
        if i + 1 < len(rows):
            hi = thresholds[i + 1] - 1
            label = str(lo) if hi == lo else f"{lo}{EN_DASH}{hi}"
        else:
            label = f"{lo}+"
        mins = [None if c == "-" else int(c) for c in r[1:]]
        cells = []
        for j, m in enumerate(mins):
            if m is None:
                cells.append(EN_DASH)
                continue
            nxt = next((x for x in mins[j + 1:] if x is not None), 7)
            hi = nxt - 1
            cells.append(str(m) if hi == m else f"{m}{EN_DASH}{hi}")
        out.append({"dungeon": label, "cells": cells})
    return {"levels": n_levels, "rows": out}


def read_ehd_bands():
    """EHDToTable.csv: EHD threshold -> table level."""
    with open(EHD_TABLE_CSV, newline="") as f:
        reader = csv.reader(f)
        next(reader)
        bands = [(int(a), int(b)) for a, b in reader if a]
    labels = {}
    for i, (lo, t) in enumerate(bands):
        if i + 1 < len(bands):
            hi = bands[i + 1][0] - 1
            labels[t] = str(lo) if hi == lo else f"{lo}{EN_DASH}{hi}"
        else:
            labels[t] = f"{lo}+"
    return bands, labels


def band_of(ehd, bands):
    t = -1
    for lo, table in bands:
        if ehd >= lo:
            t = table
    return t


def git_version():
    """Short hash and date of the commit that last touched the CSV, so the
    PDFs carry a reproducible version stamp rather than a build time."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%h %cs", "--", CSV.name],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--", CSV.name],
            cwd=ROOT, capture_output=True, text=True).stdout.strip()
        commit, iso = out
        d = date.fromisoformat(iso)
        return {"commit": commit + ("+" if dirty else ""),
                "date": f"{d.day} {d.strftime('%B %Y')}"}
    except Exception:  # not a git checkout
        return {"commit": "unknown", "date": "unknown"}


# ------------------------------------------------------- DD names

DD_AGES = ["Hatchling", "Young", "Adult", "Mature", "Old", "Ancient"]

# Arena rows that share one DD entry and need telling apart.
DD_LABEL_OVERRIDE = {
    "Giant Constrictor Snake": "Snakes, giant (constrictor)",
    "Giant Viper": "Snakes, giant (viper)",
    "Animated Tree": "Treants (animated tree)",
}


def dd_names():
    """Arena monster name -> {'label': DD Table 3.1 name, 'member': age for
    dragons, 'order': position in mapping.json}. Reuses generate.py from the
    parent directory, which expands mapping.json into the Arena rows."""
    import os
    cwd = os.getcwd()
    os.chdir(HERE.parent)
    sys.path.insert(0, str(HERE.parent))
    sys.dont_write_bytecode = True  # keep __pycache__ out of the parent
    try:
        import generate
    finally:
        os.chdir(cwd)
    names = {}
    for order, entry in enumerate(generate.MAPPING):
        label = generate.entry_label(entry)
        for i, row in enumerate(generate.rows_for(entry)):
            arena = row["Monster"]
            names[arena] = {
                "label": DD_LABEL_OVERRIDE.get(arena, label),
                "member": DD_AGES[i] if entry.get("source") == "dragons" else None,
                "order": order,
            }
    return names


def dd_sort_key(label, order):
    """DD Table 3.1 order: alphabetical by the part before the comma, then
    the order of mapping.json (which follows the DD tables) within it."""
    return (label.split(",")[0].lower(), order)


# ------------------------------------------------- HD-range families

def family_key(name):
    """('Giant Beetle', 2, 'hd') for 'Two Hit Dice Giant Beetle',
    ('Hydra', 5, 'heads') for 'Five-Headed Hydra', else None."""
    m = HD_FAMILY.match(name)
    if m and m.group(1) in NUMBER_WORDS:
        return m.group(2), NUMBER_WORDS[m.group(1)], "hd"
    m = HEADS_FAMILY.match(name)
    if m and m.group(1) in NUMBER_WORDS:
        return m.group(2), NUMBER_WORDS[m.group(1)], "heads"
    return None


def fmt_range(values, unit=""):
    values = sorted(values)
    if len(values) == 1:
        return f"{values[0]}{unit}"
    contiguous = values == list(range(values[0], values[-1] + 1))
    if contiguous:
        return f"{values[0]}{EN_DASH}{values[-1]}{unit}"
    return ", ".join(str(v) for v in values) + unit


def hd_display(hd):
    return hd  # '2-1' is HD minus one, so the hyphen stays


# ------------------------------------------------------ stat blocks

def plain_entry(r, names):
    n = names[r["Monster"]]
    return {
        "name": n["label"], "arena": r["Monster"], "order": n["order"],
        "member": n["member"], "number": r["Number"], "ac": r["AC"], "mv": r["MV"],
        "hd": hd_display(r["HD"]), "ehd": r["EHD"], "atk": r["Atk"],
        "dam": r["Dam"], "align": r["Align"],
        "special": "" if r["Special"] == "-" else r["Special"],
        "note": "", "dragon": r["Monster"].endswith("Dragon"),
    }


def statblocks(rows, version, names):
    """One entry per DD monster, in DD Table 3.1 order within each type;
    rows of an HD-range family whose other columns agree are merged into one
    entry, and dragons are grouped by colour with one sub-row per age."""
    sections = OrderedDict((t, []) for t in TYPES)
    groups = OrderedDict()
    dragon_ehds = read_dragon_ehds() or {}
    for r in rows:
        key = family_key(r["Monster"])
        entry = plain_entry(r, names)
        if entry["dragon"] and r["Monster"] in dragon_ehds:
            entry["ehd"] = str(dragon_ehds[r["Monster"]])  # HD-only, see dragon-ehd.sh
        if key is None:
            sections[r["Type"]].append(entry)
            continue
        base, n, kind = key
        g = groups.get((r["Type"], base))
        if g is None:
            g = groups[(r["Type"], base)] = {"kind": kind, "members": []}
            sections[r["Type"]].append(g)  # placeholder, replaced below
        g["members"].append((n, r))

    for (t, base), g in groups.items():
        members = sorted(g["members"])
        first = members[0][1]
        same = lambda col: all(r[col] == first[col] for _, r in members)
        kind = g["kind"]
        mergeable = all(same(c) for c in ("Number", "AC", "MV", "Dam", "Align", "Special")) \
            and (same("Atk") or (kind == "heads" and all(r["Atk"] == str(n) for n, r in members)))
        idx = sections[t].index(g)
        if not mergeable:
            sections[t][idx:idx + 1] = [plain_entry(r, names) for _, r in members]
            continue
        ns = [n for n, _ in members]
        ehds = [int(r["EHD"]) for _, r in members]
        unit = " heads" if kind == "heads" else ""
        n = names[first["Monster"]]
        entry = {
            "name": n["label"] if kind == "hd" else f"{n['label']} ({fmt_range(ns, unit)})",
            "arena": base, "order": n["order"], "member": None,
            "number": first["Number"], "ac": first["AC"], "mv": first["MV"],
            "hd": fmt_range(ns),
            "ehd": f"{min(ehds)}{EN_DASH}{max(ehds)}" if min(ehds) != max(ehds) else str(ehds[0]),
            "atk": fmt_range(ns) if kind == "heads" else first["Atk"],
            "dam": first["Dam"], "align": first["Align"],
            "special": "" if first["Special"] == "-" else first["Special"],
            "note": ("EHD by heads: " if kind == "heads" else "EHD by HD: ")
                    + ", ".join(str(e) for e in ehds),
            "dragon": False,
        }
        sections[t][idx] = entry

    # Group dragons by colour: one heading entry with a sub-row per age.
    for t, entries in sections.items():
        grouped = OrderedDict()
        out = []
        for e in entries:
            if e["member"] is None:
                out.append(e)
                continue
            g = grouped.get(e["name"])
            if g is None:
                g = grouped[e["name"]] = {"group": e["name"], "order": e["order"], "rows": []}
                out.append(g)
            e["name"] = e["member"]
            g["rows"].append(e)
        out.sort(key=lambda e: dd_sort_key(e.get("group") or e["name"], e["order"]))
        sections[t] = out

    return {
        "version": version,
        "csv": CSV.name, "repo": REPO_URL, "pr": PR_URL,
        "rows": len(rows),
        "sections": [{"letter": t, "title": TYPES[t], "entries": e}
                     for t, e in sections.items() if e],
    }


# --------------------------------------------------------- matrices

DRAGON_TSV = HERE / "dragon-ehd.tsv"
ARENA_AGES = ["Very Young", "Young", "Sub-Adult", "Adult", "Old", "Very Old"]
DRAGON_COLOURS = ["White", "Black", "Green", "Blue", "Red", "Gold"]
DD_COLOUR = {"Gold": "Golden"}


def read_dragon_ehds():
    """dragon-ehd.tsv (from dragon-ehd.sh): Arena name -> HD-only EHD."""
    if not DRAGON_TSV.exists():
        return None
    out = {}
    with open(DRAGON_TSV, newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)
        for name, ehd in reader:
            out[name] = int(ehd)
    return out


def dragon_placement(bands):
    """One table entry per run of DD ages that share a band, placed by the
    median HD-only EHD over the six colours; plus the age x colour grid for
    the notes. Returns (placements, grid) or (None, None) without the tsv."""
    ehds = read_dragon_ehds()
    if ehds is None:
        return None, None
    grid = []
    by_age_level = []
    for i, age in enumerate(DD_AGES):
        vals = [ehds[f"{ARENA_AGES[i]} {c} Dragon"] for c in DRAGON_COLOURS]
        srt = sorted(vals)
        median = (srt[len(srt) // 2 - 1] + srt[len(srt) // 2]) // 2
        level = band_of(median, bands)
        grid.append({"age": age, "ehds": [str(v) for v in vals], "level": level})
        by_age_level.append((age.lower(), level, min(vals), max(vals)))
    placements = []
    for age, level, lo, hi in by_age_level:
        if placements and placements[-1]["level"] == level:
            placements[-1]["ages"].append(age)
            placements[-1]["lo"] = min(placements[-1]["lo"], lo)
            placements[-1]["hi"] = max(placements[-1]["hi"], hi)
        else:
            placements.append({"ages": [age], "level": level, "lo": lo, "hi": hi})
    for pl in placements:
        ages = pl["ages"]
        pl["name"] = "Dragons, " + (ages[0] if len(ages) == 1
                                    else ", ".join(ages[:-1]) + " or " + ages[-1])
    return placements, grid


def matrices(rows, version, names):
    matrix = read_matrix()
    bands, band_labels = read_ehd_bands()
    with open(HERE / "families.json") as f:
        rules = [(re.compile(r["pattern"]), r) for r in json.load(f)["rules"]]
    placements, dragon_grid = dragon_placement(bands)

    tables = OrderedDict((t, OrderedDict()) for t in range(1, matrix["levels"] + 1))
    excluded = {"ehd0": [], "env": 0}
    for r in rows:
        if r["Env"] != "D":
            excluded["env"] += 1
            continue
        name = r["Monster"]
        if names[name]["member"] is not None:  # a dragon: placed by age below
            continue
        ehd = int(r["EHD"])
        level = band_of(ehd, bands)
        if level < 1:
            if ehd == 0:
                excluded["ehd0"].append(names[name]["label"])
            continue
        dd = names[name]["label"]
        family, member = None, None
        for rx, rule in rules:
            m = rx.match(dd)
            if m:
                family, member = rule["family"], m.expand(rule.get("member", ""))
                break
        if family is None:
            key = family_key(name)
            if key:
                base, n, kind = key
                family, member = dd, (n, kind)
        label = family or dd
        tables[level].setdefault(label, []).append((member, ehd, name))

    if placements is None:  # no dragon-ehd.tsv: fall back to the OED entry
        tables[matrix["levels"]]["Dragons (any)"] = [(None, 11, "Dragon")]
        print("warning: dragon-ehd.tsv missing, run dragon-ehd.sh", file=sys.stderr)
    else:
        for pl in placements:
            tables[pl["level"]][pl["name"]] = [(None, pl["lo"], "Dragon"), (None, pl["hi"], "Dragon")]

    out_tables = []
    for level, entries in tables.items():
        items = []
        for label, members in entries.items():
            ehds = sorted(set(e for _, e, _ in members))
            ms = [m for m, _, _ in members if m]
            if ms and isinstance(ms[0], tuple):
                kind = ms[0][1]
                unit = " heads" if kind == "heads" else " HD"
                text = f"{label} ({fmt_range([m[0] for m in ms], unit)})"
            elif ms:
                seen = list(OrderedDict.fromkeys(ms))
                text = f"{label} ({'/'.join(seen)})"
            else:
                text = label
            items.append({"name": text,
                          "ehd": f"{ehds[0]}{EN_DASH}{ehds[-1]}" if len(ehds) > 1 else str(ehds[0]),
                          "n": len(members)})
        items.sort(key=lambda i: i["name"].lower())
        out_tables.append({"level": level, "ehd": band_labels[level],
                           "die": len(items), "entries": items})

    return {
        "version": version, "csv": CSV.name, "repo": REPO_URL, "pr": PR_URL,
        "matrix": matrix, "tables": out_tables, "excluded": excluded,
        "dragons": {"colours": [DD_COLOUR.get(c, c) for c in DRAGON_COLOURS],
                    "grid": dragon_grid, "tsv": DRAGON_TSV.name} if dragon_grid else None,
    }


# ------------------------------------------------------------- main

def main():
    rows = read_rows()
    version = git_version()
    names = dd_names()
    missing = [r["Monster"] for r in rows if r["Monster"] not in names]
    if missing:
        sys.exit(f"no DD name for: {', '.join(missing)}")
    BUILD.mkdir(exist_ok=True)
    (BUILD / "statblocks.json").write_text(
        json.dumps(statblocks(rows, version, names), indent=1, ensure_ascii=False))
    (BUILD / "matrices.json").write_text(
        json.dumps(matrices(rows, version, names), indent=1, ensure_ascii=False))
    for stem, pdf in (("statblocks", "DD-MonsterStatBlocks.pdf"),
                      ("matrices", "DD-MonsterMatrices.pdf")):
        subprocess.run(["typst", "compile", "--root", str(HERE),
                        str(HERE / f"{stem}.typ"), str(HERE / pdf)], check=True)
        print("wrote", pdf)


if __name__ == "__main__":
    sys.exit(main())
