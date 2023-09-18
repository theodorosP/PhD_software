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
		chg = round(ZVAL_dict[dataframe["symbols"][i]] -  dataframe["bader_charge"][i], 8)
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



def get_angles_C_O_C(system, c1, o, c2, top_bi, volt):
	angles = list()
	distance = list()
	distance_aux = list()
	for i in volt:
		print("Reading system FindChg_" + str(i) +"/CONTCAR")
		struc =  read("~/PROJ_ElectroCat/theodoros/forces/" + system + "/FindChg_" + str(i) + "/CONTCAR" )
		print("System FindChg_" + str(i) + "/CONTCAR ready")
		angle = struc.get_angle(c1, o, c2, mic = False)
		#angles.append(angle)
		dist = struc.get_distances(o, [top_bi], mic=True, vector=False)
		distance_aux.append(dist.tolist())
	#for i in distance_aux:
	#	for j in i:
#			distance.append(j)
	return angle, dist[0]

voltage = [-1.8]


angles_NH4_top =  get_angles_C_O_C("NH4/NH4_top", 228, 216, 229, 36, voltage)[0]
distance_NH4_top =  get_angles_C_O_C("NH4/NH4_top", 228, 216, 229, 36, voltage)[1]

angles_NH4_side =  get_angles_C_O_C("NH4/NH4_side", 228, 217, 229, 121, voltage)[0]
distance_NH4_side =  get_angles_C_O_C("NH4/NH4_side", 228, 217, 229, 121, voltage)[1]


angles_CH3NH3_top =  get_angles_C_O_C("CH3NH3/CH3NH3_top", 236, 218, 237, 36, voltage)[0]
distance_CH3NH3_top =  get_angles_C_O_C("CH3NH3/CH3NH3_top", 236, 218, 237, 36, voltage)[1]

angles_CH3NH3_side =  get_angles_C_O_C("CH3NH3/CH3NH3_side", 236, 218, 237, 36, voltage )[0]
distance_CH3NH3_side =  get_angles_C_O_C("CH3NH3/CH3NH3_side", 236, 218, 237, 36, voltage )[1]

angles_CH3NH3_reversed =  get_angles_C_O_C("CH3NH3/CH3NH3_reversed", 236, 218, 237, 36, voltage)[0]
distance_CH3NH3_reversed =  get_angles_C_O_C("CH3NH3/CH3NH3_reversed", 236, 218, 237, 36, voltage)[1]

angles_Na_top =  get_angles_C_O_C("Na/Na_top", 222, 217, 220, 36, voltage)[0]
distance_Na_top =  get_angles_C_O_C("Na/Na_top", 222, 217, 220, 36, voltage)[1]

angles_Na_side =  get_angles_C_O_C("Na/Na_side", 222, 216, 220, 121, voltage)[0]
distance_Na_side =  get_angles_C_O_C("Na/Na_side", 222, 216, 220, 121, voltage)[1]

angles_CH3_4N_top =  get_angles_C_O_C("CH3_4N/CH3_4N_top", 254, 218, 255, 118, voltage)[0]
distance_CH3_4N_top =  get_angles_C_O_C("CH3_4N/CH3_4N_top", 254, 218, 255, 118, voltage)[1]

angles_CH3_4N_side =  get_angles_C_O_C("CH3_4N/CH3_4N_side", 254, 220, 255, 39, voltage)[0]
distance_CH3_4N_side =  get_angles_C_O_C("CH3_4N/CH3_4N_side", 254, 220, 255, 39, voltage)[1]




