from variables import * 
from setters import *
from functions import *
from setters import *


def get_global_variables():
    '''Gives a list of the names of all global variables'''
    global_vars = []
    for var_name, var_value in globals().items():
        # Überprüfen, ob die Variable nicht spezielle Systemvariablen oder Funktionen sind
        if not var_name.startswith("__") and not callable(var_value):
            global_vars.append(var_name)
    return global_vars