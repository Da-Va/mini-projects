#!/usr/bin/env bash

SCRIPTS_DIR=$(dirname "$0")

"$SCRIPTS_DIR"/list-submissions.sh "$1" | shuf | fzf | xargs -I {} nvim -O {}/main.c {}/eval.txt
