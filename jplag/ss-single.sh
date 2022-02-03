#!/usr/bin/env bash 

set -e
set -o pipefail
set -u

LANG="cpp"
EXTENSIONS="c,cpp"
INP_FOLDER="$1" #"./codes"
OUT_FOLDER="$2" #"./result"
LIB_FOLDER="lib"
RES_COUNT="100"


JPLAG_JAR="./jplag.jar"
JPLAG_CMD="java -jar $JPLAG_JAR"

OPTS_LANG=(-l "$LANG" -p "$EXTENSIONS") # -bc "$LIB_FOLDER")
OPTS_GENERAL=(-v quiet -c normal -r "$OUT_FOLDER" -n "$RES_COUNT")

$JPLAG_CMD "${OPTS_GENERAL[@]}" "${OPTS_LANG[@]}" "${INP_FOLDER}"

