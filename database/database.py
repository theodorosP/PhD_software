import json
import os 
import os.path
os.system("rm -rf data.json")

def json_object_function(dictionary):
	json_object = json.dumps(dictionary, indent = 4)
	print(json_object)
	return json_object



def write_to_file(json_object):
	with open("data.json", "a") as f:
		f.write("\n")
	        f.write("---"*22 + " START " + "---"*22)
        	f.write("\n")
       		json.dump(json_object, f)
        	f.write("\n")
		f.write("---"*22 + " STOP " + "---"*22)
        	f.write("\n")
	return "data.json"

def validate_path(loc):
	a = os.path.isdir(loc)	
	b = os.path.isfile(loc)
	if  b == True:
		print("The file : ", loc, " exists")
	elif a == True:
		print("The folder : ", loc, " exists")
	else:
		print(loc, "DOES NOT exist")	

Bi_optimal = {"Bi optimal latice constant" : "/home/theodoros/PROJ_ElectroCat/theodoros/Bi_111/optimal_lattice_constant/final"}
json_object = json_object_function(Bi_optimal)
write_to_file(json_object)

Bi_6x6x6 = {"Bi_111_6x6x6" : "/home/theodoros/PROJ_ElectroCat/theodoros/Bi_111/Bi_111_6x6x6"}
json_object = json_object_function(Bi_6x6x6)
write_to_file(json_object)


plot = {"plot biding energy, angles, distance " : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/binding_energy.py"}
json_object = json_object_function(plot)
write_to_file(json_object)


path_list_side =  {
		"CO2 side, V = 0.0"  : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_0.0/target_potential", 
		"CO2 side, V = -0.5" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-0.5/target_potential", 
		"CO2 side, V = -1.0" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-1.0/target_potential", 
		"CO2 side, V = -1.5" :  "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-1.5/target_potential/test1/target_potential", 
		"CO2 side, V = -2.0" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-2.0/target_potential", 
		"CO2 side, V = -2.5" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/right_left_4_symmetric/FindChg_U_-2.5/target_potential"
		}
json_object = json_object_function(path_list_side)
write_to_file(json_object)


path_list_top = {
		"CO2 top, V = 0.0"  : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_0.0/target_potential", 
		"CO2 top, V = -0.5" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_-0.5/target_potential", 
		"CO2 top, V = -1.0" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_-1.0/target_potential", 
		"CO2 top, V = -1.5" :  "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_-1.5/target_potential", 
		"CO2 top, V = -2.0" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_-2.0/target_potential", 
		"CO2 top, V = -2.5" : "/home/theodoros/PROJ_ElectroCat/theodoros/NH4_Bi111/NH4_Bi111_O_not_constrained/more_sites/NH4_top_symmetric/FindChg_-2.5/target_potential"
		}
json_object = json_object_function(path_list_top)
write_to_file(json_object)

'''
l = list()
for i in [Bi_optimal, Bi_6x6x6, plot, path_list_side, path_list_top]:
	l.append(i.values())


for i in l:
	for j in range(len(i)):
		validate_path(i[j])

'''
