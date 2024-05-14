# Pipe pressure loss - Circular pipe, full flow water in SI Units
# based on Darcy-Weisbach, using Clamond algorithm for friction factor

# Inputs
D=4.75-(2*0.71)      # [mm]      Pipe diameter
aRou=0.001    # [mm]      Absolute roughness
mFlow=0.02  # [kg/s]    Mass flow rate
T=20        # [ºC]      Water temperature
L=10        # [m]       Pipe length

## Main Function that returns the pressure loss
import pressure_loss_calculator.PressureLossMod as PL

print("Pressure Loss [bar] = ", PL.PressureLoss_DW(L,D,mFlow,T,aRou))

## Other Functions

# Function that returns Reynolds number
import pressure_loss_calculator.SubFunctions as SF
Re=SF.Reynolds(mFlow,D,T)
print("Reynolds = ", Re)

# Functions that return Darcy Friction Factor, f
import pressure_loss_calculator.DarcyFrictionFactor as DF

print("Darcy Friction Factor via ColebrookWhite = ", DF.f_ColebrookWhite(D,Re,aRou))
print("Darcy Friction Factor via SwameeJain = ", DF.f_SwameeJain(D,Re,aRou))
print("Darcy Friction Factor via Clamond = ", DF.f_Clamond(Re,aRou/D))
