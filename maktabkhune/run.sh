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


# --suffix=none 
# --pad-oper
ASTYLE_OPTS=(--quiet --mode=c --style=kr --break-blocks --pad-comma --pad-first-paren-out --unpad-paren --add-braces --convert-tabs --delete-empty-lines)
GCC_OPTS=(-Wall -Wno-implicit -lm)
SPLINT_OPTS=(-standard -hints +quiet -limit 1 -retvalint -retvalother -bufferoverflowhigh +matchanyintegral -exportlocal)
BAT_OPTS=(--style=numbers --paging=never)
TREE_OPTS=(--dirsfirst  --noreport --si --du -htr)


# clear temp folder
rm -rf "$TMP_FOLDER"
mkdir "$TMP_FOLDER"

# find and extract submission file from downloads
find "$LOOKING_FOLDER" -maxdepth 1 -type f -printf "%C@ %p\0" | sort -zrn | { \
    read -d '' ts file; \
    echo "$file"; \
    extract "$file"
}

# zip's file structure
tree "${TREE_OPTS[@]}" -- "$TMP_FOLDER"
all_c=`find "$TMP_FOLDER" -name "*.c" -print`
the_c=`echo "$all_c" | head -1`

# view unmodified code
bat "${BAT_OPTS[@]}" "$the_c"
echo "----------------------"

# format code and view it again
clang-format -i "$the_c" --style=Google
astyle "$the_c" "${ASTYLE_OPTS[@]}"
bat "${BAT_OPTS[@]}" "$the_c"

# compile, view compiler warnings and linter messages
gcc "${GCC_OPTS[@]}" "$the_c" -o "$TMP_FOLDER/a.out"
splint "${SPLINT_OPTS[@]}" "$the_c" || true
#read -p "Press enter to continue"

echo "running the program"
firejail --private="$TMP_FOLDER" --net=none --quiet ./a.out
#rm -rf "$TMP_FOLDER" || true
echo ""

