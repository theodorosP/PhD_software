#! /bin/bash

path=`pwd`
for i in -2.5 -2.0 -1.8 -1.6 -1.5 -1.4 -1.2 -1.0 -0.5 0.0
do
    cd $path/FindChg_$i/target_potential
    find=`grep "General timing and accounting informations for this job:" OUTCAR`
    if [ -z "$find" ]
    then
        echo job not COMPLETE, folder: FindChg_$i/target_potential
    else
        echo job is COMPLETE FindChg_$i/target_potential
    fi
done


