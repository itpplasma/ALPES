import math
import sys
import numpy as np
import inspect
import seaborn as sns

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
    stellarator.length_of_circuit = stellarator.get_length_of_circuit()
    stellarator.volume_of_coils_within = stellarator.get_volume_of_coils_within()
    stellarator.I_coil = stellarator.get_I_coil()
    stellarator.I_winding = stellarator.get_I_winding()
    stellarator.resistance_per_circuit = stellarator.get_resistance_per_circuit()
    stellarator.resistance_per_winding = stellarator.get_resistance_per_winding()
    stellarator.voltage_per_circuit = stellarator.get_voltage_per_circuit()
    stellarator.voltage_per_winding = stellarator.get_voltage_per_winding()
    stellarator.power_per_winding = stellarator.get_power_per_winding()
    stellarator.power_per_circuit = stellarator.get_power_per_circuit()

def controll(stellarator):
    stellarator.controll_circumference_within()
    stellarator.controll_outer_dimension()
    stellarator.controll_number_of_windings_y()
    stellarator.controll_radius_major()
    stellarator.controll_geometry()
    return True

def test_major_radius(R_min, R_max, numer_of_testings):
    radii = np.linspace(R_min, R_max, numer_of_testings)
    for i in radii:
        print("###################################### Testing of major_radius = ", i, " #################################")
        stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=i,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, inner_radius=None, isolation_width = None)
        calculations(stellarator)
        stellarator.print_parameters()

def test_out(R_min, R_max, number_of_testings, specific_variable_name, radius_major_name):
    radii = np.linspace(R_min, R_max, number_of_testings)
    specific_variable_values = []  # List to store values of the specific variable

    for radius_major_value in radii:
        # Dynamically create the stellarator with the radius_major set
        stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                        max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                                        radius_minor=None, number_of_coils_per_circuit=None,
                                        number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                                        max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                                        winding_radius=None, inner_radius=None, isolation_width = None)
        
        # Dynamically set the radius_major attribute
        setattr(stellarator, radius_major_name, radius_major_value)
        
        print("###################################### Testing of", radius_major_name, "=", radius_major_value, "#################################")
        
        # Perform calculations to update the stellarator's attributes
        calculations(stellarator)

        # Access the specific variable dynamically
        specific_variable_value = getattr(stellarator, specific_variable_name)
        specific_variable_values.append(specific_variable_value)
        
        stellarator.print_parameters()
    
    # Plotting the specific variable against radius_major
    plt.figure(figsize=(10, 6))
    plt.plot(radii, specific_variable_values, marker='o')
    plt.title(f'{specific_variable_name.replace("_", " ").title()} vs {radius_major_name.replace("_", " ").title()}')
    plt.xlabel(radius_major_name.replace("_", " ").title())
    plt.ylabel(specific_variable_name.replace("_", " ").title())
    plt.grid(True)
    plt.show()


def test_number_of_coils_y(num_min, num_max):
    for i in range(num_min, num_max):
        print("###################################### Testing of number_of_coils_y = ", i, " #################################")
        stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y= i,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, inner_radius=None, isolation_width = None)
        calculations(stellarator)
        #stellarator.get_number_of_windings()
        stellarator.print_parameters()

def default_run():
    stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                 max_aspect_ratio=None, min_aspect_ratio=None, radius_major=None,
                 radius_minor=None, number_of_coils_per_circuit=None,
                 number_of_circuits=None, number_of_windings_x=None, number_of_windings_y=None,
                 max_current_per_m_2=None, specific_resistance=None, major_winding_radius=None,
                 winding_radius=None, inner_radius=None, isolation_width = None)
    calculations(stellarator)
    controll(stellarator)
    stellarator.print_parameters()

