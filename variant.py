import math
import sys
#This is a test commit
m = 1
cm = 0.01
mm = 0.001
kA = 1000
GHz = 10e9

electron_mass = 9.1093837015e-31 #kg
electron_charge = 1.602176634e-19 #C
mu_0 = 1.25663706212e-6 #N*A^-2


from variables import * 
from functions import *
from controll import *

	def calcEverything( 
  #number_of_windings_x = None
  #number_of_wingings_y = None
  max_current_per_mm_2 = float(50.) #A/mm²
  specific_resistance = None
  #major_winding_radius = float(0.16) #m
  #winding_radius = float(0.) 
  #total_winding_radius = float(0.) #mm, coil + cooling
  radius_major = None
  radius_minor = None
  number_coils = None
  number_windings = None
	material = None
	B_toroidal = None
	frequency_rotation = None
):
	'''This function will output all parameters of the stellarator coil design based on a set of keyword arguments that are passed to it.
	This set has to be complete in a sense that all other parameters can be determined from it.
	'''

	
  if number_coils == None or number_windings == None or radius_major == None or radius_minor == None:
		raise Exception('Required geometric argument missing: number_coils or number_windings or radius_major or radius_minor')

	if isinstance(B_toroidal, int) or isinstance(B_toroidal, float):
		if I_linking != None or frequency_rotation != None:
			raise Exception('To much information on target magnetic field. Pass B_toroidal or frequency_rotation or I_linking')
		I_linking = 2*np.pi*radius_major*B_toroidal/mu_0
	if isinstance(frequency_rotation, int) or isinstance(frequency_rotation, float):
		B_toroidal = 2*np.pi*frequency_rotation*electron_mass/electron_charge
		I_linking = 2*np.pi*radius_major*B_toroidal/mu_0
	if I_linking = None
		raise Exception('No information on target magnetic field. Pass B_toroidal or frequency_rotation or I_linking')
		
	if material == 'copper':
		specific_resistance = 1.68e-8 #Ohm*m @ 77°C 
		# heat capacity =
		# heat conduction =
	elif material == 'aluminum' or 'aluminium':
		specific_resistance = 3.875e-8 #Ohm*m @ 77°C (source: https://hypertextbook.com/facts/2004/ValPolyakov.shtml)
		# heat capacity = 
		# heat conduction = 
	if specific_resistance == None:
		raise Exception('Missing conductor material properties')
  

		calcEverything(radius_major = 0.5, radius_minor = 16*cm, 
