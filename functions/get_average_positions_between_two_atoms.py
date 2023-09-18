#struc = the structure 
#atom1 = integer number, it is the index of the first atom
#atom2 = integer number, it is the index of the second atom
def get_average_positions(struc, atom1, atom2):
  import numpy as np
	cordinates = ["x", "y", "z"]
	average_positions = {}
	for i in range(0, 3):
		average_positions[str(cordinates[i])] = (struc[atom1].position[i] + struc[atom2].position[i])/2
	keys = list(average_positions.keys())
	average_cordinates = np.array([average_positions[keys[0]],average_positions[keys[1]] ,average_positions[keys[2]] ])
	return average_cordinates
