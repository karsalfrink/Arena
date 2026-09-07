#!/usr/bin/env python3
"""Generate the Arena monster database for Delving Deeper.

Inputs:  tables.json, descriptions.json (from parse.py) and mapping.json
Outputs: ../../MonsterDatabase-DelvingDeeper.csv   (default)
         mapping.md   (--mapping)   human-readable mapping proposal
         NOTES.md     (--notes)     everything that could not be mapped

Usage:   python3 generate.py [--csv] [--mapping] [--notes] [--all]
"""
import csv
import json
import re
import sys

CSV_OUT = "../../MonsterDatabase-DelvingDeeper.csv"
COLUMNS = ["Monster", "Number", "AC", "MV", "HD", "Lair%", "Treas", "Atk",
           "Dam", "Align", "Type", "EHD", "HDD", "Env", "Source", "Special"]

with open("tables.json", encoding="utf-8") as fh:
    TABLES = json.load(fh)
with open("mapping.json", encoding="utf-8") as fh:
    MAPPING = json.load(fh)["monsters"]

# Computed EHD values (from run-metrics.sh), if present: name -> EHD.
EHD_FILE = "ehd.tsv"
EHD = {}
try:
    with open(EHD_FILE, encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            name, ehd, _ = line.rstrip("\n").split("\t")
            EHD[name] = ehd
except FileNotFoundError:
    pass

SUMMARY = {r["qualified_name"]: r for r in TABLES["summary"]}
GIANTS = {r["type"]: r for r in TABLES["giants"]}
HORSES = {r["type"]: r for r in TABLES["horses"]}
ROCS = {r["type"]: r for r in TABLES["rocs"]}

NUMBER_WORDS = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six",
                7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven",
                12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen",
                16: "Sixteen"}

# Dragon age mapping: DD -> Arena (parseDragonAge matches on name prefix).
DD_AGES = ["Hatchling", "Young", "Adult", "Mature", "Old", "Ancient"]
ARENA_AGES = ["Very Young", "Young", "Sub-Adult", "Adult", "Old", "Very Old"]
DRAGON_NAME = {"Black": "Black", "Blue": "Blue", "Golden": "Gold",
               "Green": "Green", "Red": "Red", "White": "White"}
DRAGON_BREATH = {"Black": "AcidBreath", "Blue": "VoltBreath",
                 "Golden": "FireBreath", "Green": "PoisonBreath",
                 "Red": "FireBreath", "White": "ColdBreath"}
DRAGON_EXTRA = {"Black": ["AcidImmunity"], "Blue": ["VoltImmunity"],
                "Golden": ["SaveBonus (4)", "Spells"], "Green": [],
                "Red": ["FireImmunity"], "White": ["ColdImmunity"]}
# Dragons group introduction: sense hidden/invisible within 6"; from
# adulthood (DD Adult = Arena age 3) never check morale; old and ancient
# (Arena ages 5-6) make normal-types check morale to approach or stand.
DRAGON_DETECTION = "Detection (6)"
DRAGON_FEARLESS_FROM_AGE = 3
DRAGON_FEAR_FROM_AGE = 5

# ---------------------------------------------------------------------------
# Conversion helpers (the rules documented in mapping.md)
# ---------------------------------------------------------------------------

STANDARD_DICE = (2, 3, 4, 5, 6, 8, 10, 12, 20, 100)


def dice_from_range(s):
    """'2-8' -> '2d4', '3-8' -> '1d6+2', '6-21' -> '3d6+3', '7' -> '7'."""
    s = s.strip().rstrip("+").replace(" ", "")
    if s in ("n/a", "-", ""):
        return "1"
    if re.fullmatch(r"\d+", s):
        return s
    m = re.fullmatch(r"(\d+)-(\d+)", s)
    if not m:
        raise ValueError("Cannot convert range: %r" % s)
    lo, hi = int(m.group(1)), int(m.group(2))
    span = hi - lo
    cands = []
    for n in range(1, span + 1):
        if span % n:
            continue
        sides = span // n + 1
        if sides not in STANDARD_DICE:
            continue
        cands.append((n, sides, lo - n))
    if not cands:
        raise ValueError("No dice expression for range %r" % s)

    def key(c):
        n, sides, add = c
        return (add != 0, sides != 6 and add != 0, abs(add), n)
    n, sides, add = min(cands, key=key)
    out = "%dd%d" % (n, sides)
    if add:
        out += "%+d" % add
    return out


