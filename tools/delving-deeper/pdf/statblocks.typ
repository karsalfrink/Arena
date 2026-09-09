#import "common.typ": setup, intro, colophon
#let d = json("build/statblocks.json")

#show: setup.with("Delving Deeper Monster Stat Blocks")

= Delving Deeper Monster Stat Blocks

#intro[
  Every monster of the _Delving Deeper_ rules on one line each, in the
  compact form of the OED Monster Stat Blocks, with an Equivalent Hit Dice
  (EHD) rating for each. EHD measures a monster's real fighting strength,
  which its hit dice alone often misjudge, so referees can pit encounters
  against a party with more confidence; the companion _Monster Matrices_
  handout uses the same ratings to build wandering-monster tables. The
  baseline is the fighting-man: a monster of EHD _n_ is an even match for
  fighters in chain mail totalling _n_ levels, whether _n_ first-level
  fighters or one fighter of level _n_, averaged over levels 1 to 12. So
  EHD 1 is one first-level fighting-man and EHD 0 a monster that does not
  fight.

  Monsters carry the names of Delving Deeper's Table 3.1 and are grouped
  by kind (animals, beasts, faerie and sylvan creatures, humanoids, men,
  slimes, undead, extraplanar) in Table 3.1 order within each group.
  _NA_ is the number appearing, _AL_ the alignment. Where the rules give a
  monster a range of hit dice (giant beetles, giant fish, pterodactyls,
  hydras, elementals) and the other columns agree, the family is one line
  with the EHD of each size in small type. _Special_ lists the abilities
  that the Arena simulator models, under its own names; the small-type
  _Also_ line beneath a monster gives the abilities it cannot model, which
  are therefore not in the EHD (see the colophon). Dragon EHDs (marked \*)
  were measured with ordinary hit dice, not with the values in the
  database; see the colophon.
]

#set text(size: 8.5pt)

#let also(text-, indent: 0mm) = table.cell(colspan: 10, inset: (top: 0pt, bottom: 2.6pt))[
  #h(indent + 3mm)#text(size: 7pt)[_Also:_ #text-]
]

#let row(e, indent: 0mm) = (
  [#h(indent)#e.name #if e.note != "" [\ #h(indent + 3mm)#text(size: 7pt)[#e.note]]],
  e.number, e.ac, e.mv, e.hd,
  if e.dragon [#e.ehd\*] else { e.ehd },
  e.atk, e.dam, e.align, e.special,
) + if e.also != "" { (also(e.also, indent: indent),) } else { () }

#for s in d.sections [
  == #s.title
  #table(
    columns: (40mm, 10mm, 7mm, 7mm, 12mm, 10mm, 10mm, 12mm, 8mm, 1fr),
    align: (left, center, center, center, center, center, center, center, center, left),
    stroke: none,
    inset: (x: 4pt, y: 2.2pt),
    table.hline(stroke: 0.6pt),
    table.header(
      [*Monster*], [*NA*], [*AC*], [*MV*], [*HD*], [*EHD*], [*Atk*], [*Dam*], [*AL*], [*Special*],
      table.hline(stroke: 0.4pt),
    ),
    ..for e in s.entries {
      if "group" in e {
        let head = (table.cell(colspan: 10)[_#e.group _],)
        if e.also != "" { head += (also(e.also),) }
        head + e.rows.map(row.with(indent: 3mm)).flatten()
      } else {
        row(e)
      }
    },
    table.hline(stroke: 0.6pt),
  )
]

#colophon(d)[
  *Names.* The database uses Arena's names, so "Beetles, giant" is Arena's
  "Two Hit Dice Giant Beetle" and so on; the groups are Arena's monster
  types.

  *Specials.* The _Special_ column holds Arena `SpecialType` codes: only
  the Delving Deeper abilities that could be mapped onto something the
  simulator models, and so only those that count towards the EHD. A few
  codes are documentation only (Arena knows the name but does not act on
  it as a monster attack); the _Also_ line marks these "not simulated".
  Abilities with no Arena counterpart, such as burrowing, split armour
  classes or a larger damage figure on a high attack roll, are on the
  _Also_ line, worded for play; the fuller record is per monster in
  `tools/delving-deeper/NOTES.md`.

  *Dragons.* Arena gives a dragon hit points of HD × age category (its
  OD&D idiom, where a dragon's HD are fixed), so the EHDs in the database
  make hatchlings far too weak and old and ancient dragons far too strong.
  The dragon EHDs here were therefore measured again with ordinary hit
  dice (`dragon-ehd.tsv` from `dragon-ehd.sh`, in which golden dragons
  lose their spells) and differ from the database column. See
  `tools/delving-deeper/NOTES.md`.
]
