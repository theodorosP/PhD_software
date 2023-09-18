import numpy as np
import pandas as pd
from ase.io.bader import attach_charges
from ase.visualize import view
from ase.io import read
from ase.io.bader import attach_charges


#This function gets the column names of a dataframe called df
def get_columns(df):
	columns = list()
	for i in range(0, len(df.columns)):
		columns.append(i)
	return columns




def get_ZVAL( outcar ):
	ZVAL = {}
	with open( outcar, 'r' ) as f:
		lines = f.readlines()
	for i in range( len( lines ) ):
		line = lines[ i ]
		if 'TITEL' in line:
			at = line.split()[ 3 ]
			for j in range( i, i + 10 ):
				line = lines[ j ]
				if 'ZVAL ' in line:
					zval_ = float( line.split()[ 5 ] )
					ZVAL[ at ] = zval_
	return ZVAL


def read_file_to_dataframe(file_to_read):
	dataframe = pd.read_csv(file_to_read,  sep = "\s+", skiprows = 2, header = None, skipinitialspace = True, skipfooter=4, engine = "python")
	return dataframe


struc = read("CONTCAR")


dataframe = read_file_to_dataframe("ACF.dat")


columns = get_columns(dataframe)
dataframe = dataframe.drop([columns[0]], axis = 1)
for i in range(1, 3):
	dataframe = dataframe.drop([columns[len(dataframe.columns)]], axis = 1)
dataframe.columns = ["X", "Y", "Z", "bader_charge"]

symbols = list()
for i in range(0, len(dataframe)):
	symbols.append(struc.get_chemical_symbols()[i])


dataframe["symbols"] = symbols
print(dataframe)

ZVAL_dict = get_ZVAL("OUTCAR")

charge = list()
for i in range(0, len(dataframe)):
	chg = round(ZVAL_dict[dataframe["symbols"][i]] -  dataframe["bader_charge"][i], 2)
	charge.append(chg)

dataframe["charge"] = charge

ZVAL = list()
for i in range(0, len(dataframe)):
	zval = ZVAL_dict[dataframe["symbols"][i]]
	ZVAL.append(zval)

dataframe["ZVAL"] = ZVAL

print(dataframe.to_string())

#atom_2 = oxygen atom
#atom_1 = the other atom
def force(atom1, atom2):
	kc = 14.3996/78.4
	d1 = np.array([dataframe["X"][atom2], dataframe["Y"][atom2], dataframe["Z"][atom2]]) - np.array([dataframe["X"][atom1], dataframe["Y"][atom1], dataframe["Z"][atom1]])
	#print(d1)
	d2 = d1**2
	#print(d2)
	d = d2[0] + d2[1] + d2[2]
	#print(d)
	q = dataframe["charge"][atom1] *  dataframe["charge"][atom2]
	#print(q)
	f = [kc * q/ d**(3/2)] * d1
	#print(f)
	return f

def magnitude(force_):
	mag = np.sqrt(force_[0]**2 + force_[1]**2 + force_[2]**2)
	return mag

final = force(218, 228) + force(219, 228) + force(220, 228) + force(221, 228) + force(226, 228)
print("force = ", final)
print("magnitude = ", magnitude(final))
#print(dataframe.to_string())
