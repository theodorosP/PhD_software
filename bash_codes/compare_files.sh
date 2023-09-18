#! /bin/bash

file_1="/u/trahman/data/theo/Bi/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-1.5/target_potential/POSCAR"
for i in $(seq 0 -0.5 -2.5)
do
file_2="/u/trahman/data/theo/Bi/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_$i/target_potential/1/POSCAR"
if [ ! -f "$file_2" ]; then
        file_2="/u/trahman/data/theo/Bi/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_$i/target_potential/POSCAR"
fi
if cmp -s $file_1 $file_2; then
        echo "$i-POSCAR same with -1.5-POSCAR"
else
        echo "$i-POSCAR different than -1.5-POSCAR"
fi
done

