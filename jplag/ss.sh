#!/usr/bin/env bash 

set -e
set -o pipefail
set -u


INP_FOLDER="${1:-./codes}"
OUT_FOLDER="${2:-./result}"

LANG="java"


./ss-single.sh "$INP_FOLDER" "$OUT_FOLDER" "$LANG"