def first_int(s):
    """'3/7' -> 3, '7*' -> 7, '5-2' -> 5, 'n/a' -> 0."""
    m = re.match(r"\s*(-?\d+)", s)
    return int(m.group(1)) if m else 0


def split_move(s):
    """'9/15' -> ('9', '15'); '-/36' -> ('-', '36'); '12' -> ('12', None)."""
    parts = s.replace(" ", "").split("/")
    return (parts[0], parts[1] if len(parts) > 1 else None)


def hd_decimal(hd):
    """'3+1' -> '3.3', '1/2' -> '0.5', '1-1' -> '0.7', '8' -> '8'."""
    m = re.fullmatch(r"(\d+)(?:/(\d+))?([+-]\d+)?", hd)
    if not m:
        raise ValueError("Bad HD: %r" % hd)
    val = int(m.group(1))
    if m.group(2):
        val = val / int(m.group(2))
    if m.group(3):
        val += int(m.group(3)) * 0.3
    val = round(val, 1)
    return str(int(val)) if val == int(val) else "%.1f" % val


def lair_pct(s):
    return "-" if s in ("n/a", "") else str(first_int(s))


def treasure_char(s):
    s = s.strip()
    if s in ("n/a", "", "*", "-"):
        return "-"
    return s[0]


def align_char(s):
    s = s.strip()
    if s == "Any":
        return "N"
    return s[0]


def format_specials(specials):
    return ", ".join(specials) if specials else "-"


# ---------------------------------------------------------------------------
# Row builders
# ---------------------------------------------------------------------------


def base_row(name, number, ac, mv, hd, lair, treas, atk, dam, align,
             typ, env, specials):
    return {
        "Monster": name, "Number": number, "AC": str(ac), "MV": str(mv),
        "HD": hd, "Lair%": lair, "Treas": treas, "Atk": str(atk), "Dam": dam,
        "Align": align, "Type": typ, "EHD": EHD.get(name, "?"), "HDD": hd_decimal(hd),
        "Env": env, "Source": "DD", "Special": format_specials(specials),
    }


def movement(entry, move_str):
    """Return (mv, extra_specials) from a DD move string and the entry's
    'mv2' hint (Flight / Swimming / WebMove)."""
    primary, secondary = split_move(move_str)
    mv2 = entry.get("mv2")
    extra = []
    if "mv" in entry:
        mv = entry["mv"]
    elif primary == "-":
        # No ground move: fliers keep their fly speed as MV (master Air
        # Elemental idiom); swimmers get MV 0 (master aquatic idiom).
        mv = int(secondary) if mv2 == "Flight" else 0
    elif primary in ("n/a", ""):
        mv = 0
    else:
        mv = int(primary)
    if mv2 and secondary:
        extra.append("%s (%s)" % (mv2, secondary))
    elif mv2 and not secondary:
        raise ValueError("%s: mv2 given but no secondary move in %r"
                         % (entry.get("name"), move_str))
    return mv, extra


