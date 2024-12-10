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

search_pairs "224 199" "223 214" "220 210" "222 202"
