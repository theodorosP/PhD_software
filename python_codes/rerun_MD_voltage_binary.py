import os
import glob

def sub():
    path = os.getcwd()
    dirs = [ i for i in os.listdir( path ) if os.path.isdir( i ) == True ]
    print( dirs )
    for i in dirs:
        os.chdir( path + "/" + i )
        os.system( "python rerun.py" )

if __name__ == "__main__":
    sub()
[trahman@viper01 MD_voltage]$ nano rerun.py 
[trahman@viper01 MD_voltage]$ ls
CH3NH3  Na  NH4  rerun.py  sub.sh
[trahman@viper01 MD_voltage]$ cd CH3NH3/
[trahman@viper01 CH3NH3]$ ls
1_CH3NH3_40_H2O  3_CH3NH3_40_H2O  5_CH3NH3_40_H2O  job  rerun.py  slurm-300582.out
[trahman@viper01 CH3NH3]$ cat rerun.py 
import os
import re
import glob
import shutil

def get_path_and_dirs():
    path = os.getcwd()
    dirs = [ i for i in os.listdir( "." ) if os.path.isdir( i ) == True  ]
    return path, dirs

def make_dirs_and_copy():
	dirs = [ i for i in os.listdir( "." ) if os.path.isdir( i ) == True  ]
	if dirs:
		new_dir_name = f"RUN{len(dirs) + 1 }"
	else:
		new_dir_name = "RUN1"
	os.mkdir( new_dir_name )
	new_dirs = [ i for i in os.listdir( "." ) if os.path.isdir( i ) == True  ]
	new_dirs.sort( key = os.path.getctime )
	target_dir =  new_dirs[ - 1 ]
	files = [ i for i in glob.glob( "*" ) if os.path.isfile( i ) ]
	for i in files:
		if i in [ "OUTCAR", "REPORT", "vasprun.xml", "XDATCAR" ]:
			os.system( f"gzip {i}" )
	files = [ i for i in glob.glob( "*" ) if os.path.isfile( i ) ]
	for i in files:
		shutil.copy( i, target_dir )
	os.remove( "POSCAR" )
	os.rename( "CONTCAR", "POSCAR" )

def get_OUTCAR_NELECT():
	files = [ i for i in glob.glob( "*" ) if os.path.isfile( i ) ]
	print( files )
	if "OUTCAR" in files:
		print( "OUTCAR found" )
		with open( "OUTCAR", "rb" ) as file:
			lines = file.readlines()
		nelect_lines = [ line.decode('utf-8', errors='ignore').strip() for line in lines if b"NELECTCURRENT" in line ]
		last_line = nelect_lines[ - 1 ].strip()
		#print( last_line )
		if nelect_lines:
			match =  re.search( r'NELECTCURRENT\s+([\d.-]+)', last_line )
			#print( "NELECTCURRENT = ", match.group( 1 )  )
			return  float( match.group( 1 ) )
		else:
			print( "NELECT not found yet" )
			return
	else:
		print( "OUTCAR not found" )
		return


def update_INCAR( val ):
	with open( "INCAR", 'r') as file:
		lines = file.readlines()

	NELECT_present = False
	for i, line in enumerate( lines ):
		if line.startswith( 'NELECT' ):
			lines[ i ] = f'NELECT = {val}\n'
			NELECT_present = True
			break

	if not NELECT_present:
		lines.append(f'NELECT = {val}\n')

	with open( "INCAR" , 'w' ) as file:
		file.writelines( lines )


def parse_INCAR():
	path, dirs = get_path_and_dirs()
	for i in dirs:
		os.chdir( path + "/" + i  )
		print( "--" * 10 )
		print( os.getcwd()  )
		NELECTCURRENT = get_OUTCAR_NELECT()
		print( "nelect =", NELECTCURRENT )
		make_dirs_and_copy()
		update_INCAR( NELECTCURRENT )

def submit_job():
	cpath = os.getcwd()
	parse_INCAR()
	os.chdir( cpath )
	os.system( "sbatch job" )

if __name__ == "__main__":
	submit_job()