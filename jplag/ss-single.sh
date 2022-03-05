#!/usr/bin/env bash

set -e
set -o pipefail
set -u

INP_FOLDER="$1" #"./codes"
OUT_FOLDER="$2" #"./result"
LANG="$3"       # "cpp"
LIB_FOLDER="lib"
RES_COUNT="100"

mkdir -p "$INP_FOLDER/$LIB_FOLDER"


case "$LANG" in
    "cpp" | "c" )
        EXTENSIONS="c,cpp"
        ;;
    * )
        EXTENSIONS="$LANG"
esac

find "$INP_FOLDER" -name "*.txt" -type f -delete
find "$INP_FOLDER" -name "*.zip" -type f | while read -r file; do
    echo "Unzipping $file"
    zip_path="${file%/*}"
    unzip -o "$file" -d "$zip_path"
    rm "$file"
done

ASTYLE_OPTS=(--suffix=none --recursive --style=java --break-blocks --pad-comma --pad-first-paren-out --unpad-paren --add-braces --convert-tabs --delete-empty-lines)
astyle "$INP_FOLDER/*" "${ASTYLE_OPTS[@]}"


JPLAG_JAR="./jplag.jar"
JPLAG_CMD="java -jar $JPLAG_JAR"

OPTS_LANG=(-l "$LANG" -p "$EXTENSIONS" -bc "$LIB_FOLDER")
OPTS_GENERAL=(-v quiet -c normal -r "$OUT_FOLDER" -n "$RES_COUNT")

$JPLAG_CMD "${OPTS_GENERAL[@]}" "${OPTS_LANG[@]}" "${INP_FOLDER}"

python3 inplace.py "$OUT_FOLDER"

