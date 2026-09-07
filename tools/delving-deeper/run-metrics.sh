#!/bin/sh
# Compute EHD for every row of the Delving Deeper database with Arena's own
# MonsterMetrics (spotlight mode, one monster per run) and write ehd.tsv.
# Run from this directory. Compiles Arena into ./build first.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
ROOT="$HERE/../.."
CSV="MonsterDatabase-DelvingDeeper.csv"
BUILD="$HERE/build"
mkdir -p "$BUILD"
(cd "$ROOT" && javac -cp pdfbox-app.jar -d "$BUILD" *.java)
cd "$ROOT"
OUT="$HERE/ehd.tsv"
printf 'Monster\tEHD\tEHD_exact\n' > "$OUT"
tail -n +2 "$CSV" | tr -d '\r' | python3 -c 'import sys,csv
for r in csv.reader(sys.stdin): print(r[0])' | while IFS= read -r m; do
  java -cp "$BUILD:pdfbox-app.jar" MonsterMetrics "-b=$CSV" "$m" 2>&1 \
    | sed -n 's/^\(.*\): Old EHD -\{0,1\}[0-9]*, New EHD \([0-9]*\) (\([0-9.]*\))$/\1\t\2\t\3/p' >> "$OUT"
done
echo "wrote $OUT ($(($(wc -l < "$OUT") - 1)) rows)"
