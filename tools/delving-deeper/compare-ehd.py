#!/usr/bin/env python3
"""Compare the computed Delving Deeper EHDs (ehd.tsv) with the master
database's analogous monsters, recomputed with the same Arena build.

Usage:  python3 compare-ehd.py MASTER_EHD_FILE
where MASTER_EHD_FILE is MonsterMetrics output lines
("Name: Old EHD n, New EHD m (x.xx)") for MonsterDatabase.csv,
MonsterDatabase-Dragons.csv and MonsterDatabase-Hydras.csv.
Writes ehd-comparison.md.
"""
import csv
import re
import sys

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
ROOT = HERE + "/../.."

# DD row -> master row. Only monsters that are the same creature in both.
ANALOGUES = [
    ("Orc", "Orc"), ("Goblin", "Goblin"), ("Kobold", "Kobold"),
    ("Hobgoblin", "Hobgoblin"), ("Gnoll", "Gnoll"), ("Ogre", "Ogre"),
    ("Troll", "Troll"), ("Hill Giant", "Hill Giant"), ("Stone Giant", "Stone Giant"),
    ("Frost Giant", "Frost Giant"), ("Fire Giant", "Fire Giant"),
    ("Cloud Giant", "Cloud Giant"), ("Storm Giant", "Storm Giant"), ("Titan", "Titan"),
    ("Skeleton", "Skeleton"), ("Zombie", "Zombie"), ("Ghoul", "Ghoul"), ("Wight", "Wight"),
    ("Wraith", "Wraith"), ("Mummy", "Mummy"), ("Spectre", "Spectre"), ("Vampire", "Vampire"),
    ("Yellow Mold", "Yellow Mold"), ("Green Slime", "Green Slime"), ("Gray Ooze", "Gray Ooze"),
    ("Gelatinous Cube", "Gelatinous Cube"), ("Ochre Jelly", "Ochre Jelly"),
    ("Black Pudding", "Black Pudding"),
    ("Bear", "Bear"), ("Lion", "Lion"), ("Sabre-Toothed Tiger", "Sabre-Tooth Tiger"),
    ("Boar", "Boar"), ("Wolf", "Wolf"), ("Giant Wolf", "Dire Wolf"), ("Giant Rat", "Giant Rat"),
    ("Giant Centipede", "Giant Centipede"), ("Giant Spider", "Giant Spider"),
    ("Large Spider", "Large Spider"), ("Giant Scorpion", "Giant Scorpion"),
    ("Giant Toad", "Giant Toad"), ("Giant Leech", "Giant Leech"), ("Giant Weasel", "Giant Weasel"),
    ("Giant Lizard", "Giant Lizard"), ("Giant Crab", "Giant Crab"),
    ("Crocodile", "Crocodile"), ("Giant Crocodile", "Giant Crocodile"),
    ("Giant Viper", "Giant Poisonous Snake"), ("Giant Constrictor Snake", "Giant Constrictor Snake"),
    ("Giant Octopus", "Giant Octopus"), ("Giant Squid", "Giant Squid"),
    ("Mastodon", "Mastodon"), ("Tyrannosaurus Rex", "Tyranosaurus Rex"), ("Wight Ape", "White Ape"),
    ("Basilisk", "Basilisk"), ("Cockatrice", "Cockatrice"), ("Medusa", "Medusa"), ("Gorgon", "Gorgon"),
    ("Chimera", "Chimera"), ("Manticora", "Manticore"), ("Wyvern", "Wyvern"),
    ("Salamander", "Salamander"), ("Minotaur", "Minotaur"), ("Gargoyle", "Gargoyle"),
    ("Doppelganger", "Doppleganger"), ("Shadow", "Shadow"), ("Purple Worm", "Purple Worm"),
    ("Dragon Turtle", "Dragon Turtle"), ("Gothrog", "Balrog"),
    ("Werewolf", "Werewolf"), ("Wereboar", "Wereboar"), ("Weretiger", "Weretiger"), ("Werebear", "Werebear"),
    ("Flesh Golem", "Flesh Golem"), ("Stone Living Statue", "Stone Golem"), ("Iron Living Statue", "Iron Golem"),
    ("Dwarf", "Dwarf"), ("Elf", "Elf"), ("Gnome", "Gnome"), ("Pixie", "Pixie"), ("Nixie", "Nixie"),
    ("Dryad", "Dryad"), ("Centaur", "Centaur"), ("Unicorn", "Unicorn"), ("Pegasus", "Pegasus"),
    ("Hippogriff", "Hippogriff"), ("Griffon", "Griffon"), ("Treant", "Treant"),
    ("Animated Tree", "Animated Tree"), ("Young Roc", "Small Roc"), ("Adult Roc", "Medium Roc"),
    ("Ancient Roc", "Large Roc"),
    ("Bandit", "Bandit"), ("Brigand", "Brigand"), ("Berserker", "Berserker"), ("Dervish", "Dervish"),
    ("Nomad", "Nomad"), ("Buccaneer", "Buccaneer"), ("Pirate", "Pirate"), ("Merman", "Merman"),
    ("Caveman", "Caveman"),
    ("Djinni", "Djinni"), ("Efreeti", "Efreeti"), ("Invisible Stalker", "Invisible Stalker"),
    ("Eight Hit Dice Air Elemental", "Small Air Elemental"), ("Twelve Hit Dice Air Elemental", "Medium Air Elemental"),
    ("Sixteen Hit Dice Air Elemental", "Large Air Elemental"),
    ("Eight Hit Dice Earth Elemental", "Small Earth Elemental"), ("Twelve Hit Dice Earth Elemental", "Medium Earth Elemental"),
    ("Sixteen Hit Dice Earth Elemental", "Large Earth Elemental"),
    ("Eight Hit Dice Fire Elemental", "Small Fire Elemental"), ("Twelve Hit Dice Fire Elemental", "Medium Fire Elemental"),
    ("Sixteen Hit Dice Fire Elemental", "Large Fire Elemental"),
    ("Eight Hit Dice Water Elemental", "Small Water Elemental"), ("Twelve Hit Dice Water Elemental", "Medium Water Elemental"),
    ("Sixteen Hit Dice Water Elemental", "Large Water Elemental"),
    ("Draft Horse", "Draft Horse"), ("Mule", "Mule"), ("Riding Horse", "Light Horse"),
    ("War Horse", "Medium Horse"), ("Destrier", "Heavy Horse"),
]
for n in ["Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]:
    ANALOGUES.append(("%s-Headed Hydra" % n, "%s-Headed Hydra" % n))
for color in ["White", "Black", "Green", "Blue", "Red", "Gold"]:
    for age in ["Very Young", "Young", "Sub-Adult", "Adult", "Old", "Very Old"]:
        ANALOGUES.append(("%s %s Dragon" % (age, color), "%s %s Dragon" % (age, color)))


def read_rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["Monster"]: r for r in csv.DictReader(fh)}


