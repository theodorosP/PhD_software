from dlePy.vasp.getdata import get_energy
import os

all_subdirs_1 = [d for d in os.listdir('.') if os.path.isdir(d)]


for i in all_subdirs_1:
        os.chdir(i)
        all_subdirs_2 = [d for d in os.listdir('.') if os.path.isdir(d)]
        for j in all_subdirs_2:
                os.chdir(j)
                os.chdir("target_potential")
                #os.system("pwd")
                print("--" * 20)
                os.system("pwd")
                energy = get_energy("OUTCAR")
                print("--" * 20)
                #print(energy)
                os.chdir("../../")
        os.chdir("../")
