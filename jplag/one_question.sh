#!/usr/bin/env bash

set -e
set -o pipefail
set -u

clean_zip(){ 
    # redirect stdout and stderr to /dev/null
    # so that we don't see the output of the unzip command

    zip -d "$1" __MACOSX/\* \*/.DS_Store  > /dev/null 2>&1 || true
}



INP_FOLDER="$1" #"./codes"
OUT_FOLDER="$2" #"./result"
LANG="$3"       # "cpp"
LIB_FOLDER="lib"
RES_COUNT="100"


case "$LANG" in
    "cpp" | "c" )
        EXTENSIONS="c,cpp"
        ;;
    * )
        EXTENSIONS="$LANG"
esac

#mkdir -p "$INP_FOLDER/$LIB_FOLDER"
#touch "$INP_FOLDER/$LIB_FOLDER/lib.$EXTENSIONS"

find "$INP_FOLDER" -name "*.txt" -type f -delete
find "$INP_FOLDER" -name "*.zip" -type f | while read -r file; do
    #echo "Unzipping $file"
    zip_path="${file%/*}"
    clean_zip "$file"
    unzip -q -o "$file" -d "$zip_path"
    rm "$file"
done

#find "$INP_FOLDER" -name "*" -type d -delete

ASTYLE_OPTS=(--quiet --suffix=none --recursive --style=java \
    --break-blocks --pad-comma --pad-first-paren-out \
    --unpad-paren --add-braces --convert-tabs \
    --delete-empty-lines --max-code-length=80)
astyle "$INP_FOLDER/*" "${ASTYLE_OPTS[@]}"


JPLAG_JAR="./jplag.jar"
JPLAG_CMD="java -jar $JPLAG_JAR"

OPTS_LANG=(-l "$LANG" -p "$EXTENSIONS") # -bc "$LIB_FOLDER")
OPTS_GENERAL=(-v quiet -c normal -r "$OUT_FOLDER" -n "$RES_COUNT")

mkdir -p "$OUT_FOLDER" 
$JPLAG_CMD "${OPTS_GENERAL[@]}" "${OPTS_LANG[@]}" "${INP_FOLDER}" >  "$OUT_FOLDER/jplag.log"

python3 inplace.py "$OUT_FOLDER"

