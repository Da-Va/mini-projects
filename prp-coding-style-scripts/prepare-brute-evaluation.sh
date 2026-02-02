#!/usr/bin/env bash

set -e

HW_DIR="$1" ; [[ -d "$HW_DIR" ]]
SCRIPTS_DIR=$(dirname "$0")
# BRUTE_DIR="$HW_DIR"_brute
BRUTE_DIR=brute


mkdir -p "$BRUTE_DIR"

echo -n "" > "$BRUTE_DIR"/points.csv

for d in $(find "$HW_DIR" -maxdepth 1 -mindepth 1  -type d); do
    USER_NAME=$(basename "$d")
    cp "$d"/eval.pdf "$BRUTE_DIR"/"$USER_NAME".pdf

    POINTS=$(tail -1 "$d"/eval.md)
    echo "$USER_NAME,$POINTS" >> "$BRUTE_DIR"/points.csv
done

# cd "$BRUTE_DIR"
# zip "$BRUTE_DIR".zip *
zip -jr "$BRUTE_DIR".zip "$BRUTE_DIR"/
