#! /bin/bash

shopt -s nullglob
logfiles=(*.log)
echo ${#logfiles[@]}
