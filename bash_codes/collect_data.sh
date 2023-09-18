#! /bin/bash
FILE='DATA.dat'
for i in `seq 5.5 .01 5.85`
   do
       TOTAL_ENERGY="$(grep 'energy  w' A-$i/OUTCAR|awk '{print $4}')"
       LAT_CONST=$i
       echo "$i  $TOTAL_ENERGY" >> $FILE
#	sed -i 's/s//' $FILE
   done
