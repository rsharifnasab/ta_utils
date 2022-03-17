#!/usr/bin/env bash 

set -e
set -o pipefail
set -u


INP="${1:-./codes}"
OUT_FOLDER="${2:-./result}"
LIBS_FOLDER="${3:-NO_LIB}"
TMP_FOLDER="./tmp"
LANG="java"

rm -rf "$TMP_FOLDER"
mkdir -p "$TMP_FOLDER"

# if INP does not exists print error
if [ ! -e "$INP"  ]; then
    echo "Input does not exist"
    exit 1
fi

if [[ "$INP" == *.zip ]]; then
    echo "Zip file detected, extracting to tmp folder..."
    unzip -q -o "$INP" -d "$TMP_FOLDER"
else
    echo "Input dir detected, copying to tmp folder..."
    cp -r "$INP"/* "$TMP_FOLDER"
fi


for question in "$TMP_FOLDER"/*; do
    if [[ -d "$question" ]]; then
        question_name=$(basename "$question")
        echo "processing $question_name"
        ./one_question.sh "$question" "$OUT_FOLDER/$question_name" "$LANG" "$LIBS_FOLDER/$question_name"
    fi
done


rm -rf "$TMP_FOLDER"
echo "done"