def interface():
    test_input = input("Do you want to test a certain value?[y/n]")
    if test_input.lower().startswith('n'):
        default_run()
    elif test_input.lower().startswith('y'):
        print("variables, which can be tested")
        signature = inspect.signature(StellaratorDesign)
        args_list = ["radius_major", "radius_minor", "frequency_rotation", "number_of_coils_per_circuit", "number_of_circuits", "number_of_windings_x", "number_of_windings_y", "major_winding_radius", "winding_radius", "inner_radius"]
        for no, arg in enumerate(args_list, start=1):
            print(f"[{no}] {arg}")
        try:
            set_test_input = int(input("Which value do you want to test? (put in number)"))
            if set_test_input < len(args_list):
                if args_list[set_test_input-1].startswith("number"):
                    min_value = int(input("min_value: "))
                    max_value = int(input("max_value: "))
                    test_out(min_value, max_value, max_value-min_value, "I_linking", args_list[set_test_input-1])
                R_min = float(input("R_min (in m): "))
                R_max = float(input("R_max (in m): "))
                number_of_tests = int(input("Number of tests: "))
                test_out(R_min, R_max, number_of_tests, "I_linking", args_list[set_test_input-1])
            else:
                print("out of bound")
                return interface()
        except ValueError:
            print("Please put in valid values")
            return interface()
    else:
        print("Please put in a valid answer [y/n]")
        return interface()


def test_parameters_for_different_winding(R_min, R_max, number_of_tests_R, param1_name, output_var_name):
    # Create a grid of values for the two parameters
    param1_values = np.linspace(R_min, R_max, number_of_tests_R)
    outer_radius_values = np.array([0.003, 0.004, 0.004])
    inner_radius_values = np.array([0.002, 0.0025, 0.003])
    
    # Initialize a matrix to store the output variable values
    output_values = np.zeros((number_of_tests_R, len(outer_radius_values)))

    stellarator_temp = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                         max_aspect_ratio=None, min_aspect_ratio=None,
                                         radius_major=None, radius_minor=None,
                                         number_of_coils_per_circuit=None, number_of_circuits=None,
                                         number_of_windings_x=None, number_of_windings_y=None,
                                         max_current_per_m_2=None, specific_resistance=None,
                                         major_winding_radius=None, winding_radius=None, inner_radius=None, isolation_width = None)

    # Check if param1_name need to be integers
    param1_is_integer = isinstance(getattr(stellarator_temp.geometry if hasattr(stellarator_temp.geometry, param1_name) else stellarator_temp, param1_name), int)
    
    # If the parameter needs to be an integer, convert the grid values to integers
    if param1_is_integer:
        if not isinstance(R_max, int) or not isinstance(R_min, int):
            print(param1_name,"needs to be fed integer values and is not")
            sys.exit()
        param1_values = np.linspace(R_min, R_max, number_of_tests_R).astype(int)
    
    for j, outer_radius_value in enumerate(outer_radius_values):
        # Create an instance of the StellaratorDesign class with the current parameter values
        stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                        max_aspect_ratio=None, min_aspect_ratio=None,
                                        radius_major=None, radius_minor=None,
                                        number_of_coils_per_circuit=None, number_of_circuits=None,
                                        number_of_windings_x=None, number_of_windings_y=None,
                                        max_current_per_m_2=None, specific_resistance=None,
                                        major_winding_radius=None, winding_radius=None, inner_radius=None, isolation_width = None)
        
        # Set the parameters dynamically
        setattr(stellarator, "outer_radius", outer_radius_value)
        setattr(stellarator, 'inner_radius', inner_radius_values[j])
        stellarator.print_parameters()


        for i, param1_value in enumerate(param1_values):
            setattr(stellarator, param1_name, param1_value)

            # Perform calculations to update the stellarator's attributes
            calculations(stellarator)
            
            # Access the output variable dynamically
            output_var_value = getattr(stellarator, output_var_name)
            output_values[i, j] = output_var_value
    
    # Create a heat map of the output variable
    plt.figure(figsize=(10, 8))
    sns.heatmap(output_values, xticklabels=np.round(outer_radius_values, 2), yticklabels=np.round(param1_values, 2), cmap='viridis')
    plt.title(f'Heatmap of {output_var_name.replace("_", " ").title()}')
    plt.xlabel("layout")
    plt.ylabel(param1_name.replace("_", " ").title())
    plt.show()


