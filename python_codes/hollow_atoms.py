from ase.io import read 
import math 
from ase import Atoms 
from ase.neighborlist import NeighborList 
import numpy as np 
from ase.build import add_adsorbate 


struc = read( 'POSCAR' ) 


Pb = [ atom.index for atom in struc if atom.symbol == 'Pb' ] 

nl = NeighborList( [ 1.2 ] * len( struc ), self_interaction = False, bothways = True ) 
nl.update( struc )
pb_atom = Atoms( 'Pb', positions = [ (0,0,0) ] ) 
corner_edge = [ ] 
mid_edge = [ ]
for i in Pb:
    out, offset = nl.get_neighbors( i )
    if len( out ) == 4:
        mid_edge.append( [i,out]) 
    if len( out ) == 3: 
        corner_edge.append( [ i, out ] ) 
for i in corner_edge:
      for k in mid_edge: 
         if k[ 0 ] in i[ 1 ]: 
            atoms=[ k[ 0 ], i[ 0 ], int( np.intersect1d( i[ 1 ], k[ 1 ] ) ) ]
            dis = struc.get_distance( atoms[ 0 ], atoms[ 1 ], mic = True ) + struc.get_distance( atoms[ 2 ], atoms[ 1 ], mic = True ) + struc.get_distance( atoms[ 0 ], atoms[ 2 ], mic = True )
            dis /= 3. 
            ht = math.sqrt( 2/3. ) * dis 
            centroid = np.sum( struc[ atoms ].get_positions(), axis = 0 )/3 
            add_adsorbate( struc, pb_atom, ht, position = centroid[ 0:2 ] ) 

from ase.visualize import view 
view( struc ) 
