#! /bin/bash


for i in 02_03 03_603 108_13 15_108 208_308 215_208 315_316 513_519 515_532 519_520 532_538 536_542 606_605
do
cp  Na_01_02.py  Na_$i.py
done


for i in 02_03 03_603 108_13 15_108 208_308 215_208 315_316 513_519 515_532 519_520 532_538 536_542 606_605
do
sed -i "s/NEB_Na_01_02.png/NEB_Na_$i.png/g" Na_$i.py
IS=$(echo "$i" | cut -d'_' -f1)
FS=$(echo "$i" | cut -d'_' -f2)
sed -i "s/CONF01/CONF$IS/g" Na_$i.py
sed -i "s/CONF02/CONF$FS/g" Na_$i.py
sed -i "s/NEB_01_02/NEB_${IS}_${FS}/g" Na_$i.py
done
