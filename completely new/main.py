import math
import sys
import numpy as np
import inspect

from definitions import *
from functions import *

def main():
    outputs_dependant_on_number_of_coils = (['I_winding'])
    outputs_dependant_on_desing_of_coils = (['cond_volume', 'power_per_circuit', 'voltage_per_circuit'])
    outputs_dependant_on_arrangement_of_coils = (['d_pressure'])
    test(outputs_dependant_on_desing_of_coils)
    #test_two_parameters(0.5, 0.6, 20, 5, 7, 3, 'radius_major', 'number_of_windings_x', 'I_winding')
    #interface()
main()