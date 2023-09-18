def change_position(system, atom, x, y, z):
	l = [x, y, z]
	for i in range(0, len(l)):
		system[atom].position[i] = l[i]
	return system
