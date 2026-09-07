#import "common.typ": setup, front-note
#let d = json("build/matrices.json")

#show: setup.with("Delving Deeper Monster Matrices")

= Delving Deeper Monster Matrices

#front-note(d)[
  The Monster Level Matrix is Dan's (Arena's `MonsterLevelMatrix.csv`). The
  Monster Level Tables are rebuilt from the Delving Deeper EHDs with Arena's
  banding (`EHDToTable.csv`): only dungeon monsters (Env D) with an EHD of
  1 or more are listed, and monster families are collapsed into one entry as
  described under _Notes_.
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
#text(size: 8pt)[Roll the die shown, or a larger die and roll again on a result above the table.]

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
- *Not in the tables:* #ex.ehd0.join(", ") (EHD 0, no attack) and the
  #ex.env monsters whose environment is wilderness, water or another plane.
- *Families* (provisional, see `families.json`): giant beetles, hydras and
  the like are one entry per table with the range of sizes that fall in
  that band; giants, lycanthropes, golems and living statues are one entry
  each with the members in parentheses.
- *Dragons* (provisional): one entry, _Dragon (any)_, at level 6, as in
  the OED tables, because the Arena EHDs for Very Young and Very Old
  dragons are not reliable (see the stat-block document).
