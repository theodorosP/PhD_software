import pandas as pd
import numpy as np
from ase.io import read
from pandas import concat
import os
import matplotlib.pyplot as plt 

loc = os.path.abspath(os.getcwd()) + "/"

struc = read(loc + "k-4/" + "OUTCAR")
df = pd.DataFrame(struc.get_forces(), columns = ["Fx4", "Fy4", "Fz4"])
#print(df)

#number of directories that I want
t = 26

for i in range(5, t):
	os.chdir(loc + "k-" + str(i))
	struc = read("OUTCAR")
	df1 = pd.DataFrame(struc.get_forces(), columns = ["Fx" + str(i), "Fy" + str(i), "Fz" + str(i)])
	df = concat([df, df1], axis =1)
#print(df["Fx4"][0])



names = []
for i in range(4, t):
        names.append("df_F"  + str(i))

for i in range(len(names)):
	names[i] = pd.DataFrame()
#print(names)


new_df = pd.DataFrame()
df_test = pd.DataFrame( concat([df["Fx4"], df["Fy4"], df["Fz4"]], axis = 0))
df_test.columns = ["F4"]
#print(df_test["F4"][0])


lis = []
i = 4
j = 0
a = pd.DataFrame()
while  i < t:
	a = concat([df["Fx" + str(i)], df["Fy" + str(i)], df["Fz" + str(i)]], axis = 0, ignore_index = True)
	a = pd.DataFrame(a)
	a.columns = ["F" + str(i)]
	lis.append(a)
	i = i + 1
#print(lis[14]["F18"][0])	




df_final = pd.DataFrame()
for i in range(len(lis)):
	df_final = concat([df_final, lis[i]], axis =1)
#print(df_final)



for i in  range(4, t):
        MSE_F = np.square(df_final["F" + str(t - 1)] - df_final["F" + str(i)]).mean()
        RMSE_F = np.sqrt(MSE_F)
	error = np.abs(df_final["F" + str(t - 1)] - df_final["F" + str(i)])
	df_final["errors" + str(i)] = error
	df_final.loc[0, "RMSE_F" + str(i)] = RMSE_F
	
#print(df_final)


df_error = pd.DataFrame()


for i in range(4, t):
	try:
		df_error.loc[i, "rmse"] = df_final["RMSE_F" + str(i)][0]
		df_error.loc[i, "max-error"] = max(df_final["errors" + str(i)])
	except:
		pass

print(df_error)




x_labels = [] 
for i in range(4, len(df) +4):
	x_labels.append(str(i)+"x" +str(i)+ "x" + "1")


plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=10)
fig, ax = plt.subplots()
ax.plot(df_error["rmse"], "-o", label = "RMSE")
ax.plot(df_error["max-error"], "-o", label = "max-error")
#ax.scatter(i1, f_rmse + 0.0015 , color = "green", marker='v', label ="rmse, max-error < 0.001 ev/A")
#ax.scatter(j1, f_max_error + 0.0015   , color = "green", marker='v')
ax.title.set_text(" Error in force (eV/$\AA$) vs k-point mesh")
ax.set_xlabel(" k-point mesh")
ax.set_ylabel("Error in  force per atom (eV/$\AA$)")
ax.axhline(0.0001,  linestyle = "--", color = "black")
ax.text( t - 1, 0.0001, '0.0001 eV/$\AA$', va = 'bottom', ha = 'right' )
ax.legend(loc = "best")
plt.xticks(df_error.index, x_labels, rotation=25)
ax.legend(loc = "best")
os.chdir(loc)
plt.savefig("forces_100.png")
plt.show()
