#! /bin/bash

file=CHGDIFF.vasp
if [[ -f "$file" ]]; then
        printf "File: $file was found, move without compressing or decompressing \n"
else
        printf "File: $file NOT found \n"
	for i in CO2  NH4_CO2_Bi_111  NH4_Bi_111/CHARGE 
		do
		cd $i
		path=`pwd`
		echo Decompressing  $path/CHGCAR.gz
		gzip -d CHGCAR.gz
		python reduc.py
		echo Compressing  $path/CHGCAR.gz
		gzip CHGCAR
		cd ../
	done
cd ../
python chgdif.py
fi
