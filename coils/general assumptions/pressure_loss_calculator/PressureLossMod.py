# Pipe pressure loss calculator for a circular pipe, full flow water (SI Units) - Darcy-Weisbach
#   prepared by Hakan İbrahim Tol, PhD
#modified 05/2024 by D. Hipp to work fom a single file
import math
def f_Clamond(R, K=0):
		# DWc = COLEBROOK(R,K) fast, accurate and robust computation of the
		#     Darcy-Weisbach friction factor F according to the Colebrook equation:
		#                             -                       -
		#      1                     |    K        2.51        |
		#  ---------  =  -2 * Log_10 |  ----- + -------------  |
		#   sqrt(DWc)                |   3.7     R * sqrt(DWc) |
		#                             -                       -
		# INPUT:
		#   R : Reynolds' number (should be >= 2300).
		#   K : Equivalent sand roughness height divided by the hydraulic
		#       diameter (default K=0).
		#
		# OUTPUT:
		#   DWc : Darcy Weisbach Friction factor.
		#
		# FORMAT:
		#   R, K and DWc are ONLY scalars in this Python Module
		#
		# ACCURACY:
		#   Around machine precision forall R > 3 and forall 0 <= K,
		#   i.e. forall values of physical interest.
		#
		# EXAMPLE: DWc = f_Clamond(7e5,0.01)
		#
		# Method: Quartic iterations.
		# Reference: http://arxiv.org/abs/0810.5564
		# Read this reference to understand the method and to modify the code.

		# Author: D. Clamond, 2008-09-16.
		# Modified for Python by Hakan İbrahim Tol, PhD, 2019-07-02

		# Check for errors.
		if R < 2300:
				warnings.warn('The Colebrook equation is valid for Reynolds'' numbers >= 2300.')

		if K < 0:
				warnings.warn('The relative sand roughness must be non-negative.')

				# Initialization.
		X1 = K * R * 0.123968186335417556  # X1 <- K * R * log(10) / 18.574.
		X2 = math.log(R) - 0.779397488455682028  # X2 <- log( R * log(10) / 5.02

		# Initial guess.
		DWc = X2 - 0.2

		# First iteration.
		E = (math.log(X1 + DWc) - 0.2) / (1 + X1 + DWc)
		DWc = DWc - (1 + X1 + DWc + 0.5 * E) * E * (X1 + DWc) / (1 + X1 + DWc + E * (1 + E / 3))

		# Second iteration (remove the next two lines for moderate accuracy).
		E = (math.log(X1 + DWc) + DWc - X2) / (1 + X1 + DWc)
		DWc = DWc - (1 + X1 + DWc + 0.5 * E) * E * (X1 + DWc) / (1 + X1 + DWc + E * (1 + E / 3))

		# Finalized solution.
		DWc = 1.151292546497022842 / DWc  # DWc <- 0.5 * log(10) / DWc;
		DWc = DWc * DWc  # DWc <- Friction factor.

		return DWc
 #from SubFunctions import Reynolds
def Reynolds(mFlow, D, T):
	# Calculates the Reynolds Number for a circular pipe (water)
	
	# INPUTS (scalar or vector)
	#   MF  : Mass flow                     [kg/s]
	#   D   : Inner diameter of the pipe	[mm]
	#   T   : Temperature of the water      [°C]
	
	P = 8 * 100  # [kPa] Pressure
	
	from math import pi
	from XSteamPython import my_pT
	
	Reynolds = 4 * mFlow / (pi * (D / 1000) * my_pT(P, T))
	
	return Reynolds

def PressureLoss_DW(L,D,mFlow,T,aRou):
    # Inputs
    #   L       : Length of pipe segment        [m]
    #   D       : Pipe inner diameter           [mm]
    #   aRou    : Absolute roughness of pipe    [mm]
    #   mFlow   : Mass flow rate                [kg/s]
    #   T       : Water temperature             [ºC]

    # Output
    #   PL      : Pressure loss                 [bar]

    #from DarcyFrictionFactor import f_Clamond
    #   prepared by Hakan İbrahim Tol, PhD on 02/07/2019

    import math
    import warnings

    # via Clamond algorithm _ Copied,Modified,Pasted!
    
   

    import XSteamPython as XSteam
    from math import pi

    # Reynolds number [-]
    Re=Reynolds(mFlow,D,T)

    # Darcy friction factor, f
    if Re<2300:
        f=64/Re
    else:
        f=f_Clamond(Re,aRou/D)

    PL=(8*f*L*mFlow**2/(pi**2*XSteam.rhoL_T(T)**2*9.81*(D/1000)**5))/10.1971621297792

    return PL