def rows_from_summary(entry):
    src = SUMMARY[entry["dd"]]
    mv, extra = movement(entry, src["move"])
    specials = extra + list(entry.get("specials", []))
    number = entry.get("number", dice_from_range(src["number_appearing"]))
    ac = entry.get("ac", first_int(src["ac"]))
    lair = entry.get("lair", lair_pct(src["lair_pct"]))
    treas = entry.get("treas", treasure_char(src["treasure"]))
    align = entry.get("align", align_char(src["align"]))
    typ, env, atk, dam = entry["type"], entry["env"], entry.get("atk", 1), entry.get("dam", "1d6")

    exp = entry.get("expand")
    if not exp:
        hd = entry.get("hd", src["hd"])
        return [base_row(entry["name"], number, ac, mv, hd, lair, treas,
                         atk, dam, align, typ, env, specials)]
    rows = []
    if exp["kind"] in ("hd_range", "hd_list"):
        values = (range(exp["from"], exp["to"] + 1) if exp["kind"] == "hd_range"
                  else exp["values"])
        for v in values:
            name = exp["name"].replace("{HD}", NUMBER_WORDS[v])
            rows.append(base_row(name, number, ac, mv, str(v), lair, treas,
                                 atk, dam, align, typ, env, specials))
    elif exp["kind"] == "hydra":
        for v in range(exp["from"], exp["to"] + 1):
            name = "%s-Headed Hydra" % NUMBER_WORDS[v]
            rows.append(base_row(name, number, ac, mv, str(v), lair, treas,
                                 v, dam, align, typ, env, specials))
    else:
        raise ValueError("Unknown expand kind %r" % exp["kind"])
    return rows


def rows_from_dragons(entry):
    color = entry["color"]
    summ = SUMMARY["Dragons, %s" % color]
    rows = []
    for idx, det in enumerate(TABLES["dragons"][color]):
        assert det["age"] == DD_AGES[idx], (color, det["age"])
        arena_age = idx + 1
        name = "%s %s Dragon" % (ARENA_AGES[idx], DRAGON_NAME[color])
        walk, fly = split_move(det["move"])
        specials = ["Flight (%s)" % fly, DRAGON_DETECTION]
        if arena_age >= DRAGON_FEARLESS_FROM_AGE:
            specials.append("Fearlessness")
        if arena_age >= DRAGON_FEAR_FROM_AGE:
            specials.append("Fear (2)")
        specials.append(DRAGON_BREATH[color])
        specials.extend(DRAGON_EXTRA[color])
        treas = "-" if idx == 0 else treasure_char(summ["treasure"])
        rows.append(base_row(
            name, dice_from_range(summ["number_appearing"]), first_int(det["ac"]),
            int(walk), det["hd"], lair_pct(summ["lair_pct"]), treas, 1,
            dice_from_range(det["melee_dam"]), align_char(det["align"]),
            "B", "D", specials))
    return rows


def rows_from_giants(entry):
    det = GIANTS[entry["giant"]]
    summ = SUMMARY["Giants, %s" % entry["giant"]]
    mv, extra = movement(entry, det["move"])
    return [base_row(
        entry["name"], dice_from_range(summ["number_appearing"]),
        first_int(det["ac"]), mv, det["hd"], lair_pct(summ["lair_pct"]),
        treasure_char(summ["treasure"]), entry.get("atk", 1),
        dice_from_range(det["melee_dam"]), align_char(det["align"]),
        entry["type"], entry["env"], extra + entry.get("specials", []))]


def rows_from_horses(entry):
    det = HORSES[entry["horse"]]
    mv, extra = movement(entry, det["move"])
    return [base_row(
        entry["name"], "1", first_int(det["ac"]), mv, det["hd"], "-", "-",
        entry.get("atk", 1), entry.get("dam", "1d6"), "N",
        entry["type"], entry["env"], extra + entry.get("specials", []))]


def rows_from_rocs(entry):
    det = ROCS[entry["roc"]]
    summ = SUMMARY["Rocs, %s" % entry["roc"]]
    entry = dict(entry, mv2="Flight")
    mv, extra = movement(entry, det["move"])
    return [base_row(
        entry["name"], dice_from_range(summ["number_appearing"]),
        first_int(det["ac"]), mv, det["hd"], lair_pct(summ["lair_pct"]),
        treasure_char(summ["treasure"]), entry.get("atk", 1),
        dice_from_range(det["melee_dam"]), align_char(summ["align"]),
        entry["type"], entry["env"], extra + entry.get("specials", []))]


