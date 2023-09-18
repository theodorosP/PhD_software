import numpy as np
import pandas as pd
from ase.io.bader import attach_charges
from ase.visualize import view
from ase.io import read
from ase.io.bader import attach_charges
import os

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


#atom_2 = oxygen atom
#atom_1 = the other atom
def force(atom1, atom2, df):
	kc = 14.3996/78.4
	d1 = np.array([df["X"][atom2], df["Y"][atom2], df["Z"][atom2]]) - np.array([df["X"][atom1], df["Y"][atom1], df["Z"][atom1]])
	d2 = d1**2
	d = d2[0] + d2[1] + d2[2]
	q = df["charge"][atom1] *  df["charge"][atom2]
	f = [kc * q/ d**(3/2)] * d1
	return f

def magnitude(force_):
	mag = np.sqrt(force_[0]**2 + force_[1]**2 + force_[2]**2)
	return mag

def calculate_force(path, oxygen_atom, other_atoms, carbon_atom, bismuth_atom):
	os.chdir(path)
	struc = read("CONTCAR")
	dataframe = read_file_to_dataframe("ACF.dat")
	columns = get_columns(dataframe)
	dataframe = dataframe.drop([columns[0]], axis = 1)
#	print(dataframe.to_string())
	for i in range(1, 3):
		dataframe = dataframe.drop([columns[len(dataframe.columns)]], axis = 1)
	dataframe.columns = ["X", "Y", "Z", "bader_charge"]
	symbols = list()
	for i in range(0, len(dataframe)):
		symbols.append(struc.get_chemical_symbols()[i])
	dataframe["symbols"] = symbols
	ZVAL_dict = get_ZVAL("OUTCAR")

	charge = list()
	for i in range(0, len(dataframe)):
 		chg = round(ZVAL_dict[dataframe["symbols"][i]] -  dataframe["bader_charge"][i], 3)
		charge.append(chg)

	dataframe["charge"] = charge
	oxygen_charge = dataframe["charge"][oxygen_atom[0]]
	carbon_charge = dataframe["charge"][carbon_atom[0]]
	ZVAL = list()
	for i in range(0, len(dataframe)):
		zval = ZVAL_dict[dataframe["symbols"][i]]
		ZVAL.append(zval)

	dataframe["ZVAL"] = ZVAL
	final = 0
	for i in other_atoms:
		final += force(i, oxygen_atom[0], dataframe)
	return magnitude(final), oxygen_charge, carbon_charge

	#print("Configuration: ", conf +  " force on Oxygen from cation", final)
	#print("Configuration: ", conf +  " force magnitude on Oxygen from cation", magnitude(final))
	#print("Configuration: ", conf +  " force magnitude on Carbon atom from Bismuth ", magnitude(force(carbon_atom[0], bismuth_atom[0], dataframe)))

