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
B_middle = UnitFloat(87.3, "milli Tesla") # mT
mu_0 = UnitFloat(1.25663706212*10**(-6), "Newton per Ampere squared") #magnetic permeability, N/A²

# Dimension restrictions
max_radius = UnitFloat(0.8, "meter") #meter
max_height = UnitFloat(0.8, "meter") #meter
max_aspect_ratio = UnitFloat(10.) #no dimension
min_aspect_ratio = UnitFloat(6.) #no dimension
major_radius_plasma = UnitFloat(0.5, "meter") #meter
minor_radius_plasma = UnitFloat(80., "milli meter") #mm

# coil assumptions
number_of_coils_per_circuit = int(10)
number_of_circuits = int(4)
number_of_windings = int(12)
number_of_windings_x = int(3)
number_of_wingings_y = int(4)
max_current_per_mm_2 = UnitFloat(50., "Ampere per square milli meter") #A/mm²
specific_resistance = UnitFloat(0.) #
major_winding_radius = UnitFloat(160., "milli meter") #mm
winding_radius = UnitFloat(0., "milli meter")
total_winding_radius = UnitFloat(0., "milli meter") #mm, coil + cooling 

input_variables = get_global_variables()

# calculated from basis variables
max_current_per_winding = UnitFloat(0., "Ampere") #A
length_of_winding = UnitFloat(0., "meter") #m
length_of_coil = UnitFloat(0., "meter") #m
length_of_circuit = UnitFloat(0., "meter") #m
current_within = UnitFloat(0., "kilo Ampere") #kA, within labels the stuff which is at positions < major radius
radius_within = UnitFloat(0., "milli meter") #mm
total_coil_radius_within = UnitFloat(0., "milli meter") #mm
total_coil_volume_within = UnitFloat(0., "milli meter squared") #mm²
number_of_coils = int(0)

#calculated from precalculations
current_per_coil = UnitFloat(0., "kilo Ampere") #kA
current_per_winding = UnitFloat(0., "kilo Ampere") #kA
volume_within = UnitFloat(0., "milli meter squared") #mm²
aspect_ratio = UnitFloat(0.) #no dimension
resistance_per_circuit = UnitFloat(0., "Ohm") #ohm
voltage_per_circuit = UnitFloat(0., "Volt") #Volt

#make a list of all variables
all_variables =  get_global_variables()
output_variables = all_variables[len(input_variables)+1:len(all_variables)]