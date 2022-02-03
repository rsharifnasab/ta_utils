#!/usr/bin/env bash 

set -e
set -o pipefail
set -u

INP_FOLDER="./codes"
OUT_FOLDER="./result"

./ss-single.sh $INP_FOLDER $OUT_FOLDER
