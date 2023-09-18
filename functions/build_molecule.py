def add_atoms(system, symbol, x_pos, y_pos, z_pos):
	add_adsorbate(system, symbol, -1, position = (x_pos, y_pos), mol_index = 0 )
	system[len(system) - 1 ].position[2] = z_pos + 1	
	return system
