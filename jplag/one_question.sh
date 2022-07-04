#!/usr/bin/env bash

set -e
set -o pipefail
set -u

INP_FOLDER="$1"  #"./codes"
OUT_FOLDER="$2"  #"./result"
LANG="$3"        #"cpp"
LIB_FOLDER="$4"  #"./libs/current_question"

LIB_NAME="lib"
RES_COUNT="40"

clean_zip(){ 
   zip -d "$1" __MACOSX/\* \*/.DS_Store  > /dev/null 2>&1 || true
   true
}

function flatten(){
    return 0

    for student in "$INP_FOLDER"/*; do
        if [ -d "$student" ]; then
            echo "$student"

            find "$student" -type f | while read -r file; do
                dest="$INP_FOLDER/$student/$(basename -- "$file")"
                #echo "$file" "$dest"
                [ -f "$dest" ] || mv "$file" "$dest" > /dev/null 2>&1 && {
                    #echo "duplicate file: $file"
                    true
                    #return 1
                }
            done
        fi
    done
    find "$INP_FOLDER" -type d -empty -delete    
}

function textify(){ # for example textify dart
    find "$INP_FOLDER" -name "*.$1" -type f | while read file; do
        mv "$file" "${file%.$1}.txt"
    done
}

function clean_out_folder(){
    find "$OUT_FOLDER" \( -name "match*.html" -or -name "result.html" -or -name "matches_avg.csv" \) -delete
}

function clean_in_folder(){
    find "$INP_FOLDER" \( -name ".gitignore" -or -name ".idea" -or -name "*.class" -or -name ".git" \) -print0 | sort | uniq | xargs -0 -r -n 1 rm -r
}

case "$LANG" in
    "cpp" | "c" )
        EXTENSIONS="c,cpp"
        ;;
    * )
        EXTENSIONS="$LANG"
esac

ASTYLE_OPTS=(--quiet --suffix=none --recursive --style=java \
    --break-blocks --pad-comma --pad-first-paren-out \
    --unpad-paren --add-braces --convert-tabs \
    --delete-empty-lines --max-code-length=80)

JPLAG_JAR="./jplag.jar"
JPLAG_CMD="java -jar $JPLAG_JAR"
# -bc "$LIB_NAME" \
JPLAG_OPTS=(-l "$LANG" -p "$EXTENSIONS" \
    -v quiet -c normal -r "$OUT_FOLDER" -n "$RES_COUNT")

mkdir -p "$INP_FOLDER/$LIB_NAME"
unzip -q -o "$LIB_FOLDER" -d "$INP_FOLDER/$LIB_NAME"  > /dev/null 2>&1 || true


find "$INP_FOLDER" -name "result.txt" -type f -delete
find "$INP_FOLDER" -name "*.zip" -type f | while read -r file; do
    zip_path="${file%/*}"
    clean_zip "$file"
    unzip -q -o "$file" -d "$zip_path"
    rm "$file"
done


clean_in_folder

astyle "$INP_FOLDER/*" "${ASTYLE_OPTS[@]}"

flatten


mkdir -p "$OUT_FOLDER" 
clean_out_folder
$JPLAG_CMD "${JPLAG_OPTS[@]}" "${INP_FOLDER}" > "$OUT_FOLDER/jplag.log" || {
    cat "$OUT_FOLDER/jplag.log"
    exit 1
}

head -5 "$OUT_FOLDER/jplag.log"
tail -5 "$OUT_FOLDER/jplag.log"

python3 inplace.py "$OUT_FOLDER"