NH4_top_1, O_NH4_top_1, C_NH4_top_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/NH4/NH4_top/FindChg_-1.8", [228], [218, 219, 220, 221, 226], [216], [36])
NH4_top_2, O_NH4_top_2, C_NH4_top_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/NH4/NH4_top/FindChg_-1.8", [229], [218, 219, 220, 221, 226], [216], [36])
NH4_side_1, O_NH4_side_1, C_NH4_side_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/NH4/NH4_side/FindChg_-1.8", [229], [218, 219, 220, 221, 226], [217] , [121])
NH4_side_2, O_NH4_side_2, C_NH4_side_2, = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/NH4/NH4_side/FindChg_-1.8", [228], [218, 219, 220, 221, 226], [217] , [121])
CH3NH3_top_1, O_CH3NH3_top_1, C_CH3NH3_top_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_top/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_top_2, O_CH3NH3_top_2, C_CH3NH3_top_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_top/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_side_1, O_CH3NH3_side_1, C_CH3NH3_side_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_side/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_side_2, O_CH3NH3_side_2, C_CH3NH3_side_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_side/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_reversed_1, O_CH3NH3_reversed_1, C_CH3NH3_reversed_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_reversed/FindChg_-1.8", [237], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
CH3NH3_reversed_2, O_CH3NH3_reversed_2, C_CH3NH3_reversed_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3NH3/CH3NH3_reversed/FindChg_-1.8", [236], [216, 223, 224, 225, 231, 227, 221, 233], [218] , [36])
Na_top_1, O_Na_top_1, C_Na_top_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/Na/Na_top/FindChg_-1.8", [222], [218], [217] , [36])
Na_top_2, O_Na_top_2, C_Na_top_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/Na/Na_top/FindChg_-1.8", [220], [218], [217] , [36])
Na_side_1, O_Na_side_1, C_Na_side_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/Na/Na_side/FindChg_-1.8", [220], [218], [216] , [121])
Na_side_2, O_Na_side_2, C_Na_side_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/Na/Na_side/FindChg_-1.8", [222], [218], [216] , [121])
CH3_4N_top_1, O_CH3_4N_top_1, C_CH3_4N_top_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3_4N/CH3_4N_top/FindChg_-1.8", [254], [241, 226, 237, 234, 239, 230, 235, 229, 236, 232, 231, 233], [218] , [118])
CH3_4N_top_2, O_CH3_4N_top_2, C_CH3_4N_top_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3_4N/CH3_4N_top/FindChg_-1.8", [255], [241, 226, 237, 234, 239, 230, 235, 229, 236, 232, 231, 233], [218] , [118])
CH3_4N_side_1, O_CH3_4N_side_1, C_CH3_4N_side_1 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3_4N/CH3_4N_side/FindChg_-1.8", [254], [241, 226, 237, 234, 239, 230, 235, 229, 236, 232, 231, 233], [218] , [118])
CH3_4N_side_2, O_CH3_4N_side_2, C_CH3_4N_side_2 = calculate_force("/home/theodoros/PROJ_ElectroCat/theodoros/forces/CH3_4N/CH3_4N_side/FindChg_-1.8", [255], [241, 226, 237, 234, 239, 230, 235, 229, 236, 232, 231, 233], [218] , [118])


force_O1 = list()
force_O2 = list()
charge_O = list()
charge_C = list()
charge_CO2 = list()
systems = ["$NH_{4}^{+(1)}$",  "$NH_{4}^{+(2)}$", "$CH_{3}NH_{3}^{+(1)}$", "$CH_{3}NH_{3}^{+(2)}$", "$CH_{3}NH_{3}^{+(3)}$", "$Na^{+(1)}$", "$Na^{+(2)}$", "$(CH_{3})_{4}N^{+(1)}$", "$(CH_{3})_{4}N^{+(1)}$"]
systems_plot = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

for i in [NH4_top_1, NH4_side_1, CH3NH3_top_1, CH3NH3_side_1, CH3NH3_reversed_1, Na_top_1, Na_side_1, CH3_4N_top_1, CH3_4N_side_1]:
	force_O1.append(i)


for i in [NH4_top_2, NH4_side_2, CH3NH3_top_2, CH3NH3_side_2, CH3NH3_reversed_2, Na_top_2, Na_side_2, CH3_4N_top_2, CH3_4N_side_2]:
    force_O2.append(i)