def rows_for(entry):
    src = entry.get("source")
    if src is None:
        return rows_from_summary(entry)
    return {"dragons": rows_from_dragons, "giants": rows_from_giants,
            "horses": rows_from_horses, "rocs": rows_from_rocs}[src](entry)


def build():
    """Return list of (entry, [rows])."""
    return [(e, rows_for(e)) for e in MAPPING]


def entry_label(entry):
    if "dd" in entry:
        return entry["dd"]
    return {"dragons": "Dragons, %s" % entry.get("color"),
            "giants": "Giants, %s" % entry.get("giant"),
            "horses": "Horses, %s" % entry.get("horse"),
            "rocs": "Rocs, %s" % entry.get("roc")}[entry["source"]]


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------


TYPE_ORDER = "ABFHMSUX"   # section order of MonsterDatabase.csv


def sort_key(r):
    """Master-file order: by Type section, then EHD, then hit dice."""
    ehd = int(r["EHD"]) if r["EHD"] != "?" else 10 ** 6
    return (TYPE_ORDER.index(r["Type"]), ehd, float(r["HDD"]), r["Monster"])


def write_csv(groups):
    rows = sorted((r for _, rs in groups for r in rs), key=sort_key)
    with open(CSV_OUT, "w", encoding="utf-8", newline="") as fh:
        # CRLF to match MonsterDatabase.csv
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\r\n",
                           quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("wrote %s (%d rows)" % (CSV_OUT, sum(len(r) for _, r in groups)))