NH4_top_1, O_NH4_top_1, C_NH4_top_1 = calculate_force("/u/trahman/data/theo/Bi/forces/NH4/NH4_top/FindChg_-1.8", [228], [218, 219, 220, 221, 226], [216], [36])
NH4_top_2, O_NH4_top_2, C_NH4_top_2 = calculate_force("/u/trahman/data/theo/Bi/forces/NH4/NH4_top/FindChg_-1.8", [229], [218, 219, 220, 221, 226], [216], [36])
NH4_side_1, O_NH4_side_1, C_NH4_side_1 = calculate_force("/u/trahman/data/theo/Bi/forces/NH4/NH4_side/FindChg_-1.8", [229], [218, 219, 220, 221, 226], [217] , [121])
NH4_side_2, O_NH4_side_2, C_NH4_side_2, = calculate_force("/u/trahman/data/theo/Bi/forces/NH4/NH4_side/FindChg_-1.8", [228], [218, 219, 220, 221, 226], [217] , [121])
CH3NH3_top_1, O_CH3NH3_top_1, C_CH3NH3_top_1 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_top/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_top_2, O_CH3NH3_top_2, C_CH3NH3_top_2 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_top/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_side_1, O_CH3NH3_side_1, C_CH3NH3_side_1 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_side/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_side_2, O_CH3NH3_side_2, C_CH3NH3_side_2 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_side/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_reversed_1, O_CH3NH3_reversed_1, C_CH3NH3_reversed_1 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_reversed/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_reversed_2, O_CH3NH3_reversed_2, C_CH3NH3_reversed_2 = calculate_force("/u/trahman/data/theo/Bi/forces/CH3NH3/CH3NH3_reversed/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
Na_top_1, O_Na_top_1, C_Na_top_1 = calculate_force("/u/trahman/data/theo/Bi/forces/Na/Na_top/FindChg_-1.8", [222], [218], [217] , [36])
Na_top_2, O_Na_top_2, C_Na_top_2 = calculate_force("/u/trahman/data/theo/Bi/forces/Na/Na_top/FindChg_-1.8", [220], [218], [217] , [36])
Na_side_1, O_Na_side_1, C_Na_side_1 = calculate_force("/u/trahman/data/theo/Bi/forces/Na/Na_side/FindChg_-1.8", [220], [218], [216] , [121])
Na_side_2, O_Na_side_2, C_Na_side_2 = calculate_force("/u/trahman/data/theo/Bi/forces/Na/Na_side/FindChg_-1.8", [222], [218], [216] , [121])



force_O1 = list()
force_O2 = list()
charge_O = list()
charge_C = list()
charge_CO2 = list()
systems = ["NH4_top",  "NH4_side", "CH3NH3_top", "CH3NH3_side", "CH3NH3_reversed", "Na_top", "Na_side"]

for i in [NH4_top_1, NH4_side_1, CH3NH3_top_1, CH3NH3_side_1, CH3NH3_reversed_1, Na_top_1, Na_side_1]:
	force_O1.append(i)


for i in [NH4_top_2, NH4_side_2, CH3NH3_top_2, CH3NH3_side_2, CH3NH3_reversed_2, Na_top_2, Na_side_2]:
    force_O2.append(i)


O_NH4_top = O_NH4_top_1 + O_NH4_top_2
O_NH4_side = O_NH4_side_1 + O_NH4_side_2 
O_CH3NH3_top = O_CH3NH3_top_1 + O_CH3NH3_top_2
O_CH3NH3_side = O_CH3NH3_side_1 + O_CH3NH3_side_2
O_CH3NH3_reversed = O_CH3NH3_reversed_1 + O_CH3NH3_reversed_2
O_Na_top = O_Na_top_1 + O_Na_top_2
O_Na_side = O_Na_side_1 + O_Na_side_2


for i in [O_NH4_top, O_NH4_side, O_CH3NH3_top, O_CH3NH3_side, O_CH3NH3_reversed, O_Na_top, O_Na_side]:
    charge_O.append(i)

for i in [C_NH4_top_1, C_NH4_side_1, C_CH3NH3_top_1, C_CH3NH3_side_1, C_CH3NH3_reversed_1, C_Na_top_1, C_Na_side_1]:
    charge_C.append(i)

for i in range(0, len( [O_NH4_top, O_NH4_side, O_CH3NH3_top, O_CH3NH3_side, O_CH3NH3_reversed, O_Na_top, O_Na_side])):
	charge_CO2.append(charge_O[i] + charge_C[i] )


BE = [-0.017598, 0.018123, -0.021773, 0.012819, -0.009439, 0.287321, 0.080832]
CO2_charge_initially = list()
for i in range(1, 8):
	CO2_charge_initially.append(16)

df = pd.DataFrame()
df["system"] = systems
df["oxygen 1 (eV/A)"] = force_O1
df["oxygen 2 (eV/A)"] = force_O2
df["CO2 BE (eV)"] = BE
#df["I CO2 charge (e)"] = CO2_charge_initially
df["CO2 charge"] = charge_CO2

#df.set_index('system', inplace=True)
print(df)
