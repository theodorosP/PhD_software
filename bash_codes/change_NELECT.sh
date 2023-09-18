#! /bin/bash

for i in side top
do
for j in `seq -2.5 0.5 0.0`
do
cd /home/theodoros/PROJ_ElectroCat/theodoros/addition_calcs_for_binding_energy/remove_CO2_$i/FindChg_$j/OPT
NELECT=`grep "NELECT =" INCAR|tail -1|awk '{print $3}'`
NELECT_UPDATED=$(echo "$NELECT - 32"|bc)
echo NELECT = $NELECT
echo NELECT_UPDATED = $NELECT_UPDATED
sed -i "s/NELECT = $NELECT/NELECT = $NELECT_UPDATED/g" INCAR
NELECT_new=`grep "NELECT =" INCAR|tail -1|awk '{print $3}'`
echo NELECT after update changed from NELECT = $NELECT to NELECT = $NELECT_new
done
done