MAPPING_PREAMBLE = """# Delving Deeper -> Arena monster mapping

This is the proposal for turning every monster in the Delving Deeper
reference rules (Section III, *Monsters*) into rows of
`MonsterDatabase-DelvingDeeper.csv`. It is rendered by `generate.py` from
`mapping.json` + `tables.json`, so what you see here is exactly what the CSV
will contain. Edit `mapping.json` and re-run `python3 generate.py --all`.

## Derivation rules

Columns: `Monster,Number,AC,MV,HD,Lair%,Treas,Atk,Dam,Align,Type,EHD,HDD,Env,Source,Special`.

* **Stats source.** Table 3.1 (summary) unless a detail table exists: dragons
  (Tables 3.4-3.9), giants (3.10), horses (3.11), rocs (3.12). Where the two
  disagree the detail table wins (e.g. Destrier MV 15, Fire Elemental HD).
* **Number.** DD "a-b" ranges become Arena dice: prefer an expression with no
  modifier (2-8 -> 2d4, 3-12 -> 3d4, 10-80 -> 10d8), else the d6 form with the
  smallest modifier (3-8 -> 1d6+2, 4-14 -> 2d6+2, 6-21 -> 3d6+3, 1-11 -> 2d6-1),
  else the fewest dice (2-9 -> 1d8+1, 2-5 -> 1d4+1). "n/a" (horses) -> 1.
  Number appearing (wandering) is used, not number in lair.
* **AC.** Split ACs are hit-location or facing values; the one a melee
  attacker faces is used, following the master file (Salamander 5 not 3,
  Giant Squid 7 not 3, Giant Centipede 3, Triceratops 2, Stegosaurus 5).
  "7*" (barded) -> 7. The unused value is recorded in NOTES.md.
* **MV.** First value of a split move; the second value goes into Special as
  `Flight (n)` / `Swimming (n)` / `WebMove (n)` following MonsterDatabase.csv.
  "-/n" fliers keep n as MV (master Air Elemental idiom); "-/n" swimmers get
  MV 0 (master aquatic idiom). Burrowing/climbing/wall-crawling secondaries
  have no master idiom and are listed in NOTES.md instead.
* **HD.** As written (`1/2`, `3+1`, `1-1` all parse). A *range* of HD
  (giant beetles 2-7, pterodactyls 2-7, giant fish 4-9, hydras 5-12,
  elementals 8/12/16) becomes one row per value, named
  "Two Hit Dice Giant Beetle", "Five-Headed Hydra",
  "Eight Hit Dice Air Elemental", etc.
* **Lair%.** "n/a" -> `-`. **Treas.** First character; `*` (coins carried) and
  "n/a" -> `-`; A1/A2/A3 -> A; E* -> E. **Align.** First listed ("C, N" -> C,
  "L, N" -> L, "Any" -> N).
* **Atk / Dam.** From the *Explanation of Monsters* prose; single attack roll
  and 1d6 when unstated (DD Combat, *Damage*). Prose ranges convert like
  Number. Multiple attack rolls (centaur 2, chimera 3, gothrog 2, hydra
  heads, octopus/squid/kraken "1-6 rolls" -> 4) become Atk.
  The "exceeds the number required by 4 or more, or a 20" bigger-damage
  pattern is *not* modelled; base damage is used and every case is listed
  in NOTES.md.
* **Type.** Same letters as MonsterDatabase.csv: A animal (normal, giant,
  prehistoric, aquatic), B beast/monster (fantastic creatures, lycanthropes,
  golems, dragons), F faerie/sylvan and noble creatures (dwarf, elf, pixie,
  pegasus, roc, treant), H humanoid (kobold to giant), M men,
  S slime/mold/ooze (auto-adds Slime), U undead (auto-adds Undead),
  X extraplanar (elementals, djinni, efreeti, invisible stalker).
* **EHD** computed by Arena's MonsterMetrics (`run-metrics.sh` writes
  `ehd.tsv`, which generate.py copies into the column; `?` if absent). **HDD** HD as a decimal, +0.3 per bonus
  hit point (`3+1` -> 3.3, `1-1` -> 0.7, `1/2` -> 0.5), as in the master file.
  **Env** D dungeon, W wilderness, U underwater, X extraplanar (as master).
  **Source** `DD`.
* **Special.** Exact `SpecialType` enum names, `Name (n)` for parameters,
  plus the three master-file movement words (`Flight`, `Swimming`,
  `WebMove`) which Arena silently ignores. Parameter meanings used:
  `Poison (n)` / `Charm (n)` = target's save modifier; `Fear (n)` = enemies
  of HD <= n must save or flee; `MagicToHit (n)` = weapon plus needed;
  `ChopResistance (n)` = half damage from weapons below magic level n
  (0 = all); `Regeneration (n)` = hp per round; `BloodDrain (n)` = 1d(n)
  per round while attached; `EnergyDrain (n)` = levels per hit;
  `Whirlwind (n)` = width; `FireBreath (n)` = n dice / cone length;
  `SaveBonus (n)`; `HitBonus (n)`; `Spells (n)` = nth-level wizard
  (bare `Spells` for the Gold Dragon and Titan, which Monster.java
  special-cases by name); `Detection (n)` = sees invisible.
  Names Arena only implements as *conditions* (Sleep, Webs, Death, Hold,
  Disintegration) are listed where DD clearly describes the ability, but are
  inert; see NOTES.md.
* **Row order.** As the master file: by Type section (A, B, F, H, M, S,
  U, X), then EHD, then hit dice. mapping.md keeps DD's table order.
* **Names.** Natural singular, Arena style. DD spellings kept where DD's
  monster is its own thing (Manticora, Gothrog, Thull, Wight Ape,
  Sabre-Toothed Tiger); "Golden Dragon" becomes "Gold Dragon" so
  Monster.java's Gold Dragon spell handling applies.
* **Dragons.** DD ages Hatchling / Young / Adult / Mature / Old / Ancient map
  in order onto Arena's Very Young / Young / Sub-Adult / Adult / Old /
  Very Old. Each age is a row with that age's AC, MV, HD and melee damage.
  Specials from the Dragons group introduction: `Flight (n)`,
  `Detection (6)` ("sense hidden and invisible creatures within 6\""),
  `Fearlessness` from DD Adult up ("from adulthood they ... need never
  check morale"), `Fear (2)` from DD Old up ("old and ancient dragons
  require normal-types to throw a positive morale check"), breath type and
  immunity per colour; Gold adds `SaveBonus (4)` and `Spells`. Hatchlings
  have no treasure (*Dragon Treasure*).

## Master-file vocabulary deliberately not used

MonsterDatabase.csv uses many Special names that are not in `SpecialType`
(Stealth, Disease, Lycanthropy, Spawn, Camouflage, Bravery, Cowardice,
LightSensitivity, Splitting, GasForm, Creation, Tracking, Leaping, Jet,
InkCloud, WeatherControl, DimensionDoor, Grappling, LandWeakness, Undying).
Arena drops them silently. Apart from the three movement words above, this
file does not use them; the corresponding DD abilities are recorded per
monster in NOTES.md so they can be added if Dan implements them.

## Mapping table

Grouped entries (dragons, HD ranges, hydras, elementals) are shown once with
the row count; the Special column shows the pattern shared by every row.
"""


