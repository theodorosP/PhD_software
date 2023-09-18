import os
import sys

for i in range(1, 11):
	os.chdir("new_" + str(i))
	os.system("sbatch " + "job")
	os.chdir("../")
