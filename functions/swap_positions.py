def swap_atoms(system, atom1, atom2):
	aux = list()
	for i in range(0, 3):
		aux.append(system[atom1].position[i])
		system[atom1].position[i] = system[atom2].position[i]
		system[atom2].position[i] = aux[i]
	return system
