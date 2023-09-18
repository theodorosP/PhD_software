from ase.io import *
from ase.build import bulk
from dlePy.qe.pwscf import PWscfInput 
from ase.visualize import view 
import ase 
from ase.build import * 


latt = $UU
Gebulk = bulk( 'Ge', 'diamond', a = latt )


#view(Gebulk) 
write('POSCAR',Gebulk,format='vasp',direct=True, vasp5 = True)
