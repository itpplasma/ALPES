import math
import sys
import numpy as np
import inspect

from definitions import *

def calculations(stellarator):
    stellarator.major_winding_radius = stellarator.get_major_winding_radius()
    stellarator.len_of_winding = stellarator.get_len_of_winding()
    stellarator.B_toroidal = stellarator.get_B_toroidal()
    stellarator.max_I_winding = stellarator.get_max_I_winding()
    stellarator.len_coil = stellarator.get_len_coil()
    stellarator.number_of_coils = stellarator.get_number_of_coils()
    stellarator.circumference_within = stellarator.get_circumference_within()
    stellarator.I_linking = stellarator.get_I_linking()
    stellarator.aspect_ratio = stellarator.get_aspect_ratio()
    stellarator.radius_within = stellarator.get_radius_within()
    stellarator.total_coil_volume_within = stellarator.get_total_coil_volume_within()
    stellarator.length_of_circuit = stellarator.get_length_of_circuit()
    stellarator.volume_of_coils_within = stellarator.get_volume_of_coils_within()
    stellarator.total_coil_radius_within = stellarator.get_total_coil_radius_within()
    stellarator.I_coil = stellarator.get_I_coil()
    stellarator.I_winding = stellarator.get_I_winding()
    stellarator.resistance_per_circuit = stellarator.get_resistance_per_circuit()
    stellarator.resistance_per_winding = stellarator.get_resistance_per_winding()
    stellarator.voltage_per_circuit = stellarator.get_voltage_per_circuit()
    stellarator.voltage_per_winding = stellarator.get_voltage_per_winding()
    stellarator.power_per_winding = stellarator.get_power_per_winding()
    stellarator.power_per_circuit = stellarator.get_power_per_circuit()

def test_major_radius(R_min, R_max, numer_of_testings):
    radii = np.linspace(R_min, R_max, numer_of_testings)
    for i in radii:
        print("###################################### Testing of major_radius = ", i, " #################################")
        stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=i,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, cooling_radius=None)
        calculations(stellarator)
        #stellarator.get_number_of_windings()
        stellarator.print_parameters()

def default_run():
    stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, cooling_radius=None)
    calculations(stellarator)
    stellarator.print_parameters()

def interface():
    test_input = input("Do you want to test a certain value?[y/n]")
    if test_input.lower().startswith('n'):
        default_run()
    elif test_input.lower().startswith('y'):
        print("variables, which can be tested")
        signature = inspect.signature(StellaratorDesign)
        args_list = [param.name for param in signature.parameters.values()]
        for i in args_list:
            print(i)
        set_test_input = input("Which value do you want to test?")
        if set_test_input == "radius_major":
            print("in what range would you like to test?")
            try:
                R_min = float(input("R_min (in m): "))
                R_max = float(input("R_max (in m): "))
                number_of_tests = int(input("Number of tests: "))
            except ValueError:
                print("Please put in valid values")
                return interface()
            test_major_radius(R_min, R_max, number_of_tests)
        else:
            print("function not implemented yet")
    else:
        print("Please put in a valid answer [y/n]")
        return interface()