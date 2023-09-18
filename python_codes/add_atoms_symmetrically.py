from ase.build import diamond111, add_adsorbate
from ase.io import *
from ase.build import bulk
from dlePy.qe.pwscf import PWscfInput 
from ase.visualize import view 
import ase 
#from ase.build import *
from dlePy.supercell import supercell
from ase.constraints import FixAtoms




#make the structure that I want
slab = diamond111("Ge", a =  5.61651701355064, size = (1,1,12), vacuum =7.5  )

# Remove the top atom with one bonding
del slab[0]
del slab[10]


x_ads = (slab[9].position[0])
y_ads = (slab[9].position[1])
add_adsorbate(slab, 'Pb',  3.4 , position= (x_ads ,y_ads ))


x_ads = (slab[0].position[0])
y_ads = (slab[0].position[1])
add_adsorbate(slab, 'Pb',  -17.432 , position= (x_ads ,y_ads ))


slab *= (6,6,1) 

list = [ at.index for at in slab if at.position[ 2 ] == slab[ 6 ].position[ 2 ]]
list += [ at.index for at in slab if at.position[ 2 ] == slab[ 8 ].position[ 2 ]]  


from random import randint 
import random
num_list = [] 
num = 1 
random.seed(3)
for i in range( num ): 

   a = randint( 0, len( list )-1 )
   if a not in num_list:
      num_list.append( a )   
      pos = slab[ list[ a ] ].position
      add_adsorbate( slab, 'Pb', 3.4, position = ( pos[ 0 ], pos[ 1 ] ) )
      add_adsorbate( slab, 'Pb', -17.432, position = ( pos[ 0 ] + slab[ 11 ].position[ 0 ], pos[ 1 ] + slab[ 11 ].position[ 1 ] ) )    



view(slab)
write ('POSCAR', slab, direct=True, format='vasp', sort = True)