O_NH4_top = O_NH4_top_1 + O_NH4_top_2
O_NH4_side = O_NH4_side_1 + O_NH4_side_2 
O_CH3NH3_top = O_CH3NH3_top_1 + O_CH3NH3_top_2
O_CH3NH3_side = O_CH3NH3_side_1 + O_CH3NH3_side_2
O_CH3NH3_reversed = O_CH3NH3_reversed_1 + O_CH3NH3_reversed_2
O_Na_top = O_Na_top_1 + O_Na_top_2
O_Na_side = O_Na_side_1 + O_Na_side_2
O_CH3_4N_top = O_CH3_4N_top_1 + O_CH3_4N_top_2
O_CH3_4N_side = O_CH3_4N_side_1 + O_CH3_4N_side_2



for i in [O_NH4_top, O_NH4_side, O_CH3NH3_top, O_CH3NH3_side, O_CH3NH3_reversed, O_Na_top, O_Na_side, O_CH3_4N_top, O_CH3_4N_side]:
    charge_O.append(i)

for i in [C_NH4_top_1, C_NH4_side_1, C_CH3NH3_top_1, C_CH3NH3_side_1, C_CH3NH3_reversed_1, C_Na_top_1, C_Na_side_1, C_CH3_4N_top_1,  C_CH3_4N_top_2]:
    charge_C.append(i)

for i in range(0, len( [O_NH4_top, O_NH4_side, O_CH3NH3_top, O_CH3NH3_side, O_CH3NH3_reversed, O_Na_top, O_Na_side, O_CH3_4N_top, O_CH3_4N_side])):
	charge_CO2.append(charge_O[i] + charge_C[i] )

#the BE list is taken by this code, path: /home/theodoros/PROJ_ElectroCat/theodoros/CH3NH3/get_binding_energy_-1.8.py
BE = [-0.017598, 0.018123, -0.021773, 0.012819, -0.009439, 0.287321, 0.080832, 0.192319, 0.098130]
CO2_charge_initially = list()
for i in range(1, 8):
	CO2_charge_initially.append(16)

angles = list()
distance = list()
for i in [angles_NH4_top, angles_NH4_side, angles_CH3NH3_top, angles_CH3NH3_side, angles_CH3NH3_reversed, angles_Na_top, angles_Na_side, angles_CH3_4N_top, angles_CH3_4N_side]:
	angles.append(i)

for i in [distance_NH4_top, distance_NH4_side, distance_CH3NH3_top, distance_CH3NH3_side, distance_CH3NH3_reversed, distance_Na_top, distance_Na_side,  distance_CH3_4N_top,  distance_CH3_4N_side]:
	distance.append(i)

df = pd.DataFrame()
df["system"] = systems
df["oxygen 1 (eV/A)"] = force_O1
df["oxygen 2 (eV/A)"] = force_O2
df["CO2 BE (eV)"] = BE
#df["I CO2 charge (e)"] = CO2_charge_initially
df["CO2 charge"] = charge_CO2
df["O charge"] = charge_O
df["C charge"] = charge_C
df["angles"] = angles
df["distance"] = distance

#df.set_index('system', inplace=True)
print(df)

import matplotlib.pyplot as plt

os.chdir("/home/theodoros/PROJ_ElectroCat/theodoros/forces")

state_l = 0.9
state_h = 3

m_left = 0.18
m_right = 0.98
m_bottom = 0.17
m_top = 0.95

plt_h = 3.2 
plt_w = 4.5

fig = plt.figure(figsize=(plt_w, plt_h))
ax = fig.add_subplot( 1, 1, 1 )
xmax = -0.7
xmin = -2.2
ymax = 0.45
ymin = -0.25
Lx = xmax - xmin
Ly = ymax - ymin
ax.set_ylim( -0.03, 0.31 )
ax.set_xlim( -0.95, -0.73 )

