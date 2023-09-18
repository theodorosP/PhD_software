#! /bin/bash

a=`ls -d */`
for i in $a
do
cd $i
for i in $a find -type f -name "*.png" find -type f -name "*.pov" 
do
rm -rf $i
done
cd ../
done


