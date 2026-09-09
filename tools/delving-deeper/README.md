# Delving Deeper monster database: tools

This directory produces `MonsterDatabase-DelvingDeeper.csv` in the
repository root, an Arena monster database for every monster in the OD&D
retroclone [Delving Deeper](https://ddo.immersiveink.com/), with EHDs
computed by Arena's own MonsterMetrics.

## How it was made

This pipeline and the database were produced with a large language model.
Kars Alfrink worked with Claude (Anthropic's Claude Fable 5.1, via Claude
Code) in an interactive session: the model read the Arena sources to
establish the format constraints, wrote the parser, proposed the
per-monster mapping and the SpecialType codes, generated the CSV, wrote the
validator and ran MonsterMetrics. Kars reviewed the mapping before the CSV
was generated and made the judgement calls it flagged (split ACs, the
crit-damage pattern, inert SpecialType names). The bulk of the text in
`mapping.json`, `mapping.md` and `NOTES.md` is the model's. Each commit
carries a `Co-Authored-By` trailer for the model.

The pipeline is reproducible and the rationale per monster is written down,
so mistakes can be traced and fixed, but the mapping deserves a second pair
of eyes.

## Files

| File | Role |
|---|---|
| `delving-deeper-rules.html` | SingleFile capture of the Delving Deeper reference rules (source) |
| `parse.py` | Reads the HTML into `tables.json` (Table 3.1 and the dragon, giant, horse and roc tables) and `descriptions.json` (the Explanation of Monsters prose, including the group introductions) |
| `mapping.json` | One entry per Arena row or expansion group: attack routine, Type/Env, SpecialType codes, notes, every DD ability that could not be mapped, and its `handout` wording for the stat-block PDF |
| `generate.py` | Derives the remaining columns from `tables.json`, renders `mapping.md` and `NOTES.md`, and writes the CSV |
| `mapping.md` | The human-readable mapping: derivation rules plus one line per DD entry with rationale |
| `NOTES.md` | Source inconsistencies, Arena engine caveats, the crit-damage pattern list, EHD findings, and unmapped abilities per monster |
| `validate.py` | Checks each row the way Arena's Java loader would and cross-checks AC/HD/Align against `tables.json` |
| `run-metrics.sh` | Compiles Arena and computes EHD for every row with MonsterMetrics, writing `ehd.tsv` |
| `compare-ehd.py` | Sets the DD EHDs against the master file's analogues, writing `ehd-comparison.md` |

## Regenerating

From this directory:

```sh
python3 parse.py            # tables.json, descriptions.json
python3 generate.py --all   # CSV, mapping.md, NOTES.md
python3 validate.py         # loader-style checks and table cross-check
./run-metrics.sh            # ehd.tsv (a couple of minutes)
python3 generate.py --csv   # copy the EHDs into the CSV
```

`compare-ehd.py` needs MonsterMetrics output for the master files as its
argument; see its docstring.