plt.scatter(df["CO2 charge"], df["CO2 BE (eV)"], linewidth=1, s=60 )
#for i, txt in enumerate(systems):
#	ax.annotate(txt, (df["CO2 charge"][i], df["CO2 BE (eV)"][i]), fontsize = 5, xytext = (df["CO2 charge"][i]- 0.001, df["CO2 BE (eV)"][i] + 0.01))


ax.annotate("$NH_{4}^{+(1)}$", (df["CO2 charge"][0], df["CO2 BE (eV)"][0]), fontsize = 5, xytext = (df["CO2 charge"][0] - 0.016, df["CO2 BE (eV)"][0]))
ax.annotate("$NH_{4}^{+(2)}$", (df["CO2 charge"][1], df["CO2 BE (eV)"][1]), fontsize = 5, xytext = (df["CO2 charge"][1] - 0.016, df["CO2 BE (eV)"][1]))
ax.annotate("$CH_{3}NH_{3}^{+(1)}$", (df["CO2 charge"][2], df["CO2 BE (eV)"][2]), fontsize = 5, xytext = (df["CO2 charge"][2] + 0.004, df["CO2 BE (eV)"][2]))
ax.annotate("$CH_{3}NH_{3}^{+(2)}$", (df["CO2 charge"][3], df["CO2 BE (eV)"][3]), fontsize = 5, xytext = (df["CO2 charge"][3] + 0.004, df["CO2 BE (eV)"][3]))
ax.annotate("$CH_{3}NH_{3}^{+(3)}$", (df["CO2 charge"][4], df["CO2 BE (eV)"][4]), fontsize = 5, xytext = (df["CO2 charge"][4] - 0.021, df["CO2 BE (eV)"][4] + 0.01))
ax.annotate("$Na^{+(1)}$", (df["CO2 charge"][5], df["CO2 BE (eV)"][5]), fontsize = 5, xytext = (df["CO2 charge"][5] + 0.004, df["CO2 BE (eV)"][5]))
ax.annotate("$Na^{+(2)}$", (df["CO2 charge"][6], df["CO2 BE (eV)"][6]), fontsize = 5, xytext = (df["CO2 charge"][6] + 0.004, df["CO2 BE (eV)"][6]))
ax.annotate("$(CH_{3})_{4}N^{+(1)}$", (df["CO2 charge"][7], df["CO2 BE (eV)"][7]), fontsize = 5, xytext = (df["CO2 charge"][7] + 0.004, df["CO2 BE (eV)"][7]))
ax.annotate("$(CH_{3})_{4}N^{+(2)}$", (df["CO2 charge"][8], df["CO2 BE (eV)"][8]), fontsize = 5, xytext = (df["CO2 charge"][8] + 0.004, df["CO2 BE (eV)"][8]))


yticks = [ -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3 ]
ax.set_yticks( yticks )
ax.set_yticklabels( [ str(x) for x in yticks ] )
ax.set_ylabel( '$BE_{CO_{2}}$ (eV)', fontsize = 12, labelpad = 1 )
xticks = [-0.95, -0.9,  -0.85, -0.8, -0.75 ] 
ax.set_xticks( xticks )
ax.set_xticklabels( [ str( x ) for x in xticks ] )
ax.set_xlabel( '$CO_{2}$ charge ($e^{-}$)', fontsize = 12, labelpad = 1 )
ax.hlines(0,-1.0, -0.6, lw = 0.5, color = 'gray' )
#plt.text(-0.81,-0.04 , '$\Phi$ = -1.8 (V vs RHE)', fontsize = 9)
plt.text(-0.79,-0.04 , '$\Phi$ = -1.8 (V vs SHE)', fontsize = 7)
#ax.legend( fontsize = 8 )
plt.subplots_adjust(left=m_left, right=m_right, top=m_top, bottom=m_bottom, wspace=0.00, hspace= 0.00 )
plt.savefig( 'BE_vs_charge_d.png', dpi = 300 )
plt.show()



state_l = 0.9
state_h = 3

m_left = 0.18
m_right = 0.98
m_bottom = 0.17
m_top = 0.95

