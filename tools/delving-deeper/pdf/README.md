# Delving Deeper reference PDFs

Two A4 handouts generated from `MonsterDatabase-DelvingDeeper.csv`,
modelled on Dan Collins's OED Monster Stat Blocks and OED Monster Matrices:

* `DD-MonsterStatBlocks.pdf`: every monster with NA, AC, MV, HD, EHD,
  Atk, Dam, alignment and Arena specials, in a table per Arena type and in
  Delving Deeper Table 3.1 order; abilities Arena does not model follow in
  a small-type line (the `handout` field of `../mapping.json`).
* `DD-MonsterMatrices.pdf`: the Monster Level Matrix, Monster Level Tables
  built from the Delving Deeper EHDs, and Number Appearing.

## Regenerating

```sh
python3 tools/delving-deeper/pdf/build.py
```

Needs Python 3 and [Typst](https://typst.app) (`brew install typst`).
The script reads the CSV, `MonsterLevelMatrix.csv` and `EHDToTable.csv`
from the repository root, takes the Delving Deeper names from
`../mapping.json` through `../generate.py`, writes JSON into `build/` and
compiles `statblocks.typ` and `matrices.typ`. Each PDF is stamped with the
commit that last changed the CSV. Run it again whenever the CSV changes.

If the dragon rows change, also run `./dragon-ehd.sh` (needs Java, a few
minutes): it measures the dragons with ordinary hit dice instead of
Arena's HD × age rule and writes `dragon-ehd.tsv`, which gives the dragon EHDs in the stat blocks and places dragons
in the level tables. MonsterMetrics is a simulation, so the values move by
a point or two between runs.

## Files

| File | Role |
|---|---|
| `build.py` | The generator: data preparation and the Typst calls |
| `common.typ` | Page setup, the opening paragraph and the colophon |
| `statblocks.typ`, `matrices.typ` | The two documents |
| `families.json` | How rows collapse into one level-table entry |
| `dragon-ehd.sh`, `dragon-ehd.tsv` | HD-only dragon EHDs for both documents |
| `build/` | Intermediate JSON, not committed |

Like the database, these were produced with a large language model
(Claude, via Claude Code) under Kars Alfrink's review; see `../README.md`.