def read_metrics(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"(.*): Old EHD (-?\d+), New EHD (\d+) \(([\d.]+)\)", line.strip())
        if m:
            out[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return out


def stat(r):
    return "AC %s HD %s Atk %s Dam %s; %s" % (r["AC"], r["HD"], r["Atk"], r["Dam"], r["Special"])


def main():
    master_metrics = read_metrics(sys.argv[1])
    dd = read_rows(ROOT + "/MonsterDatabase-DelvingDeeper.csv")
    master = {}
    for f in ("MonsterDatabase.csv", "MonsterDatabase-Dragons.csv", "MonsterDatabase-Hydras.csv"):
        master.update(read_rows(ROOT + "/" + f))
    lines = ["# EHD comparison: Delving Deeper rows vs the master (OD&D/OED) database",
             "",
             "Both columns are computed with the same Arena build (MonsterMetrics",
             "spotlight mode, 1000 fights per point). 'Master stored' is the EHD in",
             "MonsterDatabase.csv; 'master new' is the same row recomputed today, so",
             "the DD value should be read against 'master new'. Stat differences",
             "explain most gaps: DD monsters usually get one attack roll where OED",
             "gives several, and DD's crit-damage pattern is not modelled.",
             "",
             "| DD row | DD EHD | Master row | Master new | Master stored | DD stats | Master stats |",
             "|---|---|---|---|---|---|---|"]
    for dname, mname in ANALOGUES:
        if dname not in dd or mname not in master or mname not in master_metrics:
            continue
        d, m = dd[dname], master[mname]
        lines.append("| %s | %s | %s | %d | %s | %s | %s |" % (
            dname, d["EHD"], mname, master_metrics[mname][1], m["EHD"],
            stat(d), stat(m)))
    with open(HERE + "/ehd-comparison.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote ehd-comparison.md (%d pairs)" % (len(lines) - 11))


if __name__ == "__main__":
    main()
