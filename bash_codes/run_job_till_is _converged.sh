#! /bin/bash

#source ~/.bashrc
alias  qstat='squeue -u `whoami`'

#function to repat a string
repeat_string()
{
    local string="$1"
    count=27
    for ((i = 0; i < $count; i++)); do
        echo -n "$string"
    done
    echo ""
}

#function to get the status of a job
get_job_status()
{
    job_name_line=$(sed -n '5p' job)
    job_name=$(echo "$job_name_line" | cut -d' ' -f3-)
    job_status=`qstat -n $job_name|awk '{print $4}'`
    echo $job_status
}


#function to check if job is completed
check_if_job_is_complete()
{
    find=`grep "General timing and accounting informations for this job:" OUTCAR`
    counter=NC #NC stands for not complete
    if [ -z "$find" ]
        then
            counter="NC"
        else
            counter="C" #C stands for complete
    fi
    echo $counter
}


#function to continue the already stopped potential
continue_target_potential()
{
	a=`ls -ltr|grep -c ^d`
	num=$(echo "$a + 1"|bc)
	mkdir $num
	cp * $num
	rm -rf slurm*
	mv CONTCAR POSCAR
	NELECT_OUTCAR=`grep "NELECTCURRENT" OUTCAR|tail -1|awk '{print $2}'`
	echo $NELECT_OUTCAR
	NELECT_INCAR=`grep "NELECT =" INCAR|tail -1|awk '{print $3}'`
	echo $NELECT_INCAR
	sed -i "s/NELECT = $NELECT_INCAR/NELECT = $NELECT_OUTCAR/g" INCAR
	sbatch job
}




CHECK_INTERVAL=15
while true;
do
	job_status=$(get_job_status)
	#a=$(check_if_job_is_complete)
	if [ "$job_status" == "ST" ] || [ "$job_status" == "ST CG" ]; then
		echo Job is: STOPPED, job_status = $job_status
		a=$(check_if_job_is_complete)
		if [ "$a" == "NC" ]; then
			echo Job is NOT completed yet, I need to run again
			continue_target_potential
		elif [ "$a" == "C" ]; then
			echo Job is COMPLETED exiting the loop
			break
		fi
	elif [ "$job_status" == "ST PD" ] || [ "$job_status" == "ST CG PD" ]; then
		echo The job is PENDING, I will check again, job_status = $job_status
	elif [ "$job_status" == "ST R" ] ||  [ "$job_status" == "R" ] || [ "$job_status" == "ST CG R" ]; then
		echo Job is RUNNING, I will check again, job_status = $job_status
	fi
	repeat_string "--"
	sleep "$CHECK_INTERVAL"
done

