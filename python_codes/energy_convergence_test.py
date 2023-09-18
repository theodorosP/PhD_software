import pandas as pd
import numpy as np
from ase.io import read
from pandas import concat
import os
import matplotlib.pyplot as plt

#number of files I want
t = 26

loc = os.path.abspath(os.getcwd()) + "/"
en_atom = []
for i in range (4, t):
	struc = read(loc + "k-" + str(i) + "/OUTCAR")
	en_per_atom = struc.get_potential_energy()/len(struc)
	en_atom.append(en_per_atom)


df = pd.DataFrame()
df["en_per_atom"] = en_atom
df.index = range(4, len(df) + 4, 1)



for i in range(4, len(df) + 4):
	try:
		df.loc[i, "error"] =  abs(df["en_per_atom"][len(df) + 3]  - df["en_per_atom"][i]) 
	except:
		pass

print(df)


x_labels = [] 
for i in range(4, len(df) +4):
	x_labels.append(str(i)+"x" +str(i)+ "x" + "1")


plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=10)
fig, ax = plt.subplots()
ax.plot(df["error"]  , "-o", label = "error in energy per atom")
ax.set_xlabel("k-point mesh")
ax.set_ylabel("Error in  energy per atom (eV)")
ax.title.set_text("Error in energy per atom vs k-point mesh")
ax.axhline(0.0001,  linestyle = "--", color = "black")
ax.text(t, 0.0001, '0.0001 eV', va = 'bottom', ha = 'right' )
ax.legend(loc = "best")
plt.xticks(df.index, x_labels, rotation=25)
os.chdir(loc)
plt.savefig("energy_100.png")
plt.show()
