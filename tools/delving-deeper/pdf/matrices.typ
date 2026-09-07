#import "common.typ": setup, front-note
#let d = json("build/matrices.json")

#show: setup.with("Delving Deeper Monster Matrices")

= Delving Deeper Monster Matrices

#front-note(d)[
  The Monster Level Matrix is Dan's (Arena's `MonsterLevelMatrix.csv`). The
  Monster Level Tables are rebuilt from the Delving Deeper EHDs with Arena's
  banding (`EHDToTable.csv`), with families collapsed and dragons placed by
  age as described under _Notes_. Monsters carry the names of Delving
  Deeper's Table 3.1.
]

== Monster Level Matrix

#let m = d.matrix
#table(
  columns: (auto,) + (1fr,) * m.levels,
  align: center,
  stroke: none,
  inset: (x: 5pt, y: 3pt),
  table.header(
    table.cell(rowspan: 2, align: horizon)[*Dungeon level*],
    table.cell(colspan: m.levels)[*Monster level*],
    ..range(1, m.levels + 1).map(i => [*#i*]),
    table.hline(stroke: 0.4pt),
  ),
  ..for r in m.rows { (r.dungeon, ..r.cells) },
  table.hline(stroke: 0.6pt),
)
#v(-2mm)
#text(size: 8pt)[Roll 1d6 on the row for the dungeon level; the result gives the monster level table to use.]

== Monster Level Tables

#let level-table(t) = block(breakable: false)[
  === Level #t.level (EHD #t.ehd)
  #table(
    columns: (auto, 1fr),
    align: (right, left),
    stroke: none,
    inset: (x: 4pt, y: 1.8pt),
    table.header([*d#t.die*], [*Monster*], table.hline(stroke: 0.4pt)),
    ..for (i, e) in t.entries.enumerate() { (str(i + 1), e.name) },
    table.hline(stroke: 0.6pt),
  )
]

#grid(
  columns: (1fr, 1fr), column-gutter: 8mm, row-gutter: 2mm,
  ..d.tables.map(level-table),
)

== Number Appearing

Assume a party of four characters. Wandering monsters appear 1d3 at a time
(average 2), on the assumption that dungeon level equates to Equivalent Hit
Dice. If the matrix cell rolled lies in the column that contains the 3–4
result for that dungeon level, use the number as rolled; for columns to the
left or right, multiply as follows.

#align(center)[
  #table(
    columns: 2, align: (left, center), stroke: none, inset: (x: 8pt, y: 2pt),
    table.header([*Column*], [*Multiplier*], table.hline(stroke: 0.4pt)),
    [Two to the left], [×3],
    [One to the left], [×2],
    [One to the right], [×½],
    [Two to the right], [×⅓],
    table.hline(stroke: 0.6pt),
  )
]

For dungeon lairs, with or without treasure, place 1d6 monsters (average
3.5) and modify in the same way. This guide is not meant for the deepest
levels (11+), where monster levels and EHDs vary greatly; there, multiply
the number by the ratio of dungeon level to EHD (the stat-block document
gives the exact EHDs). If the party is larger or smaller than four, scale
the numbers in proportion. At least one monster appears in any encounter,
which may be very dangerous.

== Notes

#let ex = d.excluded
- *Which monsters are listed.* As in Arena, only monsters of the dungeon
  environment with an EHD of 1 or more: not #ex.ehd0.join("; ") (EHD 0,
  they do not attack) and not the #ex.env monsters of the wilderness, the
  water or other planes (among them the men other than bandits, the
  dinosaurs, the elementals and the sea monsters).
- *Families.* Where Delving Deeper gives one monster a range of hit dice
  (giant beetles, hydras), each table lists the sizes whose EHD falls in
  its band. Giants, lycanthropes, golems and living statues are one entry
  per table with the kinds in parentheses; the two giant snakes are
  Delving Deeper's single entry. The rules are in `families.json`.
- *Dice.* Roll the die shown, or a larger die and roll again on a result
  above the table. Level 5 is short because the Delving Deeper EHDs
  cluster in the 3–4 and 11+ bands.
- *Dragons.* Arena gives a dragon hit points of HD × age category (its
  OD&D idiom, where a dragon's HD are fixed), so the EHDs in the database
  make hatchlings far too weak and old dragons far too strong. For the
  tables the dragons were therefore measured again with ordinary hit dice
  (`dragon-ehd.sh`, output #raw(d.dragons.tsv); golden dragons lose their
  spells in that run) and each age is placed by the median of its six
  colours. The values, with the resulting level, so that a colour can be
  moved up or down:

#let g = d.dragons
#align(center)[
  #table(
    columns: 8, align: (left,) + (center,) * 7, stroke: none,
    inset: (x: 6pt, y: 2pt),
    table.header([*Age*], ..g.colours.map(c => [*#c*]), [*Level*],
      table.hline(stroke: 0.4pt)),
    ..for r in g.grid { (r.age, ..r.ehds, str(r.level)) },
    table.hline(stroke: 0.6pt),
  )
]
