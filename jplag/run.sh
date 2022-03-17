#!/usr/bin/env bash 

set -e
set -o pipefail
set -u


INP="${1:-./codes}"
OUT_FOLDER="${2:-./result}"
TMP_FOLDER="./tmp"
LANG="java"

rm -rf "$TMP_FOLDER"
mkdir -p "$TMP_FOLDER"

# if INP does not exists print error
if [ ! -e "$INP"  ]; then
    echo "input does not exist"
    exit 1
fi

if [[ "$INP" == *.zip ]]; then
    echo "input is in zip file, extracting"
    unzip -q -o "$INP" -d "$TMP_FOLDER"
else
    echo "input is a dir, copying to temp folder"
    cp -r "$INP"/* "$TMP_FOLDER"
fi


for question in "$TMP_FOLDER"/*; do
    if [[ -d "$question" ]]; then
        echo "processing $question"
        question_name=$(basename "$question")
        ./one_question.sh "$question" "$OUT_FOLDER/$question_name" "$LANG"
    fi
done


