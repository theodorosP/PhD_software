#! /bin/bash

a=`ls -d */`
for i in $a
do
cd $i/OPT
NELECT_OUTCAR=`grep NELECT OUTCAR|tail -1|awk '{print $4}'`
CURRENT_PO=`grep "CURRENT PO" OUTCAR|tail -1|awk '{print $4}'`
TPOTVTARGET=`grep TPOTVTARGET INCAR|tail -1|awk '{print $3}'`
echo CURRENT POTENTIAL = $CURRENT_PO, TARGET_POTENTIAL = $TPOTVTARGET, NELECT = $NELECT_OUTCAR
cd ../../
done

