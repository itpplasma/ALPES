##### some functions for variable handling #####
class UnitFloat(float):
    '''defines variables with a unit; if just the variable is used, it gives back the value; if variable.unit
    is used, it give back the unit.'''
    def __new__(self, value, unit=None):
       return float.__new__(self, value)

    def __init__(self, value, unit=None):
        self.unit = unit

def get_global_variables():
    '''Gives a list of the names of all global variables'''
    global_vars = []
    for var_name, var_value in globals().items():
        # Überprüfen, ob die Variable nicht spezielle Systemvariablen oder Funktionen sind
        if not var_name.startswith("__") and not callable(var_value):
            global_vars.append(var_name)
    return global_vars

# B-field specifications
B_middle = float(87.3) # mT
mu_0 = float(1.25663706212*10**(-6)) #magnetic permeability, N/A²

# Dimension restrictions
max_radius = float(0.8) #meter
max_height = float(0.8) #meter
max_aspect_ratio = float(10.) #no dimension
min_aspect_ratio = float(6.) #no dimension
major_radius_plasma = float(0.5) #meter
minor_radius_plasma = float(80.) #mm

# coil assumptions
number_of_coils_per_circuit = int(10)
number_of_circuits = int(4)
number_of_windings = int(12)
number_of_windings_x = int(3)
number_of_wingings_y = int(4)
max_current_per_mm_2 = float(50.) #A/mm²
specific_resistance = float(0.) #
major_winding_radius = float(0.16) #m
winding_radius = float(0.) 
total_winding_radius = float(0.) #mm, coil + cooling 

input_variables = get_global_variables()

# calculated from basis variables
max_current_per_winding = float(0.) #A
length_of_winding = float(0.)#m
length_of_coil = float(0.) #m
length_of_circuit = float(0.) #m
current_within = float(0.) #kA, within labels the stuff which is at positions < major radius
radius_within = float(0.) #mm
total_coil_radius_within = float(0.) #mm
total_coil_volume_within = float(0.) #mm²
number_of_coils = int(0)

#calculated from precalculations
current_per_coil = float(0.) #kA
current_per_winding = float(0.) #kA
volume_within = float(0.) #mm²
aspect_ratio = float(0.) #no dimension
resistance_per_circuit = float(0.) #ohm
voltage_per_circuit = float(0.) #Volt

#make a list of all variables
all_variables =  get_global_variables()
output_variables = all_variables[len(input_variables)+1:len(all_variables)]