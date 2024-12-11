#!/bin/bash

search_pairs() {
  local pairs=("$@")
  local pattern=""
  for pair in "${pairs[@]}"; do
    set -- $pair
    pattern+="(${1}.*${2}|${2}.*${1})|"
  done
  pattern=${pattern%|}
  local dirs=$(ls -d */ | sort -V)
  for dir in $dirs; do
    cd "$dir"
    local var=$(grep -E "$pattern" ICONST)
    if [[ -n "$var" ]]; then
      pwd
      echo "$var"
    fi
    cd ../
  done
}

dirs=$(ls -d */)
for i in $dirs
do
	cd $i
	echo -e "\e[43m$i\e[0m"
	search_pairs "83 125" "76 146" "101 180" "189 188"
	cd ../
	done
