mport os

start_val = 550
end_val = 586
mini = start_val
for i in range( start_val, end_val, 1 ):
  rename = i/100.
  EN_folder = 'A-' + str( rename )
  NAME_OF_WRITE_FILE = 'make_POSCAR.py'
  os.system( 'mkdir ' + EN_folder )
  os.system( 'cp ' + NAME_OF_WRITE_FILE + ' job ' + ' POTCAR ' + ' INCAR ' + ' KPOINTS ' + EN_folder )
  os.chdir( EN_folder )
  os.system( 'sed -i \'s/$UU/' + str( rename ) + '/g\' ' +  NAME_OF_WRITE_FILE )
  #os.system( 'mkdir -p ' + EN_folder )
  #os.system( 'cp ' + NAME_OF_WRITE_FILE + ' job ' + EN_folder )
  #os.system( 'sed -i \'s/$mini/' + str( mini ) + '/g\' ' + NAME_OF_WRITE_FILE )
  os.system( 'python ' + NAME_OF_WRITE_FILE )
  os.system( 'qsub job' )
  os.chdir ( '../' )
os.chdir( '../' )
