#! /bin/bash

for i in  2 3
do
cd /u/trahman/data/theo/09272021/5_layers/2ML/1x1x1/system_$i
num=`ls -ltr|grep -c ^d`
num=$(($num+1))
mkdir $num
cp * $num
rm -rf slurm*
mv CONTCAR POSCAR
sbatch job
done
