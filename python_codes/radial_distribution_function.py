from ase.io import read,write 
from ase.geometry.analysis import Analysis
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter1d
import numpy as np

loc = os.path.abspath(os.getcwd())

rdf_average = list()
for i in range(0, 13):
	list_rdf = list()
	for j in range(1, 6):
		os.chdir("/storage/data2/PROJ/MetalOnSemiconductor/theodoros/6x6/5_system_each_no_constrained/no_constrained_" + str(i) + "/3x3x1/system_" + str(j) + "/g_of_r")
		struc = read( 'CONTCAR.vasp') 
		ana = Analysis(struc)
		a = ana.get_rdf(10, 1000, return_dists = True)
		c = list(a[0])
		rdf = c[0].tolist()
		distance = c[1].tolist()
		list_rdf.append(rdf)
		
	print("i = ", i)
	average = list()
	for (item1, item2, item3, item4, item5) in zip(list_rdf[0], list_rdf[1],  list_rdf[2],  list_rdf[3],  list_rdf[4] ):
		average.append((item1 + item2 + item3 + item4 + item5) / 5)
	rdf_average.append(average)
	print(average)
	print("-" * 80)


for i in range(13, 26):
	list_rdf = list()
	for j in range(1, 6):
		os.chdir("/storage/data2/PROJ/MetalOnSemiconductor/theodoros/6x6/5_system_each_constrained/constrained_new_systems_" + str(i) + "/3x3x1/system_" + str(j) + "/g_of_r")
		struc = read( 'CONTCAR.vasp') 
		ana = Analysis(struc)
		a = ana.get_rdf(10, 1000, return_dists = True)
		c = list(a[0])
		rdf = c[0].tolist()
		distance = c[1].tolist()
		list_rdf.append(rdf)
	print("i = ", i)
	average = list()
	for (item1, item2, item3, item4, item5) in zip(list_rdf[0], list_rdf[1],  list_rdf[2],  list_rdf[3],  list_rdf[4] ):
		average.append((item1 + item2 + item3 + item4 + item5) / 5)
	rdf_average.append(average)
	print(average)
	print("-" * 80)

print(len(rdf_average))


print("-" * 100)
for i in range(1, len(rdf_average)):
	rdf_average[i] = [x + i + 1 for x in rdf_average[i]]
print(rdf_average)

n = len(rdf_average)
colors = plt.cm.jet(np.linspace(0,1,n))


os.chdir(loc)
sigma = 20
for i in range(0, 12):
	plt.plot(distance, gaussian_filter1d(rdf_average[i], sigma = sigma ),  color=colors[i] )
	#plt.title("Radial distribution function vs distance")	
for i in range (13, len(rdf_average)):
	plt.plot(distance, gaussian_filter1d(rdf_average[i], sigma = sigma),  color=colors[i] )
plt.plot(distance, gaussian_filter1d(rdf_average[12], sigma = sigma),  color= "black", linewidth = 1, linestyle = "--" )
plt.xlim(2, 6)
plt.ylabel("g(r)")
plt.xlabel("Distance (r)")
plt.savefig("g_of_r.png")
plt.show()

