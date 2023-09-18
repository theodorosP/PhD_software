from ase.io import read, write
from ase.constraints import FixedPlane 

struc = read( "/home/theodoros/PROJ_MetalOnSemiconductor/theodoros/6x6/no_constrained/no_constrained_12/1x1x1/CONTCAR" ) 

post = struc.get_positions()

pb_top = [ atom.index for atom in struc if atom.symbol == 'Pb' and atom.position[ 2 ] > 17 ]
pb_bot = [ atom.index for atom in struc if atom.symbol == 'Pb' and atom.position[ 2 ] < 17 ]

sum_top = 0
sum_bot = 0 

for i in range(0, len(pb_top) ): 
    sum_top += struc[ pb_top[ i ] ].position[ 2 ]
for i in range(0, len(pb_bot) ): 
    sum_bot += struc[ pb_bot[ i ] ].position[ 2 ]

mean_top = sum_top/len( pb_top ) 
mean_bot = sum_bot/len( pb_bot ) 

struc1 = read("POSCAR_1")
post1 = struc1.get_positions()

pb_top1 = [ atom.index for atom in struc1 if atom.symbol == 'Pb' and atom.position[ 2 ] > 17 ]
pb_bot1 = [ atom.index for atom in struc1 if atom.symbol == 'Pb' and atom.position[ 2 ] < 17 ]

for i in range( 71 ): 
    post1[ pb_top1[ i ], 2 ] = mean_top
    post1[ pb_bot1[ i ], 2 ] = mean_bot 

struc1.set_positions( post1 )
const = pb_top1 + pb_bot1
c = FixedPlane( const , (0,0,1) )
struc1.set_constraint( c )

write( 'POSCAR_2', struc1, vasp5 = True, sort = True, direct = True ) 
