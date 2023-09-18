mport numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('DATA.dat')
lat = data[:,0]
energy = data[:,1]

plt.plot(lat,energy)
plt.xlabel('Lattice Parameter (Angstrom)')
plt.ylabel('Total Energy (eV)')

min = energy[0]
min_lat = lat[0]
for i,at in enumerate(energy):
   if at < min: 
      min = at
      min_lat = lat[i]

plt.scatter(lat,energy)
plt.scatter(min_lat,min,label = 'Mini. energy is at ' + str(min_lat) +' A')
plt.legend(loc = 1) 

plt.savefig('DATA.png')
plt.show()

