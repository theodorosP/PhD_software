import os
import re
import math
import pandas as pd
import numpy as np
from ase.io import read

class Landau_Energy:

	def __init__( self, pH_down, pH_up ):
		self.T = 300
		self.kB = 8.617333262 * 10**(-5)
		self.ln10KT = self.T * self.kB * math.log(10)
		self.pH_down = pH_down
		self.pH_up = pH_up
		self.loc = os.getcwd()
		self.Vol_dir =  self.get_Vol_dir()
		self.SHE_voltages = self.get_SHE_voltages()
		self.coverage_dir = self.get_coverage_dir()
		self.number_of_H = self.get_number_of_H()
		self.mu_H = self.get_mu_H()
		self.dictionary = self.get_Landau_energy()

	def get_Vol_dir( self ):
		voltage_dirs =  [ i for i in os.listdir( self.loc ) if ( os.path.isdir( self.loc + "/" + i ) and i.startswith( "chg" ) ) ] 
		return sorted( voltage_dirs, key= lambda x: float(x[  4 : ] ), reverse = True )

	def get_SHE_voltages( self ):
		pattern = r'-?\d+(\.\d+)?'
		return sorted( [ float(re.search(pattern, item).group()) for item in self.Vol_dir ], reverse = True )

	def get_coverage_dir( self ):
		coverages =  [ i for i in os.listdir( self.loc + "/" + self.Vol_dir[ 0 ] ) if ( i.startswith( "0" ) or i.startswith( "1ML" ) ) ]
		return sorted( coverages, key= lambda x: float(x[ : -2 ] ) )

	def get_omega_H2( self ):
		os.chdir( self.loc + "/H2")
		word = "GC Correction"
		struc = read( "OUTCAR" )
		with open( "OUTCAR", "r" )  as file:
			for line_number, line in enumerate( file ):
				if word in line:
					a = line
		correction = re.findall( r'[-+]?\d*\.\d+|\d+', a )
		correction = float(".".join( correction ) )
		return struc.get_potential_energy() - correction

	def get_number_of_H( self ):
		number_of_H = dict()
		for i in self.coverage_dir:
			os.chdir( self.loc +  "/" + self.Vol_dir[ 0 ] + "/" + i + "/target_potential")
			struc = read( "CONTCAR" )
			n = 0
			for j in struc:
				if j.symbol == "H":
					n += 1
			number_of_H[ i ] = n
		return number_of_H

	def get_unit_cell_area( self ):
		os.chdir( self.loc +  "/" + self.Vol_dir[ 0 ] + "/" + self.coverage_dir[ 0 ] +  "/target_potential/" )
		struc = read( "CONTCAR" )
		area_vec = np.cross( struc.cell[0], struc.cell[1] )
		area = np.sqrt( area_vec[ 0 ]**2 + area_vec[ 1 ]**2 + area_vec[ 2 ]**2 )
		return area

	def get_mu_H( self ):
		energy_H2 = self.get_omega_H2()
		mu_H = {}
		for pH in range( self.pH_down, self.pH_up + 1 ):
			for SHE in self.SHE_voltages:
				for N in self.coverage_dir:
					mu_H[ str( pH ) + "_" + str( SHE ) + "_" + str( N ) ] = self.number_of_H[ N ] * ( 0.5 * energy_H2 - self.ln10KT * pH - float( SHE ) )
		return mu_H

	
	def get_mu_H_meth_2( self ):
		energy_H2 = self.get_omega_H2()
		mu_H = {}
		for pH in [ 7 ]:
			for SHE in self.SHE_voltages:
				mu_H[ str( pH ) + "_" + str( SHE ) ] =  0.5 * energy_H2 - self.ln10KT * pH - float( SHE )
		return mu_H


	def get_grand_canonical_energy( self ):
		grand_canonical_energy = {}
		for i in self.Vol_dir:
			for j in self.coverage_dir:
				os.chdir( self.loc + "/" + i + "/" + j + "/target_potential")
				print( "Reading file:  ", i + "_" + j + "/OUTCAR")
				struc = read("OUTCAR")
				grand_canonical_energy[ i + "_" + j ] = struc.get_potential_energy()
		return grand_canonical_energy

	def get_Landau_energy( self ):
		area = self.get_unit_cell_area()
		keys_to_drop = list()
		grand_canonical_energy = self.get_grand_canonical_energy()
		Landau_energy = {}
		Landau_energy_per_H = {}
		energy_H2 = self.get_omega_H2()
		for SHE in self.SHE_voltages:
			for coverage in self.coverage_dir:     
				for pH in range( self.pH_down, self.pH_up + 1 ):                 
					Landau_energy[ str( pH ) + "_" + str( SHE ) + "_" + str( coverage ) ] = grand_canonical_energy[ "chg_" + str( SHE ) + "_" + str(coverage) ] - grand_canonical_energy[ "chg_" + str( SHE ) + "_0ML"  ] - self.mu_H[ str( pH ) + "_" + str(SHE) + "_" + str(coverage) ]        
		for pH in range( self.pH_down, self.pH_up + 1 ):
			for SHE in self.SHE_voltages: 
				keys_to_drop.append( str( pH ) + "_" + str( SHE ) + "_" + "0ML" )
		Landau_energy_drop = { key: value for key, value in Landau_energy.items() if key not in keys_to_drop }
		Landau_energy_per_area = {key: value / area  for key, value in Landau_energy_drop.items()}
		#for i in Landau_energy_drop:
		#	cov =  i.split( "_" )[ -1 ] 
		#	Landau_energy_per_H[ i ] = Landau_energy_drop[ i ] /  self.number_of_H[ cov ]
		#for (key1, value1), (key2, value2) in zip( Landau_energy_drop.items(), Landau_energy_per_H.items() ):
		#	print( key1, value1, key2, value2 )
		return Landau_energy_per_area #Landau_energy_per_H #Landau_energy_drop

	
	def get_Landau_energy_for_pH_7( self ):
		area = self.get_unit_cell_area()
		keys_to_drop = list()
		grand_canonical_energy = self.get_grand_canonical_energy()
		Landau_energy = {}
		Landau_energy_per_H = {}
		energy_H2 = self.get_omega_H2()
		for SHE in self.SHE_voltages:
			for coverage in self.coverage_dir:     
				for pH in [ 7 ]:                 
					Landau_energy[ str( pH ) + "_" + str( SHE ) + "_" + str( coverage ) ] = grand_canonical_energy[ "chg_" + str( SHE ) + "_" + str(coverage) ] - grand_canonical_energy[ "chg_" + str( SHE ) + "_0ML"  ] - self.mu_H[ str( pH ) + "_" + str(SHE) + "_" + str(coverage) ]        
		for pH in range( self.pH_down, self.pH_up + 1 ):
			for SHE in self.SHE_voltages: 
				keys_to_drop.append( str( pH ) + "_" + str( SHE ) + "_" + "0ML" )
		Landau_energy_drop = { key: value for key, value in Landau_energy.items() if key not in keys_to_drop }
		#Landau_energy_per_area = {key: value / area  for key, value in Landau_energy_drop.items()}
		
		Landau_energy_drop_pH_7 = {}
		for key, value in Landau_energy_drop.items():
			print( key, value )
			coverage = key.split('_')[-1].replace( "ML", "" )
			if coverage not in Landau_energy_drop_pH_7:
				Landau_energy_drop_pH_7[ coverage ] = list()
			Landau_energy_drop_pH_7[ coverage ].append( value )
		for i, j in Landau_energy_drop_pH_7.items():
			print(i, j )
		return Landau_energy_drop_pH_7 #Landau_energy_per_H #Landau_energy_drop
	


	def get_Landau_Energy_2( self ):
		diff = {}
		grand_canonical_energy = self.get_grand_canonical_energy()
		for SHE in self.SHE_voltages:
			for coverage in self.coverage_dir:
				for pH in range( self.pH_down, self.pH_up + 1 ):
					diff[ str( pH ) + "_" + str( SHE ) + "_" + str( coverage ) ] = grand_canonical_energy[ "chg_" + str( SHE ) + "_" + str(coverage) ]	- grand_canonical_energy[ "chg_" + str( SHE ) + "_0ML"  ] 
		for i, j in diff.items():
			print(i, j)
		
	def get_min_Landau_Energy( self, voltage, pH ):
		min_val = math.inf    
		dictionary = self.dictionary
		for coverage in self.coverage_dir[1: ]:
			current_key = str( pH ) + "_" + str( voltage ) + "_" + str( coverage )
			#print( current_key, dictionary[ current_key ] )
			if dictionary[ current_key ] < min_val:
				min_val = dictionary[ current_key ]
				key = current_key
		#print("The system with the lowest energy is:", key, "and Landau energy per H =", round( min_val, 4 ) )
		return key, min_val

	def get_data_as_DataFrame( self, pH ):
		data = {}
		df = pd.DataFrame()
		Landau_Energy = list()
		keys = list()
		dictionary = self.dictionary
		df[ "V" ] = df[ "pH" ] = df[ "Coverage" ] = df[ "Landau_Energy" ] = np.nan
		V = self.SHE_voltages
		pH_list = [ str( pH ) for i in range( 0, len( V ) ) ]
		df["pH"] = pH_list
		df["V"] = V
		for i in V:
			key, Landau_Energy_sys = self.get_min_Landau_Energy( i , pH )	
			Landau_Energy.append( Landau_Energy_sys )
			key = key.split( "_" )[ 2 : ]
			key = "_".join( key )
			keys.append( key )
		keys =  keys
		df["Coverage"] = keys
		df["Landau_Energy"] = Landau_Energy
		print( df )
		return df

	def get_all_data_in_dictionary( self ):
		data = {}
		all_dfs = []	
		for pH in range( 0, self.pH_up + 1 ):
			df = self.get_data_as_DataFrame( pH = pH )
			data[ "pH=" + str(pH) ] = df
			#all_dfs.append( df )
		#print( all_dfs  )		
		#for key, value in data.items():
		#	print( key )
		#	print( value )
		#	print("---" * 10)
		return data
		

