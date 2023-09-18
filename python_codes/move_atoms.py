from ase.io import read,write 

struc = read( 'POSCAR_old') 
print( struc[ 428 ].position[ 0 ] ) 
struc[ 428 ].position[ 0 ] += 1  
print( struc[ 428 ].position[ 0 ] )
write( "POSCAR", struc, format = 'vasp', direct = True, vasp5 = True )
