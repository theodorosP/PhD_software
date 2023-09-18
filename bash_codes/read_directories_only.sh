#! /bin/bash

a=`ls -d */`
for i in $a
do
echo $i
cd $i
ls
cd ..
done
