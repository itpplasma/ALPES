import math
import sys
import numpy as np

# This is a test commit and that is a change
m = 1
cm = 0.01
mm = 0.001
mm2 = 1e-6
A = 1
kA = 1000
kW = 1000
GHz = 1e9
bar = 1e5

electron_mass = 9.1093837015e-31  # kg
electron_charge = 1.602176634e-19  # C
mu_0 = 1.25663706212e-6  # N*A^-2

'''from variables import *
from functions import *
from controll import *'''


def isNr(val):
	if isinstance(val, int) or isinstance(val, float):
		return True
	return False


def notNr(val):
	if isinstance(val, int) or isinstance(val, float):
		return False
	return True

'''def calcGeometry(
		material,
		isoThickness,
		casingThickness,
		radial_dim = None,
		poloidal_dim = None,
		windings = None,
		windings_x = None,
		windings_y = None,


):

	return(windingsPerCoil, resPerMetre, hydrResPerMetre)'''

def calcEverything(
		max_current_per_mm_2=float(50.),
		specific_resistance=None,
		radius_major=None,
		radius_minor=None,
		filament_length=None,
		number_coils=None,
		number_windings=None,
		material=None,
		B_toroidal=None,
		frequency_rotation=None,
		I_linking=None,
		conductor_crosssection=None,
		U_coil=None,
		I_winding=None,
		deltaT = None,
		pipeInnerDiam = None,
		dPancake_factor = None, #number of double pancakes in the coil crossection, same as winding nr in plasma direction div by 2
		I_winding_sum = None #I_winding times nr of windings
):
	'''This function will output all parameters of the stellarator coil design based on a set of keyword arguments that are passed to it.
	This set has to be complete in a sense that all other parameters can be determined from it.
	'''
	R_coil = None
	power_coil = None
	power_total = None

	# Geometry----------------------------------------------------------------
	if isNr(radius_minor) and isNr(filament_length):
		raise Exception('Both radius_minor and filament_length defined. remove one.')
	elif isNr(filament_length):
		radius_minor = filament_length/(2*np.pi) #virtual minor radius for further calculations
	if number_coils == None or (notNr(I_winding_sum) and notNr(radius_major)) or radius_minor == None:
		raise Exception(
			'Required geometric argument missing: number_coils or radius_major/I_winding_sum or radius_minor')

	# Field strength--------------------------------------------------
	if notNr(I_winding_sum):
		if isNr(B_toroidal):
			if I_linking != None or frequency_rotation != None:
				raise Exception(
					'To much information on target magnetic field. Pass B_toroidal or frequency_rotation or I_linking')
			I_linking = 2 * np.pi * radius_major * B_toroidal / mu_0
		if isNr(frequency_rotation):
			B_toroidal = 2 * np.pi * frequency_rotation * electron_mass / electron_charge
			I_linking = 2 * np.pi * radius_major * B_toroidal / mu_0

		if I_linking == None:
			raise Exception('No information on target magnetic field. Pass B_toroidal or frequency_rotation or I_linking or I_winding_sum')
	else:
		I_linking = I_winding_sum * number_coils #Patch to get the rest of code to work with I_winding_sum. Only single coil values are valid when using this approach!
		print('only single coil values are valid because I_winding_sum is used to compute the values for all coils!!!!')
	# Material------------------------------------------
	if material == 'copper':
		specific_resistance = 1.68e-8  # Ohm*m @ 77°C
	# heat capacity =
	# heat conduction =
	elif material == 'aluminum' or material == 'aluminium':
		specific_resistance = 3.875e-8  # Ohm*m @ 77°C (source: https://hypertextbook.com/facts/2004/ValPolyakov.shtml)
	# heat capacity =
	# heat conduction =
	if specific_resistance == None:
		raise Exception('Missing conductor material properties')
	# Voltage/Current/Resistance----------------------------------------------------------------------
	if isNr(I_winding) and isNr(U_coil) and isNr(conductor_crosssection):
		raise Exception('Too many arguments: Specifiy 2 off: I_winding or U_coil or conductor_crosssection')
	# linking current dependent geometry--------------------------------
	if isNr(number_windings) and isNr(I_winding):
		raise Exception('Too many arguments: number_windings or I_winding')
	if notNr(number_windings) and notNr(I_winding):
		raise Exception('Too few arguments: number_windings or I_winding')
	if isNr(I_winding):
		number_windings = np.ceil(I_linking / number_coils / I_winding)
		I_winding = I_linking / number_coils / number_windings
	elif isNr(number_windings):
		I_winding = I_linking / number_coils / number_windings
	len_coil = 2 * np.pi * radius_minor * number_windings
	# Voltage/Current/Resistance----------------------------------------------------------------------
	if isNr(I_winding) and isNr(conductor_crosssection):
		R_coil = len_coil * specific_resistance / conductor_crosssection
		U_coil = I_winding * R_coil
	if isNr(I_winding) and isNr(U_coil):
		R_coil = U_coil / I_winding
		conductor_crosssection = len_coil * specific_resistance / R_coil
	if isNr(U_coil) and isNr(conductor_crosssection):
		R_coil = len_coil * specific_resistance / conductor_crosssection
		I_winding = U_coil / R_coil
	if notNr(R_coil):
		raise Exception('Specifiy 2 off: I_winding or U_coil or conductor_crosssection')
	power_coil = U_coil * I_winding
	power_total = power_coil * number_coils

	if isNr(deltaT):
		c_water = 4184 #J /kg/K
		massFlow = power_total/c_water/deltaT #kg/s
		massFlowperCoil = massFlow / number_coils
		print('total mass flow: ', massFlow, ' kg/s')
		print('mass flow per coil: ', massFlowperCoil, ' kg/s')

	p_drop_per_coil = None
	if isNr(pipeInnerDiam) and isNr(deltaT):
		p_drop_per_coil = pressureDrop(pipeInnerDiam, massFlowperCoil, len_coil)
		print('pressure drop per whole coil: ', p_drop_per_coil , ' bar')
	p_drop_per_dPancake = None
	if isNr(p_drop_per_coil) and isNr(dPancake_factor):
		p_drop_per_dPancake = pressureDrop(pipeInnerDiam, massFlowperCoil/dPancake_factor, len_coil/dPancake_factor)
		print('pressure drop per double Pancake: ', p_drop_per_dPancake, ' bar')

	print('B_toroidal: ', B_toroidal, ' T')
	print('I_linking: ', I_linking / kA, ' kA')
	print('number of coils: ', number_coils)
	print('number of windings per coil: ', number_windings)
	if isNr(radius_major):
		print('Outer Diameter: ', radius_major + radius_minor, ' m')
	print('Conductor Crosssection: ', conductor_crosssection / (mm ** 2), 'mm^2')
	print('Coil resistance: ', R_coil, ' Ohm')
	print('Coil Voltage: ', U_coil, ' V')
	print('Conductor Length per Coil: ', len_coil, ' m')
	print('Winding Current: ', I_winding, ' A')
	print('Coil Power: ', power_coil / kW, ' kW')
	print('Total Power: ', power_total / kW, ' kW')

	return p_drop_per_coil, p_drop_per_dPancake, power_coil, I_winding


def pipeCondCrossection(outer, thickness):
	if thickness >= outer/2:
		raise Exception('Wall to thick, no hole in pipe :(')
	return((outer/2)**2-(outer/2 - thickness)**2)*np.pi

def pressureDrop(pipeInnerDiam, massFlow, length): #m , kg/s , m
	import pressure_loss_calculator.PressureLossMod as PL
	return(PL.PressureLoss_DW(length, pipeInnerDiam/mm, massFlow, 20, 0.005)) #fixed at 20°C and roughness of 5um


if __name__ == "__main__":
	calcEverything(radius_major=0.5, filament_length=176.35 * cm, I_winding_sum=14690*A , number_coils=12, conductor_crosssection=pipeCondCrossection(6*mm,1*mm),
				  number_windings=48, dPancake_factor=3, material='copper', frequency_rotation=2.45 * GHz, deltaT=25, pipeInnerDiam=4*mm)