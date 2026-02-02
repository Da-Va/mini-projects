#!/usr/bin/env bash

set -e

SCRIPTS_DIR=$(dirname "$0")
SUBMISSION_DIR="$1"

"$SCRIPTS_DIR/extract_evaluation.py" "$SUBMISSION_DIR" > "$SUBMISSION_DIR/eval.md"

echo "Processing $SUBMISSION_DIR..."
pandoc -V "mainfont:DejaVu Sans" -V "monofont:DejaVu Sans Mono" --pdf-engine=xelatex --highlight-style=tango "$SUBMISSION_DIR/eval.md" -o "$SUBMISSION_DIR/eval.pdf"
