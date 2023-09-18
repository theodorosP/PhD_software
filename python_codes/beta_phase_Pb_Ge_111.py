from ase.build import diamond111, add_adsorbate 
from ase.visualize import view
from ase.io import read,write 
from dlePy.supercell import supercell , create_matrix_surface

# Create your Surface structure

latt = 5.63657483
struc = diamond111( 'Ge',  a = latt, size=(1, 1, 12), vacuum = 7.5)


# Remove the atoms we do not want on the surface 
del struc[0]
del struc[10]

# Setting Vacuum 
#struc.center ( vacuum = 7.5 , axis = 2 )

struc = create_matrix_surface( struc, matrix = (1, 1, -1, 2)) 


cell = struc.get_cell() 
add_adsorbate( struc,'Pb', 2, position = ( struc[ 19 ].position[ 0 ], struc[ 19 ].position[ 1 ] ) ) 
pos1x = struc[ 28 ].position[ 0 ] + abs(struc[ 28 ].position[ 0 ] - struc[ 25 ].position[ 0 ])/2
pos1y = struc[ 28 ].position[ 1 ] + abs( struc[ 28 ].position[ 1 ] - struc[ 25 ].position[ 1 ])/2
add_adsorbate( struc, 'Pb', 2, position = ( pos1x, pos1y ) ) 
pos2x = struc[ 29 ].position[ 0 ] + abs( cell[ 0, 0 ] - struc[ 29 ].position[ 0 ] ) /2 
pos2y = struc[ 29 ].position[ 1 ]/2
add_adsorbate( struc, 'Pb', 2, position = ( pos2x, pos2y ) ) 
pos3x = struc[ 26 ].position[ 0 ] + abs( struc[ 27 ].position[ 0 ] + cell[ 0, 0 ] - struc[ 26 ].position[ 0 ] )/2 
pos3y = struc[ 26 ].position[ 1 ] 
add_adsorbate( struc, 'Pb', 2, position = ( pos3x, pos3y )) 


add_adsorbate( struc,'Pb', -15.8, position = ( struc[ 9 ].position[ 0 ], struc[ 9 ].position[ 1 ] ) )
pos1x = struc[ 3 ].position[ 0 ] + abs(struc[ 3 ].position[ 0 ] - struc[ 0 ].position[ 0 ])/2
pos1y = struc[ 3 ].position[ 1 ] + abs( struc[ 3 ].position[ 1 ] - struc[ 0 ].position[ 1 ])/2
add_adsorbate( struc, 'Pb', -15.8, position = ( pos1x, pos1y ) ) 

pos2x = struc[ 0 ].position[ 0 ] + abs( cell[ 0, 0 ] - struc[ 0 ].position[ 0 ] ) /2 
pos2y = struc[ 0 ].position[ 1 ]/2
add_adsorbate( struc, 'Pb', -15.8, position = ( pos2x, pos2y ) ) 


struc[ 34 ].position[ 0 ] += 3.452

add_adsorbate( struc,'Pb', -15.8, position = ( struc[ 9 ].position[ 0 ], struc[ 9 ].position[ 1 ] ) )

view( struc )  
write ('POSCAR', struc, direct=True, format='vasp', sort = True)
