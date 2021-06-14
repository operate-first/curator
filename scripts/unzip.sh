#!/bin/sh

unzippedHistoryFile=$unzip_dir
unzippedHistoryFile+="history.txt"

for file in $SOURCE_DIR/*; do
  # echo $file;
  filename=$(basename "$file")
  fname="${filename%.*.*}"
  current_dst=$DESTINATION_DIR
  current_dst+=$fname
  [ ! -d "$dldir" ] && mkdir -p "$current_dst"
  isAlreadyExtracted=` grep -w $fname $unzippedHistoryFile `
  if [[ -z $isAlreadyExtracted ]]; then
    echo $fname >> $unzippedHistoryFile
    echo "Extracting the file"
    tar -xvf $file -C $current_dst
  fi
#  tar -xvf $file -C $current_dst
done