plt_h = 3.2
plt_w = 4.5

fig = plt.figure(figsize=(plt_w, plt_h))
ax = fig.add_subplot( 1, 1, 1 )
xmax = -0.7
xmin = -2.2
ymax = 0.45
ymin = -0.25
Lx = xmax - xmin
Ly = ymax - ymin
#ax.set_ylim( -0.03, 0.31 )
ax.set_xlim(2.5, 2.63)

os.chdir("/home/theodoros/PROJ_ElectroCat/theodoros/forces")
plt.scatter(df["distance"], df["CO2 BE (eV)"], linewidth=1, s=60 )

ax.annotate("$NH_{4}^{+(1)}$", (df["distance"][0], df["CO2 BE (eV)"][0]), fontsize = 5, xytext = (df["distance"][0], df["CO2 BE (eV)"][0] + 0.008))
ax.annotate("$NH_{4}^{+(2)}$", (df["distance"][1], df["CO2 BE (eV)"][1]), fontsize = 5, xytext = (df["distance"][1], df["CO2 BE (eV)"][1]+ 0.01))
ax.annotate("$CH_{3}NH_{3}^{+(1)}$", (df["distance"][2], df["CO2 BE (eV)"][2]), fontsize = 5, xytext = (df["distance"][2] + 0.0025 , df["CO2 BE (eV)"][2] - 0.003))
ax.annotate("$CH_{3}NH_{3}^{+(2)}$", (df["distance"][3], df["CO2 BE (eV)"][3]), fontsize = 5, xytext = (df["distance"][3] + 0.0025, df["CO2 BE (eV)"][3] - 0.0026))
ax.annotate("$CH_{3}NH_{3}^{+(3)}$", (df["distance"][4], df["CO2 BE (eV)"][4]), fontsize = 5, xytext = (df["distance"][4] - 0.0024, df["CO2 BE (eV)"][4] + 0.012))
ax.annotate("$Na^{+(1)}$", (df["distance"][5], df["CO2 BE (eV)"][5]), fontsize = 5, xytext = (df["distance"][5] + 0.0025, df["CO2 BE (eV)"][5]))
ax.annotate("$Na^{+(2)}$", (df["distance"][6], df["CO2 BE (eV)"][6]), fontsize = 5, xytext = (df["distance"][6] - 0.004, df["CO2 BE (eV)"][6]- 0.019))
ax.annotate("$(CH_{3})_{4}N^{+(1)}$", (df["distance"][7], df["CO2 BE (eV)"][7]), fontsize = 5, xytext = (df["distance"][7] + 0.0025, df["CO2 BE (eV)"][7]))
ax.annotate("$(CH_{3})_{4}N^{+(2)}$", (df["distance"][8], df["CO2 BE (eV)"][8]), fontsize = 5, xytext = (df["distance"][8] - 0.005, df["CO2 BE (eV)"][8] + 0.0093))


#yticks = [ -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3 ]
#ax.set_yticks( yticks )
#ax.set_yticklabels( [ str(x) for x in yticks ] )
ax.set_ylabel( '$BE_{CO_{2}}$ (eV)', fontsize = 12, labelpad = 1 )
xticks = [2.5, 2.52, 2.54, 2.56, 2.58, 2.60, 2.62 ] 
ax.set_xticks( xticks )
ax.set_xticklabels( [ str( x ) for x in xticks ] )
ax.set_xlabel('C-Bi Distance ($\AA$)', fontsize = 12, labelpad = 1)
ax.hlines(0, 2.48, 2.64, lw = 0.5, color = 'gray' )
plt.text(2.58,  -0.03 , '$\Phi$ = -1.8 (V vs SHE)', fontsize = 9)
plt.subplots_adjust(left=m_left, right=m_right, top=m_top, bottom=m_bottom, wspace=0.00, hspace= 0.00 )
plt.savefig( 'BE_vs_distance_d.png', dpi = 300 )
plt.show()


state_l = 0.9
state_h = 3

