
from ase.io import read, write 

struc = read( 'POSCAR.vasp' ) 

elements = struc.get_atomic_numbers() 

elements[ 46 ] = 82
elements[ 68 ] = 82 
elements[ 161 ] = 32
elements[ 160 ] = 32 
struc.set_atomic_numbers( elements ) 

from ase.visualize import view 
view( struc )
write ('POSCAR', struc, direct=True, format='vasp', sort = True)
