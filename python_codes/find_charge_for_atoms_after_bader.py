import numpy as np
import pandas as pd
from ase.io.bader import attach_charges
from ase.visualize import view
from ase.io import read
from ase.io.bader import attach_charges

#This function returns the index of atom with distance less than cut_off, from a specific_atom(reference_atom)
#struc = POSCAR or CONTCAR file
#cut_off = the maximum distance from a specific atom. i.e. if we want to find all atoms which are 4 A away from a specific atom then cut_off = 4
#reference_atom = the atom from which we count distances. i.e. If we want to find the atom indices of atoms some A apart from atom number 10, then reference_atom = 10
def get_close_atoms(struc, cut_off, reference_atom):
	l_index_close = list()
	pos_ref = struc[reference_atom].position
	for i in struc:
		pos = i.position
		dist2 = (pos[0] - pos_ref[0])**2 + (pos[1] - pos_ref[1])**2 + (pos[2] - pos_ref[2])**2
		dist = np.sqrt(dist2)
		if dist < cut_off and i.symbol == "Bi":
			l_index_close.append(i.index)
	return(l_index_close)
		
#This function gets the number of atoms in some layers
#struc = POSCAR or CONTCAR
#z = the z cordinate
#atom = the type of atom
def get_layer_atoms(struc, z, atom):
	layer_atoms = list()
	for i in struc:
		pos = i.position
		if i.symbol == atom and pos[2] > z:
			layer_atoms.append(i.index)
	return (layer_atoms)

#This function gets the type of atom species in our system
#struc = The POSCAR or CONTCAR file
def get_atomic_species(struc):
	elements_list = list()
	elements = list()
	for i in struc:
		 elements_list.append(i.symbol)
	res = set(elements_list)
	for j in res:
		elements.append(j)
	return elements


#This function gets the indices of all atoms in dictionary
#struc = POSCAR or CONTCAR file
def get_atomic_indices_in_dict(struc):
	d = {}
	atoms = get_atomic_species(struc)
	for i in struc:
		for j in atoms:	
			if i.symbol == j:
				if j in d:
					d[j].append(i.index)
				else:
					d[j] = [i.index]
	return d

#This function gets the column names of a dataframe called df
def get_columns(df):
	columns = list()
	for i in range(0, len(df.columns)):
		columns.append(i)
	return columns


#This function rounds the numbers in a list called l.
#l is the list with the numbers
#a is the decimal we want to round
#It returns a list with the rounded numbers
def round_list(l, a):
	rounded_list = list()
	for i in l:
		rounded_list.append(round(i, a))
	return rounded_list

#This function adds a list as a column to a dataframe
#df = the existing dataframe with our data
#list_ = the list we want to add as column
#name_of_the_column = the name we want the bew column to have
#Bi starts after 6 index, this may varay in other codes
def add_list_to_dataframe(df, list_, name_of_column):
	df[name_of_column] = np.NAN
	for i in range(0, len(list_)):
		df.loc[i + 6, name_of_column] = list_[i]
	return df	


#This function makes a dataframe with the charges of each atom in a list.
#list_of_atoms = The index of atoms we want to calculate their charge
#ZVAL =  read it from the POTCAR or OUTCAR file. Alternatively, it's the number of valence electrons and can be found online
#df_ACF = the ACF.dat file read in a dataframe
def atoms(list_of_atoms, ZVAL, df_ACF, species):
	decimal_to_round = 2
	df = pd.DataFrame()
	df["atom number"] = list_of_atoms
	df["species"] = species
	total_charge = [ZVAL - df_ACF["charge"][i] for i in list_of_atoms]
	total_charge_rounded = round_list(total_charge, decimal_to_round)
	df["total_charge"] = total_charge_rounded
	return df


#This function makes a dictionary with keys: final_ + type_of_atom. The values are dataframes, which have columns: "atom number", "species", "total charge"
#struc = POSCAR or CONTCAR file
#df_ACF_dat = the ACF.dat file in read as DataFrame
#atomic_species = a list with the type of atoms, i.e. ["O", "Bi", "N", "C", "H"]
#index_dict = a dictionary with atom indices
def at_dictionary(struc, df_ACF_dat, atomic_species, index_dict):
	atomic_dictionary = {}
	for i in range(0, len(atomic_species)):
		if atomic_species[i] == "O":
			ZVAL = 6
			atomic_list = index_dict["O"]
		elif atomic_species[i] == "Bi":
			ZVAL = 5
			atomic_list = index_dict["Bi"]
		elif atomic_species[i] == "N":
			ZVAL = 5
			atomic_list = index_dict["N"]
		elif atomic_species[i] == "C":
			ZVAL = 4
			atomic_list = index_dict["C"]
		elif atomic_species[i] == "H":
			ZVAL = 1
			atomic_list = index_dict["H"]
		atomic_dictionary["final_" + atomic_species[i]] = atoms(atomic_list, ZVAL, df_ACF_dat, atomic_species[i]) 
	return atomic_dictionary

