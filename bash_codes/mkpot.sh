#! /bin/bash

atomlist=$(head -n 1 POSCAR)
rm -f POTCAR

echo 'What PP type do you need (LDA, PBE, PW91)?'

read var1

if  [ $var1 == 'LDA' ]
then
    pot='paw_LDA_CA.52'
elif [ $var1 == 'PBE' ]
then
    pot='paw_GGA_PBE.52'
elif [ $var1 == 'PW91' ]
then
    pot='paw_GGA_PW91'
fi

for atom in $atomlist
do
 cat /shared/vasp/$pot/$atom/POTCAR >> POTCAR
done

grep 'TIT' POTCAR