m_left = 0.18
m_right = 0.98
m_bottom = 0.17
m_top = 0.95

plt_h = 3.2
plt_w = 4.5

fig = plt.figure(figsize=(plt_w, plt_h))
ax = fig.add_subplot( 1, 1, 1 )
xmax = -0.7
xmin = -2.2
ymax = 0.45
ymin = -0.25
Lx = xmax - xmin
Ly = ymax - ymin
#ax.set_ylim( -0.03, 0.31 )
ax.set_xlim(132, 140.5)

plt.scatter(df["angles"], df["CO2 BE (eV)"], linewidth=1, s=60 )

ax.annotate("$NH_{4}^{+(1)}$", (df["angles"][0], df["CO2 BE (eV)"][0]), fontsize = 5, xytext = (df["angles"][0] - 0.62, df["CO2 BE (eV)"][0] - 0.015))
ax.annotate("$NH_{4}^{+(2)}$", (df["angles"][1], df["CO2 BE (eV)"][1]), fontsize = 5, xytext = (df["angles"][1] - 0.1, df["CO2 BE (eV)"][1] + 0.01))
ax.annotate("$CH_{3}NH_{3}^{+(1)}$", (df["angles"][2], df["CO2 BE (eV)"][2]), fontsize = 5, xytext = (df["angles"][2] + 0.15, df["CO2 BE (eV)"][2] - 0.01))
ax.annotate("$CH_{3}NH_{3}^{+(2)}$", (df["angles"][3], df["CO2 BE (eV)"][3]), fontsize = 5, xytext = (df["angles"][3], df["CO2 BE (eV)"][3] - 0.017))
ax.annotate("$CH_{3}NH_{3}^{+(3)}$", (df["angles"][4], df["CO2 BE (eV)"][4]), fontsize = 5, xytext = (df["angles"][4] - 0.69, df["CO2 BE (eV)"][4] + 0.01))
ax.annotate("$Na^{+(1)}$", (df["angles"][5], df["CO2 BE (eV)"][5]), fontsize = 5, xytext = (df["angles"][5] + 0.15, df["CO2 BE (eV)"][5]))
ax.annotate("$Na^{+(2)}$", (df["angles"][6], df["CO2 BE (eV)"][6]), fontsize = 5, xytext = (df["angles"][6] - 0.25, df["CO2 BE (eV)"][6] - 0.02))
ax.annotate("$(CH_{3})_{4}N^{+(1)}$", (df["angles"][7], df["CO2 BE (eV)"][7]), fontsize = 5, xytext = (df["angles"][7] - 0.25, df["CO2 BE (eV)"][7] + 0.01))
ax.annotate("$(CH_{3})_{4}N^{+(2)}$", (df["angles"][8], df["CO2 BE (eV)"][8]), fontsize = 5, xytext = (df["angles"][8] - 0.25, df["CO2 BE (eV)"][8] + 0.01))

#yticks = [ -0.05, 0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3 ]
#ax.set_yticks( yticks )
#ax.set_yticklabels( [ str(x) for x in yticks ] )
ax.set_ylabel( '$BE_{CO_{2}}$ (eV)', fontsize = 12, labelpad = 1 )
#xticks = [2.5, 2.52, 2.54, 2.56, 2.58, 2.60, 2.62 ] 
#ax.set_xticks( xticks )
#ax.set_xticklabels( [ str( x ) for x in xticks ] )
ax.set_xlabel('C-O-C Angle ($^{o}$)', fontsize = 12, labelpad = 1)
ax.hlines(0, 132, 140.5, lw = 0.5, color = 'gray' )
plt.text(137.5,  -0.03 , '$\Phi$ = -1.8 (V vs SHE)', fontsize = 9)
plt.subplots_adjust(left=m_left, right=m_right, top=m_top, bottom=m_bottom, wspace=0.00, hspace= 0.00 )
plt.savefig( 'BE_vs_angles_d.png', dpi = 300 )
plt.show()
