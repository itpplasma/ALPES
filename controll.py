import math
import sys

from variables import * 
from functions import *


''' is everything integer, what needs to be integer?
    is everything positiv, what needs to be positiv?
    is everything within boundaries?'''


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def input_validation():
    '''controll of the input variables'''

def check_input_variables():
    return True 

def check_precalculations():
    return True

def check_all():
    '''controlls, if integer values are integers, and none of the specifications is infringed'''
    if not is_integer(number_of_coils): 
        print("ERROR: number of coils is not an integer")
    if not is_integer(number_of_windings): 
        print("ERROR: number of windings is not an integer")
    return True

def give_system_status():
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
        try:
            print(name, " = ", value, value.unit)
        except AttributeError:
            print(name, " = ", value)
    print("")
    print("output values:")
    for name in output_variables:
        value = globals()[name]  # Get the variable value 
        try:
            print(name, " = ", value, value.unit)
        except AttributeError:
            print(name, " = ", value)
