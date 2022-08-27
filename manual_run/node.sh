#!/bin/bash

set -o errexit
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


BAT_OPTS=(--paging=never)
TREE_OPTS=(--dirsfirst  --noreport --si --du -htr)


KEEP="${1:-delete}"
# if keep is set to 1, then keep the original file
if [ "$KEEP" != "keep" ]; then
    echo "Keeping original file"

    # clear temp folder
    rm -rf "$TMP_FOLDER"
    mkdir "$TMP_FOLDER"

    # find and extract submission file from downloads
    find "$LOOKING_FOLDER" -maxdepth 1 -type f -printf "%C@ %p\0" | \
        sort -zrn | { \
            read -d '' ts file; \
            echo "$file"; \
            extract "$file"
        }
fi


\tree "${TREE_OPTS[@]}" -- "$TMP_FOLDER"
all_src=`find "$TMP_FOLDER" -type d -name node_modules -prune -o   -name "*.js" -print`
echo "$all_src"

# for each in all_src
for src in $all_src; do
    bat "${BAT_OPTS[@]}" "${src}"
done


(
cd tmp
cd ./* || true

npm install --prefer-offline --legacy-peer-deps --quiet --loglevel=error

read -p "Press enter to continue"

npm start --quiet


#node index.js

)

