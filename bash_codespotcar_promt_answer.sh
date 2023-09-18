! /bin/bash

for i in `seq -2.5 0.5 0`
do
cd /home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/Bi_CO2_remove_NH4_top/FindChg_$i/tmp
pwd
echo "PBE"| mkpot
cd /home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/Bi_CO2_remove_NH4_side/FindChg_$i/tmp
pwd
echo "PBE"| mkpot
done
