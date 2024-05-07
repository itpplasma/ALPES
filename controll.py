import math
import sys

from variables import * 
from functions import *
from setters import *


''' is everything integer, what needs to be integer?
    is everything positiv, what needs to be positiv?
    is everything within boundaries?'''


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def do_calculations_1():
    set_max_current_per_winding()
    set_length_of_winding()
    length_of_coil = get_length_of_coil()
    length_of_circuit = get_length_of_circuit()
    current_within = get_current_within() #kA, within labels the stuff which is at positions < major radius
    radius_within = get_radius_within() #mm
    total_coil_radius_within = get_total_coil_radius_within() #mm
    total_coil_volume_within = get_total_coil_volume_within() #mm²
    number_of_coils = get_number_of_coils()

def check_all():
    '''controlls, if integer values are integers, and none of the specifications is infringed'''
    if not is_integer(number_of_coils): 
        print("ERROR: number of coils is not an integer")
    if not is_integer(number_of_windings): 
        print("ERROR: number of windings is not an integer")
    return True

def give_system_status(input_variables, output_variables):
    '''prints all variables into the command line'''
    print("#################################################################")
    print("")
    print("System Status")
    print("")
    print("#################################################################")
    print("")
    print("input values:")
    for name in input_variables:
        value = globals()[name]  # Get the variable value 
        print(name, " = ", value)
    print("")
    print("output values:")
    for name in output_variables:
        value = globals()[name]  # Get the variable value 
        print(name, " = ", value)
