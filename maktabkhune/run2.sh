#!/bin/bash

set -e
set -o nounset
set -o pipefail

LOOKING_FOLDER="$HOME/Downloads/"
TMP_FOLDER="./tmp"

extract(){
    if [ -f "$1" ] ; then
        case "$1" in
            *.zip) unzip "$1" -d "$TMP_FOLDER" > /dev/null ;;
            *.rar) unrar x "$1" "$TMP_FOLDER" > /dev/null ;;
            *) echo "'$1 cannot be extracted" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}


function gat(){
    src-hilite-lesspipe.sh "$@" | less
}


#rm -rf "$TMP_FOLDER" || true
#mkdir "$TMP_FOLDER"



#find "$LOOKING_FOLDER" -maxdepth 1 -type f -printf "%C@ %p\0" | sort -zrn | { \
#     read -d '' ts file; \
#     echo "$file"; \
#     extract "$file"
#}


the_c=`find "$TMP_FOLDER" -name "*.c" -print`

# --suffix=none 
# --pad-oper
ASTYLE_OPTS=(--quiet --mode=c --style=kr --break-blocks --pad-comma --pad-first-paren-out --unpad-paren --add-braces --convert-tabs --delete-empty-lines)
GCC_OPTS=(-Wall -Wno-implicit -lm)
SPLINT_OPTS=(-standard -hints +quiet -limit 1 -retvalint -retvalother -bufferoverflowhigh +matchanyintegral -exportlocal)

bat --paging=never --language=c "$the_c"
clang-format -i "$the_c" --style=Google
astyle "$the_c" "${ASTYLE_OPTS[@]}"
bat --paging=never "$the_c"
gcc "${GCC_OPTS[@]}" "$the_c" -o "$TMP_FOLDER/a.out"
#splint -weak -hints +quiet -limit 1 -retvalother -bufferoverflowhigh "$the_c" || true
splint "${SPLINT_OPTS[@]}" "$the_c" || true
#read -p "Press enter to continue"
echo "running the program"
firejail --private="$TMP_FOLDER" --net=none --quiet ./a.out
#rm -rf "$TMP_FOLDER" || true
echo ""

