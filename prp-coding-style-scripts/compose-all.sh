#!/usr/bin/env bash

set -e

HW_DIR="$1"
SCRIPTS_DIR=$(dirname "$0")

find "$HW_DIR" -maxdepth 1 -mindepth 1  -type d | xargs -P "$(nproc)" -I {} "$SCRIPTS_DIR/compose-evaluation.sh" {}
