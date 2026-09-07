#import "common.typ": setup, front-note
#let d = json("build/statblocks.json")

#show: setup.with("Delving Deeper Monster Stat Blocks")

= Delving Deeper Monster Stat Blocks

#front-note(d)[
  Monsters are listed by Arena type (animals, beasts, faerie and sylvan
  creatures, humanoids, men, slimes, undead, extraplanar), then by EHD, then
  by HD, as in the database. Where the rules give a monster a range of hit
  dice (giant beetles, giant fish, pterodactyls, hydras, elementals) and
  the other columns agree, the family is one line with the EHD of each
  size in small type. Special abilities use Arena's `SpecialType` names.
  _Dragon EHDs_ (marked \*) are unreliable at the extremes: Arena gives a
  dragon hit points of HD × age category, so Very Young dragons come out
  far too weak and Old and Very Old dragons far too strong; only the
  middle ages are comparable. See `tools/delving-deeper/NOTES.md`.
]

#set text(size: 8.5pt)

#for s in d.sections [
  == #s.title
  #table(
    columns: (46mm, 8mm, 8mm, 13mm, 11mm, 9mm, 13mm, 1fr),
    align: (left, center, center, center, center, center, center, left),
    stroke: none,
    inset: (x: 4pt, y: 2.2pt),
    table.hline(stroke: 0.6pt),
    table.header(
      [*Monster*], [*AC*], [*MV*], [*HD*], [*EHD*], [*Atk*], [*Dam*], [*Special*],
      table.hline(stroke: 0.4pt),
    ),
    ..for e in s.entries {
      (
        if e.note == "" { e.name } else [#e.name \ #text(size: 7pt)[#e.note]],
        e.ac, e.mv, e.hd,
        if e.dragon [#e.ehd\*] else { e.ehd },
        e.atk, e.dam, e.special,
      )
    },
    table.hline(stroke: 0.6pt),
  )
]
