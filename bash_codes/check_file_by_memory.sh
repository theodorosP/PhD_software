#! /bin/bash

for i in NH4_top NH4_side  NH4_CO2_linear
do
for j in $list
do
cd /u/trahman/data/theo/Bi/0.1M/charge_density_difference/$i/FindChg_$j/NH4_Bi_111/CHARGE
memory=`du -h CHGCAR|awk '{print $1}'`
mem="${memory//G}"
echo memory = $mem
path=`pwd`
if [ $mem = 0 ]; then
        echo CHGCAR DOES NOT exist, path: $path
else
       echo working in path: $path
        rm -rf CHG CHG.gz CHG.zip
        gzip CHGCAR
fi
done
done
