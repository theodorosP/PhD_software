import operator
from ase.io import read
import os

energy_dict = {}
for i in ["15", "08", "06", "17", "16", "09", "10", "18", "12", "21", "04"]:
	os.chdir("conf" + i)
	struc = read("OUTCAR")
	energy = struc.get_potential_energy()
	energy_dict[i] = energy
	os.chdir("../")


sorted_energy_dict = sorted(energy_dict.items(), key=operator.itemgetter(1),reverse=True)
print(sorted_energy_dict)

for i in range(0, len(sorted_energy_dict)):
	print(-sorted_energy_dict[0][1] + sorted_energy_dict[i][1], sorted_energy_dict[i][0])
