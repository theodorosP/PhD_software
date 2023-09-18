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


slab *= (6,6,1) 

x_ads = (slab[219].position[0])
y_ads = (slab[219].position[1])
add_adsorbate(slab, 'Pb',  3.4 , position= (x_ads ,y_ads ))

x_ads = (slab[200].position[0])
y_ads = (slab[200].position[1])
add_adsorbate(slab, 'Pb',  -17 , position= (x_ads ,y_ads ))



l  = [ ] 
for i in [ 'Ge', 'Pb' ]: 
    l += [ at.index for at in slab if at.symbol == i ] 
slab = slab[ l ] 
view(slab)
write ('POSCAR00', slab, direct=True, vasp5 = True )

