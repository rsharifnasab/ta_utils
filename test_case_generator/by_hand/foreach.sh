#!/bin/bash

set -e
set -u

reports="$1.report"
processed="$1.processed"

touch "$reports"
touch "$processed"

for file in "$1"/*/*.c*
do
    # file in processed
    if grep -q "$file" "$processed"
    then 
        continue
    fi
    bat "$file" # --pager=never
    read -rp "Enter your report: " user_report_raw
    user_report=`echo "$user_report_raw" | sed 's/ *$//g'`
    if [[ $user_report ]]
    then
        printf "%s -> %s\n" "$file " "$user_report" >> "$reports"
    fi
    printf "%s\n" "$file" >> "$processed"
done
