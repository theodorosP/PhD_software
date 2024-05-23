import os

def tranfer(path):
	host = 'cobra'
	#path = '/u/trahman/data/theo/Bi/Na/Na_top'
	includes = [ '*OUTCAR*', '*CONTCAR*', '*POSCAR*', '*INCAR*', '*KPOINTS*', '*EIGENVAL*', '*.py*', '*.DAT', '*.log*', '*.j', 'chg_diff.py', "job", "show.sh", "CHGDIFF.vasp", "CHGDIFF_2.vasp", "CHGDIFF_3.vasp", "job", "TPOTCAR", "neb_results.py", "CHGDIFF.vasp", "run_job_till_converge.sh", "ACF.dat"]
#CHGDIFF.vasp
	options = '-av --exclude "transfer.py" --include "*/" ' 

	for include in includes:
		options += ' --include "' + include +'"'

	options += ' --exclude "*" '

	cmd = 'rsync ' + options + host + ':' + path + ' .'

	os.system( cmd )
	cmd = 'chmod g+rsx `find . -type d`'
	os.system(cmd)
	cmd = 'chmod g+r -R *'
	os.system(cmd)
	
tranfer( '/cobra/u/trahman/data/theo/Bi/Pt/Pt/Pt_fcc_fcc') 
tranfer( '/cobra/u/trahman/data/theo/Bi/Pt/Pt/Pt_fcc_hcp')
