
def get_NELECT():
	word = "UPDATED NELECT"
	with open("OUTCAR", "r") as file:
        	for line_number, line in enumerate(file):
                	if word in line:
                        	a = line

	b = re.sub("UPDATED NELECT      =", "", a)
	c = re.sub("electrons", "", b)
	d = float(c)
	#print("Current NELECT = ", d, " electrons")
	return d

