#!/bin/bash

# Copyright 2017 Abdel HEBA Linagora GSO

# Extract and normalize text from file.trs built with Transcriber for subsequent language model training

echo $@

. path.sh || exit 1

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <input-book-dirs> <output-root>"
  exit 1
fi

in_list=$1
out_root=$2

[[ -f "$in_list" ]] || { echo "The input file '$in_list' does not exists!"; exit 1; }

mkdir -p $out_root

processed=0

for b in $(cat $in_list); do
    id=$(basename $b)
    echo "Start processing $id at $(date '+%T %F')"
    in_file=$b/$id.trs
    [[ -f "$in_file" ]] || { echo "WARNING: $in_file does not exists"; continue; }
    #python3 local/parse_AudioDB.py $b
    python3 local/lm/parseText.py $in_file |\
    $PYTHON local/lm/pre_filter.py /dev/stdin $out_root/$id.txt
    #$PYTHON local/lm/pre_filter.py /dev/stdin $out_root/corpus_train.txt
    processed=$((processed + 1))
    echo "Processing of $id has finished at $(date '+%T %F') [$processed texts ready so far]"
done

echo "$processed texts processed OK and stored under '$out_root'"
