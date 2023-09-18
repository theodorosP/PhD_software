#! /bin/bash

gotojob ()
{
jobid=$1
cd `scontrol show jobid -dd $jobid | grep WorkDir | sed 's/WorkDir=//'`
}

