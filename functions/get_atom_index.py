def get_index(path_to_POSCAR, element, num, up_or_right):
	from ase.io import read
	struc = read(path_to_POSCAR + str("POSCAR"))
	if up_or_right == "UP":
		l = list() 
		for i in struc:
			pos = i.position
			if i.symbol == element and pos[1] > num:
				l.append(i.index)
	elif up_or_right == "RIGHT":
		l = list() 
		for i in struc:
			pos = i.position
			if i.symbol == element and pos[0] > num and pos[1] > 13.7 and pos[1] < 17.8:
				l.append(i.index)
	return l
