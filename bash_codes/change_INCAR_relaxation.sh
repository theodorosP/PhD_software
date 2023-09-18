#! /bin/bash


for i in -2.5 -2.0 -1.8 -1.6 -1.5 -1.4 -1.2 -1.0 -0.5 0.0
do
cd FindChg_$i/OPT
NELECT_OUTCAR=`grep "NELECT " OUTCAR|tail -1|awk '{print $4}'`
cd ../target_potential
NELECT_INCAR=`grep "NELECT = " INCAR|tail -1|awk '{print $3}'`
sed -i "s/NELECT = $NELECT_INCAR/NELECT = $NELECT_OUTCAR/g" INCAR
NELECT_INCAR_UPDATED=`grep "NELECT = " INCAR|tail -1|awk '{print $3}'`
echo NELECT changed from NELECT = $NELECT_INCAR to NELECT = $NELECT_INCAR_UPDATED file: FindChg_$i/target_potential
cd ../../
done

for i in -2.5 -2.0 -1.8 -1.6 -1.5 -1.4 -1.2 -1.0 -0.5 0.0
do
cd FindChg_$i/target_potential
TPOTVTARGET_INCAR=`grep "TPOTVTARGET" INCAR|awk '{print $3}'`
TPOTVTARGET_NEW=$(echo "4.43 + $i"|bc)
sed -i "s/TPOTVTARGET = $TPOTVTARGET_INCAR/TPOTVTARGET = $TPOTVTARGET_NEW/g" INCAR
TPOTVTARGET_UPDATED=`grep "TPOTVTARGET" INCAR|awk '{print $3}'`
echo TPOTVTARGET changed from TPOTVTARGET = $TPOTVTARGET_INCAR to TPOTVTARGET = $TPOTVTARGET_UPDATED file: FindChg_$i/target_potential 
cd ../../
done

for i in -2.5 -2.0 -1.8 -1.6 -1.5 -1.4 -1.2 -1.0 -0.5 0.0
do
cd FindChg_$i/target_potential
TPOTELECTSTEP_INCAR=`grep "TPOTELECTSTEP =" INCAR|tail -1|awk '{print $3}'`
sed -i "s/TPOTELECTSTEP = $TPOTELECTSTEP_INCAR/TPOTELECTSTEP = 0.05/g" INCAR
TPOTELECTSTEP_UPDATED=`grep "TPOTELECTSTEP =" INCAR|tail -1|awk '{print $3}'`
echo TPOTELECTSTEP changed from TPOTELECTSTEP = $TPOTELECTSTEP_INCAR to TPOTELECTSTEP = $TPOTELECTSTEP_UPDATED file: FindChg_$i/target_potential 
cd ../../
done
