from ase.io import read, write 

struc = read( 'POSCAR00' ) 

add = struc[ 360 ].position - struc[ 219 ].position


struc[ 360 ].position -= add
struc[ 219 ].position += add 


add2 = struc[ 361 ].position - struc[ 200 ].position


struc[ 361 ].position -= add2
struc[ 200 ].position += add2 

write( 'POSCAR05', struc, direct = True, vasp5 = True ) 