def md_escape(s):
    return s.replace("|", "\\|")


def write_mapping(groups):
    lines = [MAPPING_PREAMBLE]
    lines.append("| DD entry | Arena row(s) | Num | AC | MV | HD | Lair | Tr | Atk | Dam | Al | Ty | Env | Special | Rationale |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for entry, rows in groups:
        first = rows[0]
        if len(rows) == 1:
            name = first["Monster"]
            hd = first["HD"]
            atk = first["Atk"]
            dam = first["Dam"]
            ac = first["AC"]
            al = first["Align"]
            special = first["Special"]
            tr = first["Treas"]
        else:
            name = "%s ... %s (%d rows)" % (rows[0]["Monster"], rows[-1]["Monster"], len(rows))
            hd = "%s..%s" % (rows[0]["HD"], rows[-1]["HD"])
            atk = "/".join(sorted(set(r["Atk"] for r in rows), key=int)) if entry.get("expand", {}).get("kind") != "hydra" else "= heads"
            dam = "/".join(dict.fromkeys(r["Dam"] for r in rows))
            ac = "/".join(dict.fromkeys(r["AC"] for r in rows))
            al = "/".join(dict.fromkeys(r["Align"] for r in rows))
            tr = "/".join(dict.fromkeys(r["Treas"] for r in rows))
            # union of specials in row order, noting the age-gated Fear
            seen = []
            for r in rows:
                for s in r["Special"].split(", "):
                    if s not in seen and s != "-":
                        seen.append(s)
            flights = [s for s in seen if s.startswith("Flight (")]
            if len(flights) > 1:
                merged = "Flight (%s by age)" % "/".join(f[8:-1] for f in flights)
                seen = [merged if s == flights[0] else s for s in seen if s not in flights[1:]]
            if entry.get("source") == "dragons":
                seen = [s + " from Old up" if s == "Fear (2)" else
                        s + " from Sub-Adult up" if s == "Fearlessness" else s for s in seen]
            special = ", ".join(seen) if seen else "-"
        notes = " ".join(entry.get("notes", []))
        if entry.get("crit"):
            notes += " CRIT-DAMAGE PATTERN: %s." % entry["crit"]
        if entry.get("trigger"):
            notes += " Exceeds-by-4 trigger: %s." % entry["trigger"]
        if entry.get("unmapped"):
            notes += " Unmapped: " + " ".join(entry["unmapped"])
        lines.append("| %s |" % " | ".join(md_escape(str(x)) for x in [
            entry_label(entry), name, first["Number"], ac, first["MV"], hd,
            first["Lair%"], tr, atk, dam, al, first["Type"], first["Env"],
            special, notes.strip()]))
    with open("mapping.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote mapping.md (%d entries, %d rows)"
          % (len(groups), sum(len(r) for _, r in groups)))


NOTES_PREAMBLE = """# Notes: what the Delving Deeper database does not capture

Generated by `generate.py --notes` from `mapping.json`. Companion to
`mapping.md`.

## Source inconsistencies

* **Fire Elemental HD.** Table 3.1 gives 11+3; the *Explanation of Monsters*
  says all elementals come in 8, 12 and 16 HD sizes. The prose is used
  (three rows, like the other elementals).
* **Destrier MV.** Table 3.1 says 12, Table 3.11 says 15. Table 3.11 used.
* **Mastodons** are spelled "Mastadons" in Table 3.1.
* **Elemental group header** in Table 3.1 is singular ("Elemental"); the
  qualified names in tables.json follow the table.

## Arena engine caveats that affect this file

* **Dragon hit points.** `Monster.rollHitPoints` gives any monster with the
  `Dragon` special `HD x age-category` hit points (the OD&D idiom, where HD
  is fixed per colour). DD dragons already grow in HD with age, so Arena
  will give a Very Old (DD Ancient) Red Dragon 15 x 6 = 90 hp instead of
  the ~52 its 15 HD imply, and a Very Young (Hatchling) 2 hp. Breath damage
  equals hit points, so it is inflated the same way. HD are kept faithful to
  DD here; this is worth raising with Dan (a per-database switch, or reading
  DD dragons as HD-only).
* **EHD `?`.** MonsterMetrics skips monsters with undefined EHD when run
  over a whole database ("No measurable monsters found"); it still measures
  a monster named on the command line. To fill the EHD column, run it per
  monster or temporarily replace `?`.
* **Movement words.** `Flight (n)`, `Swimming (n)` and `WebMove (n)` are
  master-file conventions, not `SpecialType` names; Arena records them in
  `SpecialUnknownList` (shown by `MonsterMetrics -u`) and ignores them.
  The same happens with the master file.
* **Inert enum names.** `Sleep` (Pixie), `Webs` (Giant Spider), `Death` and
  `Hold` (Juggernaut) and `Disintegration` (Robot) exist in `SpecialType`
  but `Monster.java` only handles them as *conditions inflicted by spells*,
  never as a monster's own attack. They are included as documentation of
  the DD ability and have no effect in simulation.
* **Exceeds-by-4 triggers.** Arena has an analogous idiom: `Swallowing`,
  `Rending` and `Smothering` only trigger on a total attack roll of 25 or
  more. `Constriction`, `BloodDrain` and `Poison` trigger on any hit, so the
  DD monsters mapped to them are somewhat stronger than written.
* **Multiple attack rolls vs normal-types** (DD Combat, *Melee*: one roll
  per HD against sub-heroic foes) is not modelled, as in the master file.
  Dragons are "always heroic/superheroic, regardless of hit dice".
* **Impervious to normal missiles** (adult dragons, skeletons, zombies)
  has no code; Arena's fighters melee anyway.

## Master-file specials deliberately not carried over

MonsterDatabase.csv gives the OD&D analogue an ability that the DD text does
not mention. Since this file records DD, they are left out; add them back
in mapping.json if you would rather stay close to the master values.

* Dragons: `Detection (15)` becomes `Detection (6)` (DD range); `Fear (2)`
  only from DD Old up. Gold Dragon: `PoisonBreath` (DD goldens breathe
  sound; `FireBreath` stands in, see mapping.md).
* Elementals: `MagicToHit (2)` becomes `MagicToHit (1)` (DD: "affected by
  magical weapons only", no plus stated).
* Dwarf: `SaveBonus (4)`. Titan: `MagicResistance (60)`. Shadow: `BlankMind`.
* Bears, Lions, Tigers, Owl-bear-likes: `Rending` and second attacks (DD
  animals use one attack roll with the crit-damage pattern instead).

Rules found in the group introductions (Dragons, Elementals, Giants,
Golems, Living Statues) *are* applied: all giants hurl rocks and never
check morale against man-types; elementals need magic weapons; golems and
living statues are "largely invulnerable to harmful magic"; dragons sense
invisible creatures.

## EHD findings (see ehd-comparison.md)

`run-metrics.sh` computes every row's EHD with MonsterMetrics;
`compare-ehd.py` sets them against the master file's analogues recomputed
with the same build. Where DD and OD&D give the same stats the EHDs
agree (Orc, Ghoul, Wight, Wraith, Hill Giant, Giant Spider, hydras). The
systematic differences all trace to rules, not to the file:

* **Dragons.** The HD x age hit-point idiom above inverts DD's curve:
  hatchlings come out at EHD 1 (master 4-12) and ancients at 41-111
  (master 18-57). Only the middle ages are comparable. Fixing this needs
  a change in Arena, not in the CSV.
* **One attack roll.** DD gives most beasts a single attack where OED
  gives two or more, so bears, lions, trolls, minotaurs, werebears,
  griffons, mastodons, manticoras and squid land 1-6 EHD lower. For the
  animals part of that gap is the unmodelled crit-damage pattern.
* **Elementals** come out about a third lower (DD air elementals do 2-7,
  and any magic weapon hits rather than +2).
* **Higher than OED:** Giant Centipede 5 vs 1 (DD's is a 3+1 HD, 10 ft
  monster), Yellow Mold 5 vs 2 (3 HD vs 1), Treant 33 vs 26 (weapon
  immunity and half damage), Giant Viper 7 vs 5, Juggernaut 223.
* **Horses** that do not attack score 0.

## Crit-damage pattern ("exceeds the number required to hit by 4 or more, or is a 20")

DD gives these monsters a bigger damage figure on a high attack roll. Arena
has no SpecialType for it; the base figure is used. Candidates for a new
SpecialType (e.g. `CritDamage (n)` with n = extra dice) if Dan wants one:

"""


def write_notes(groups):
    lines = [NOTES_PREAMBLE]
    for entry, rows in groups:
        if entry.get("crit"):
            lines.append("* **%s** (DD *%s*): %s -> row uses `%s`."
                         % (rows[0]["Monster"], entry_label(entry), entry["crit"], rows[0]["Dam"]))
    lines.append("")
    lines.append("## Exceeds-by-4 (or natural 20) as a trigger for something other than damage")
    lines.append("")
    for entry, rows in groups:
        if entry.get("trigger"):
            lines.append("* **%s** (DD *%s*): %s." % (rows[0]["Monster"], entry_label(entry), entry["trigger"]))
    lines.append("")
    lines.append("## DD abilities with no Arena mapping, per monster")
    lines.append("")
    for entry, rows in groups:
        if entry.get("unmapped"):
            name = rows[0]["Monster"] if len(rows) == 1 else "%s (all %d rows)" % (
                re.sub(r"^\S+ (Hit Dice |Headed )?", "", rows[0]["Monster"]) if entry.get("expand") else rows[0]["Monster"].split(" ", 2)[-1] if entry.get("source") == "dragons" else rows[0]["Monster"], len(rows))
            if entry.get("source") == "dragons":
                name = "%s Dragon (all 6 ages)" % DRAGON_NAME[entry["color"]]
            lines.append("* **%s** (DD *%s*):" % (name, entry_label(entry)))
            for u in entry["unmapped"]:
                lines.append("  * %s" % u)
    with open("NOTES.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote NOTES.md")


def main(argv):
    flags = set(argv[1:]) or {"--csv"}
    if "--all" in flags:
        flags = {"--csv", "--mapping", "--notes"}
    groups = build()
    # Sanity: every DD summary row must be referenced by some entry.
    used = set(entry_label(e) for e, _ in groups)
    missing = [q for q in SUMMARY if q not in used]
    if missing:
        print("WARNING: DD summary rows not mapped: %s" % missing)
    names = [r["Monster"] for _, rows in groups for r in rows]
    dupes = sorted(set(n for n in names if names.count(n) > 1))
    if dupes:
        print("WARNING: duplicate Arena names: %s" % dupes)
    if "--csv" in flags:
        if EHD:
            missing = [r["Monster"] for _, rows in groups for r in rows if r["Monster"] not in EHD]
            if missing:
                print("WARNING: no EHD in %s for: %s" % (EHD_FILE, missing))
        else:
            print("NOTE: %s not found; EHD column left as '?'" % EHD_FILE)
        write_csv(groups)
    if "--mapping" in flags:
        write_mapping(groups)
    if "--notes" in flags:
        write_notes(groups)


if __name__ == "__main__":
    main(sys.argv)
