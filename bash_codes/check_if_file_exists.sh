#! /bin/bash

#using printf
for i in {1..5}
do
cd /u/trahman/data/theo/Pb_Ge_111/break_symmetry/2ML/3x3x1/system_$i
file=out
if [[ -f "$file" ]]; then
        printf "2ML 3x3x1 $file exists \n"
else
        printf "2ML-1 3x3x1 $file is not found \n"
fi
done


printf "%0.s-" {1..25}
printf "\n"


#using echo
for i in {1..5}
do
cd /u/trahman/data/theo/Pb_Ge_111/break_symmetry/2ML-1/3x3x1/system_$i
file=out
if [[ -f "$file" ]]; then
        echo "2ML-1 3x3x1 $file exists"
else
        echo "2ML-1 3x3x1 $file does not exist"
fi
done
