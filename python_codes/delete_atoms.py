from ase.build import diamond100
from ase.io import *
from ase.build import bulk
from dlePy.qe.pwscf import PWscfInput 
from ase.visualize import view 
from ase.io import read, write
from ase.constraints import FixedPlane 

struc = read("CONTCAR_add_Pb_to_make_dimers")
del struc[[atom.index for atom in struc if atom.symbol=='Pb']]

view(struc)
write ('POSCAR', struc, direct=True, format='vasp', sort = True)