class fix_data():
	
	def __init__( self , down_pH, up_pH ):
		self.down_pH = down_pH
		self.up_pH = up_pH
		self.obj = Landau_Energy( self.down_pH, self.up_pH )	
		self.dict = self.obj.get_all_data_in_dictionary()
	

	def get_pH( self ):
		pH = list()
		for i in self.dict.keys():
			pH_number = re.findall(r'\d+', i)[0]
			pH.append( int( pH_number) )		
		pH = np.arange( min(pH), max(pH) + 1 )
		print( pH )
		return pH

	def get_voltages( self ):
		voltage = list()
		key = list( self.dict.keys() )[0]  
		for i in self.dict[ key ]["V"]:
			voltage.append(  float( i )  )
		print( voltage )
		return voltage
	
	def get_plotting_data( self ):
		data = {}
		pH = list()
		V = self.get_voltages()
		voltages = list()
		Landau_Energy = list()
		for i in range(0, ( self.up_pH + 1) * len(V)):
			pH.append( i // len( V ) )
		voltages = [ i for j in range(0, self.up_pH + 1 ) for i in V ]
		df = self.obj.get_all_data_in_dictionary()
		for i in df.keys():
			for j in range(0, len( df[ "pH=0" ][ "Landau_Energy" ] ) ):
				Landau_Energy.append( df[ i ][ "Landau_Energy" ][ j ] )
		data[ "pH" ] =  pH 
		data[ "V" ] = voltages
		data[ "Landau_Energy" ] = Landau_Energy
		
		data_df = pd.DataFrame( data )
		pH = np.array(data_df['pH']).reshape( self.up_pH + 1,  len( V ) )
		Landau_Energy = np.array(data_df['Landau_Energy']).reshape( self.up_pH + 1,  len( V ) )
		V = np.array(data_df['V']).reshape( self.up_pH + 1,  len( V ) )
		#print( pH, V, Landau_Energy )
		return pH, V, Landau_Energy

if __name__ == "__main__":
	obj = Landau_Energy( pH_down = 0, pH_up = 7 )
	#obj.get_grand_canonical_energy()
	#obj.get_Landau_Energy_2()
	#obj.get_Landau_energy_meth_2()
	#a = obj.get_Landau_energy_for_pH_0()
	#print( obj.coverage_dir)
	#print( a )
	#obj.get_all_data_in_dictionary()
	#obj = fix_data( 0, 7 )
	#obj.get_plotting_data()
