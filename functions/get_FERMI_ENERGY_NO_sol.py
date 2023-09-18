def get_fermi_energy(path):
	os.chdir(path)
	word = "E-fermi"
	fermi_energy = ""
	with open("OUTCAR", "r") as file:
		for line_number, line in enumerate(file):
			if word in line:
				a = line
	b = a.replace(" E-fermi :  ", "")			
	for i in b:
		if i != " ":
			fermi_energy = fermi_energy + i
		else:
			break
	return float(fermi_energy)
