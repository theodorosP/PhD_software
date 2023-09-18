#! /bin/bash

path=`pwd`

for i in 0.0 -0.5 -1.0 -1.2 -1.4 -1.5 -1.6 -1.8 -2.0
do
cd $path/FindChg_$i/target_potential
pwd
a=`ls -ltr|grep -c ^d`
num=$(echo "$a + 1"|bc)
mkdir $num
cp * $num
rm -rf slurm*
mv CONTCAR POSCAR
NELECT_OUTCAR=`grep "NELECT" OUTCAR|tail -1|awk '{print $4}'`
echo $NELECT_OUTCAR
NELECT_INCAR=`grep "NELECT =" INCAR|tail -1|awk '{print $3}'`
echo $NELECT_INCAR
sed -i "s/NELECT = $NELECT_INCAR/NELECT = $NELECT_OUTCAR/g" INCAR
done

