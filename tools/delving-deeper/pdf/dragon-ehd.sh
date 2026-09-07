#!/bin/sh
# HD-only EHDs for the dragon rows of MonsterDatabase-DelvingDeeper.csv.
#
# Arena gives any monster named "... Dragon" hit points of HD x age category
# (see ../NOTES.md), which makes the CSV's dragon EHDs unreliable at the
# young and old ends. This script runs MonsterMetrics on a scratch copy of
# the database in which the dragons are renamed "... Drake", so that they
# roll ordinary hit dice, and writes dragon-ehd.tsv (Arena name, EHD), which
# build.py uses to place dragons in the Monster Level Tables. Gold dragons
# lose their spells in the scratch copy (Arena keys them on the name).
# Run from anywhere; compiles Arena into ../build first. A few minutes.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT="$HERE/../../.."
BUILD="$HERE/../build"
SCRATCH="$HERE/build/drakes.csv"
OUT="$HERE/dragon-ehd.tsv"
mkdir -p "$BUILD" "$HERE/build"
(cd "$ROOT" && javac -cp pdfbox-app.jar -d "$BUILD" *.java)
sed 's/^\([^,]*\) Dragon,/\1 Drake,/' "$ROOT/MonsterDatabase-DelvingDeeper.csv" > "$SCRATCH"
printf 'Monster\tEHD\n' > "$OUT"
cd "$ROOT"
grep -o '^[^,]* Drake' "$SCRATCH" | while IFS= read -r m; do
  java -cp "$BUILD:pdfbox-app.jar" MonsterMetrics "-b=$SCRATCH" "$m" 2>&1 \
    | sed -n 's/^\(.*\) Drake: Old EHD -\{0,1\}[0-9]*, New EHD \([0-9]*\) (\([0-9.]*\))$/\1 Dragon\t\2/p' >> "$OUT"
done
echo "wrote $OUT ($(($(wc -l < "$OUT") - 1)) rows)"
