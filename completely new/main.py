import math
import sys
import numpy as np
import inspect

from definitions import *
from functions import *

def main():
    names_of_outputs = (['I_winding', 'cond_volume', 'power_per_circuit', 'voltage_per_circuit', 'get_d_pressure'])
    test(4, 8, 5, 'number_of_windings_x', names_of_outputs)
    #test_two_parameters(0.5, 0.6, 20, 5, 7, 3, 'radius_major', 'number_of_windings_x', 'I_winding')
    #interface()
main()