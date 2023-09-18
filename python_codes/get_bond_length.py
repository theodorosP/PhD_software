from ase.io import read 
from fractions import Fraction
#from ase.neighborlist import  natural_cutoffs, NeighborList 
from ase.neighborlist import NeighborList 
import numpy as np 
import matplotlib.pyplot as plt


sys = read( 'OUTCAR' ) 

lead_list = [ atom.index for atom in sys if atom.symbol == 'Pb' ] 
struc = sys[ lead_list ] 
avg = 0 
k = 0

l_avg = list()
print( len( lead_list ), 'Pb Atoms'  ) 
for atom in range( len( struc ) ): 
	print( atom, ' out of ', len( struc ) ) 
  	out = [ ]
	cut = 2 
	nl = NeighborList( [ cut ] * len( struc ), self_interaction = False, bothways = True ) 
	nl.update( struc ) 
	out, outsets  = nl.get_neighbors( atom )
	bond = struc.get_distances( atom, out, mic = True ) 
	bond = np.array( bond ) 
	bond = np.delete( bond, np.where( bond > 4 ) ) 
	print("bond = ",  bond ) 
	avg += np.sum( bond )/( len( bond ) * len( lead_list ) )	
	print("avg = ", avg)
l_avg.append(avg)
print(l_avg)
