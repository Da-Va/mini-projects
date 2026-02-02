#!/usr/bin/env bash

HW_DIR="$1"

for d in $(find "$HW_DIR" -maxdepth 1 -mindepth 1  -type d); do
  if [[ ! -e "$d/eval.txt" ]]; then
    echo "$d"
  fi
done
