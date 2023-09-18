#This function deletes all atoms, their indexes are in the atoms_list
#struc is the POSCAR or CONTCAR
#atoms_list list with the indices of atoms we want to remove

def delete_atoms(struc, atoms_list):
	from ase.io import read
	for i in reversed(struc):#print(i.index)
		for j in range(0, len(atoms_list)):
			if i.index == atoms_list[j]:
				del struc[i.index]
	return struc