#This function get's the atoms in the first n layers, and imports it's indices and charges to the final dataframe
#struc = POSCAR or CONTCAR file
#df_ACF_dat = the ACF.dat file in DataFrame form
#df_final = the final dataframe
#atom = the type of atom we have in the n layers, i.e. "Bi", please give only one, it's string
#z_cut_off = the z cordinate above which we want to get the atoms
#column_name = the n_first_layers, i.e first_layer, or first_second_layer, or first_second_third_layer, it's a string
def get_layer_atoms_and_import_to_dataframe(struc, df_ACF_dat, df_final, atom, z_cut_off, column_name):
	layer =  get_layer_atoms(struc, z_cut_off, "Bi")
	add_list_to_dataframe(df_final, layer, column_name + "_atoms")
	index_dict = {atom : layer}
	dictionary_layer = at_dictionary(struc, df_ACF_dat, [atom], index_dict)
	df_final[column_name + "_charge"] = np.NAN
	for i in range(0, len(dictionary_layer["final_" + atom] )):
		df_final.loc[i + 6, column_name +  "_charge"] = dictionary_layer["final_" + atom]["total_charge"][i]
	return df_final

#This function get's the atoms the closest atoms to reference atom, and imports it's indices and charges to the final dataframe
#struc = POSCAR or CONTCAR file
#df_ACF_dat = the ACF.dat file in DataFrame form
#df_final = the final dataframe
#ref_atom = the atom from which we count distances. i.e. If we want to find the atom indices of atoms some A apart from atom number 10, then reference_atom = 10
#atom = the type of atom we have in the n layers, i.e. "Bi", please give only one, it's string
#cut_off = the maximum distance from a specific atom. i.e. if we want to find all atoms which are 4 A away from a specific atom then cut_off = 4
#column_name = the n_first_layers, i.e first_layer, or first_second_layer, or first_second_third_layer, it's a string
def get_close_atoms_and_import_to_dataframe(struc, df_ACF_dat, df_final, ref_atom, atom,  column_name, cut_off):
    layer = get_close_atoms(struc, cut_off, ref_atom)
    add_list_to_dataframe(df_final, layer, column_name + "_atoms")
    index_dict = {atom : layer}
    dictionary_layer = at_dictionary(struc, df_ACF_dat, [atom], index_dict)
    df_final[column_name + "_charge"] = np.NAN
    for i in range(0, len(dictionary_layer["final_" + atom] )):
        df_final.loc[i + 6, column_name +  "_charge"] = dictionary_layer["final_" + atom]["total_charge"][i]
    return df_final

#This functions gets the ZVAL from outcar file
#outcar = OUTCAR 
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

loc = "./"
struc = read("CONTCAR")

ZVAL = get_ZVAL( loc + 'OUTCAR' )
system = read( loc + 'POSCAR' )
attach_charges( system, loc + 'ACF.dat' )
for at in system:
	at.charge = round(- at.charge  +  ZVAL[ at.symbol ], 2)


dataframe = pd.read_csv("ACF.dat",  sep=" ", skiprows = 2, header = None, skipinitialspace = True, skipfooter=4, engine = "python")


columns = get_columns(dataframe)
dataframe = dataframe.drop([columns[0]], axis = 1)
dataframe.columns = ["charge" if x == columns[4] else x for x in dataframe.columns]


atomic_species = get_atomic_species(struc)
index_dict = get_atomic_indices_in_dict(struc)
atomic_dictionary = at_dictionary(struc, dataframe, atomic_species, index_dict)
keys = atomic_dictionary.keys()



df_final = atomic_dictionary[keys[0]]
for i in range(len(keys) -1, 0, -1):
	aux = pd.concat([df_final, atomic_dictionary[keys[i]]], axis = 0)
	df_final = aux

df_final = df_final.reset_index(drop=True)


get_layer_atoms_and_import_to_dataframe(struc, dataframe, df_final, "Bi", 22, "first_layer")
get_layer_atoms_and_import_to_dataframe(struc, dataframe, df_final, "Bi", 20, "first_second_layer")


cut_off = 6
ref_atom = 235
#close_atoms_index = get_close_atoms(struc, cut_off, atom)
#add_list_to_dataframe(df_final, close_atoms_index, "close_atoms")


def get_close_atoms_and_import_to_dataframe(struc, df_ACF_dat, df_final, ref_atom, atom,  column_name, cut_off):
	layer = get_close_atoms(struc, cut_off, ref_atom)
	add_list_to_dataframe(df_final, layer, column_name + "_atoms")
	index_dict = {atom : layer}
	dictionary_layer = at_dictionary(struc, df_ACF_dat, [atom], index_dict)
	df_final[column_name + "_charge"] = np.NAN
	for i in range(0, len(dictionary_layer["final_" + atom] )):
		df_final.loc[i + 6, column_name +  "_charge"] = dictionary_layer["final_" + atom]["total_charge"][i]
	return df_final


get_close_atoms_and_import_to_dataframe(struc, dataframe, df_final, ref_atom,  "Bi", "close_atoms", cut_off)

#print(df_final)


#view(system)


s_bi = 0
for i in range(6, 222):
    s_bi = s_bi + df_final["total_charge"][i]

s_co2 = df_final["total_charge"][3] + df_final["total_charge"][5] + df_final["total_charge"][236]
s_ch3nh3 = df_final["total_charge"][226] + df_final["total_charge"][227] + df_final["total_charge"][228] + df_final["total_charge"][229] + df_final["total_charge"][230] + df_final["total_charge"][231]

with open ("data.txt", "w") as file:
	file.write(str(s_bi) + "	" + str(s_co2) + "	" + str(s_ch3nh3))
