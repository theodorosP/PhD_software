#This function moves a molecule symmetrically on the surface
#system =  the POSCAR or CONTCAR file
#at = the index of an atom of the molecule we want to move.All other atoms will be moved in repsect to this atom
#layer_atom = the index of the atom above of which the at atom will be moved
#atoms to move = a list with the atoms we want to move
def move_symmetrically(system, at, layer_atom, atoms_to_move ):
	from ase.visualize import view
	x_i = system[at].position[0]
	y_i = system[at].position[1]
	for i in range(0, 2):
		system[at].position[i] = system[layer_atom].position[i]
	moving_atoms = [i for i in atoms_to_move if i != at]
	for i in moving_atoms:
  		system[i].position[0] += system[at].position[0] - x_i
  		system[i].position[1] += system[at].position[1] - y_i
	view(system)	
	return system
