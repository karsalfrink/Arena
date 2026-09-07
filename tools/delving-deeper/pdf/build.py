#!/usr/bin/env python3
"""Build the two Delving Deeper reference PDFs from the monster database.

    python3 tools/delving-deeper/pdf/build.py

Reads MonsterDatabase-DelvingDeeper.csv, MonsterLevelMatrix.csv and
EHDToTable.csv from the repository root and families.json from this
directory, writes build/statblocks.json and build/matrices.json, and
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

def plain_entry(r):
    return {
        "name": r["Monster"], "number": r["Number"], "ac": r["AC"], "mv": r["MV"],
        "hd": hd_display(r["HD"]), "ehd": r["EHD"], "atk": r["Atk"],
        "dam": r["Dam"], "align": r["Align"],
        "special": "" if r["Special"] == "-" else r["Special"],
        "note": "", "dragon": r["Monster"].endswith("Dragon"),
    }


def statblocks(rows, version):
    """One entry per monster, alphabetical within each type; rows of an
    HD-range family whose other columns agree are merged into one entry."""
    sections = OrderedDict((t, []) for t in TYPES)
    groups = OrderedDict()
    for r in rows:
        key = family_key(r["Monster"])
        entry = plain_entry(r)
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
            sections[t][idx:idx + 1] = [plain_entry(r) for _, r in members]
            continue
        ns = [n for n, _ in members]
        ehds = [int(r["EHD"]) for _, r in members]
        unit = " heads" if kind == "heads" else ""
        entry = {
            "name": base if kind == "hd" else f"{base} ({fmt_range(ns, unit)})",
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

    for entries in sections.values():  # alphabetical within a type
        entries.sort(key=lambda e: e["name"].lower())

    return {
        "version": version,
        "csv": CSV.name, "repo": REPO_URL, "pr": PR_URL,
        "rows": len(rows),
        "sections": [{"letter": t, "title": TYPES[t], "entries": e}
                     for t, e in sections.items() if e],
    }


# --------------------------------------------------------- matrices

def matrices(rows, version):
    matrix = read_matrix()
    bands, band_labels = read_ehd_bands()
    with open(HERE / "families.json") as f:
        rules = [(re.compile(r["pattern"]), r) for r in json.load(f)["rules"]]

    tables = OrderedDict((t, OrderedDict()) for t in range(1, matrix["levels"] + 1))
    excluded = {"ehd0": [], "env": 0}
    for r in rows:
        if r["Env"] != "D":
            excluded["env"] += 1
            continue
        ehd = int(r["EHD"])
        name = r["Monster"]
        level = band_of(ehd, bands)
        family, member = None, None
        for rx, rule in rules:
            m = rx.match(name)
            if m:
                if rule.get("drop"):
                    level = -1
                family = rule["family"]
                member = m.expand(rule.get("member", ""))
                member = member[:1].upper() + member[1:]
                level = rule.get("level", level)
                break
        if family is None:
            key = family_key(name)
            if key:
                base, n, kind = key
                family, member = base, (n, kind)
        if level < 1:
            if ehd == 0:
                excluded["ehd0"].append(name)
            continue
        label = family or name
        tables[level].setdefault(label, []).append((member, ehd, name))

    out_tables = []
    for level, entries in tables.items():
        items = []
        for label, members in entries.items():
            ehds = sorted(set(e for _, e, _ in members))
            ehds = [ehds[0], ehds[-1]] if len(ehds) > 1 else ehds
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
            items.append({"name": text, "ehd": EN_DASH.join(str(e) for e in ehds), "n": len(members)})
        items.sort(key=lambda i: i["name"])
        out_tables.append({"level": level, "ehd": band_labels[level],
                           "die": len(items), "entries": items})

    return {
        "version": version, "csv": CSV.name, "repo": REPO_URL, "pr": PR_URL,
        "matrix": matrix, "tables": out_tables, "excluded": excluded,
    }


# ------------------------------------------------------------- main

def main():
    rows = read_rows()
    version = git_version()
    BUILD.mkdir(exist_ok=True)
    (BUILD / "statblocks.json").write_text(
        json.dumps(statblocks(rows, version), indent=1, ensure_ascii=False))
    (BUILD / "matrices.json").write_text(
        json.dumps(matrices(rows, version), indent=1, ensure_ascii=False))
    for stem, pdf in (("statblocks", "DD-MonsterStatBlocks.pdf"),
                      ("matrices", "DD-MonsterMatrices.pdf")):
        subprocess.run(["typst", "compile", "--root", str(HERE),
                        str(HERE / f"{stem}.typ"), str(HERE / pdf)], check=True)
        print("wrote", pdf)


if __name__ == "__main__":
    sys.exit(main())
