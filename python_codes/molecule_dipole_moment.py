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


def calculate_charge():
	#os.chdir(path)
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
		chg = round(ZVAL_dict[dataframe["symbols"][i]] -  dataframe["bader_charge"][i], 8)
		charge.append(chg)

	dataframe["charge"] = charge
	#oxygen_charge = dataframe["charge"][oxygen_atom[0]]
	#carbon_charge = dataframe["charge"][carbon_atom[0]]
	ZVAL = list()
	for i in range(0, len(dataframe)):
		zval = ZVAL_dict[dataframe["symbols"][i]]
		ZVAL.append(zval)

	dataframe["ZVAL"] = ZVAL
	print(dataframe.to_string())
	return dataframe

df = calculate_charge()

