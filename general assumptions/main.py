import math
import sys
import numpy as np
import inspect

from definitions import *
from functions import *

def main():
    coil_tor_max_width = 0.05  # m
    outer_radius_values = np.array([4.75, 6, 6.35, 6.35, 8, 8, 8, 10]) * 10e-4 /2
    thick_list = np.array([0.75, 1, 0.79, 1, 1, 1.5, 2, 2]) * 10e-4
    outputs_dependant_on_desing_of_coils = (['I_winding','cond_volume', 'power_per_circuit', 'voltage_per_circuit'])
    outputs_dependant_on_arrangement_of_coils = (['d_pressure'])
    test(outputs_dependant_on_desing_of_coils, outputs_dependant_on_arrangement_of_coils, outer_radius_values, thick_list, coil_tor_max_width)
    #test_two_parameters(0.5, 0.6, 20, 5, 7, 3, 'radius_major', 'number_of_windings_x', 'I_winding')
    #interface()
main()