def test_two_parameters(R_min, R_max, number_of_tests_R, W_min, W_max, number_of_tests_W, param1_name, param2_name, output_var_name):
    # Create a grid of values for the two parameters
    param1_values = np.linspace(R_min, R_max, number_of_tests_R)
    param2_values = np.linspace(W_min, W_max, number_of_tests_W)
    
    # Initialize a matrix to store the output variable values
    output_values = np.zeros((number_of_tests_R, number_of_tests_W))

    stellarator_temp = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                         max_aspect_ratio=None, min_aspect_ratio=None,
                                         radius_major=None, radius_minor=None,
                                         number_of_coils_per_circuit=None, number_of_circuits=None,
                                         number_of_windings_x=None, number_of_windings_y=None,
                                         max_current_per_m_2=None, specific_resistance=None,
                                         major_winding_radius=None, winding_radius=None, inner_radius=None, isolation_width = None)

    # Check if param1_name and param2_name need to be integers
    param1_is_integer = isinstance(getattr(stellarator_temp.geometry if hasattr(stellarator_temp.geometry, param1_name) else stellarator_temp, param1_name), int)
    param2_is_integer = isinstance(getattr(stellarator_temp.geometry if hasattr(stellarator_temp.geometry, param2_name) else stellarator_temp, param2_name), int)

    # If the parameter needs to be an integer, convert the grid values to integers
    if param1_is_integer:
        if not isinstance(R_max, int) or not isinstance(R_min, int):
            print(param1_name,"needs to be fed integer values and is not")
            sys.exit()
        param1_values = np.linspace(R_min, R_max, number_of_tests_R).astype(int)
    if param2_is_integer:
        if not isinstance(W_max, int) or not isinstance(W_min, int):
            print(param1_name,"needs to be fed integer values and is not")
            sys.exit()
        param2_values = np.linspace(W_min, W_max, number_of_tests_W).astype(int)

    
    for i, param1_value in enumerate(param1_values):
        for j, param2_value in enumerate(param2_values):
            # Create an instance of the StellaratorDesign class with the current parameter values
            stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                            max_aspect_ratio=None, min_aspect_ratio=None,
                                            radius_major=None, radius_minor=None,
                                            number_of_coils_per_circuit=None, number_of_circuits=None,
                                            number_of_windings_x=None, number_of_windings_y=None,
                                            max_current_per_m_2=None, specific_resistance=None,
                                            major_winding_radius=None, winding_radius=None, inner_radius=None, isolation_width = None)
            
            # Set the parameters dynamically
            setattr(stellarator, param1_name, param1_value)
            setattr(stellarator, param2_name, param2_value)
            
            # Perform calculations to update the stellarator's attributes
            calculations(stellarator)
            
            # Access the output variable dynamically
            output_var_value = getattr(stellarator, output_var_name)
            output_values[i, j] = output_var_value
    
    # Create a heat map of the output variable
    plt.figure(figsize=(10, 8))
    sns.heatmap(output_values, xticklabels=np.round(param2_values, 2), yticklabels=np.round(param1_values, 2), cmap='viridis')
    plt.title(f'Heatmap of {output_var_name.replace("_", " ").title()}')
    plt.xlabel(param2_name.replace("_", " ").title())
    plt.ylabel(param1_name.replace("_", " ").title())
    plt.show()

# Example usage of the function
test_parameters_for_different_winding(0.5, 0.6, 20, 'radius_major','I_winding')
test_two_parameters(0.5, 0.6, 20, 5, 7, 3, 'radius_major', 'number_of_windings_x', 'I_winding')