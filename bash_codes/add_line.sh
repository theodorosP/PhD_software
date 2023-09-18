#! /bin/bash

#write under line 8 
sed -i '8 a #SBATCH --partition=preemptable' job
#write under line 8 
sed -i '9 a #SBATCH --qos=preemptable' job
