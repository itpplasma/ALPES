import math
import sys
import numpy as np
import inspect
import os
import copy
import seaborn as sns
import matplotlib.pyplot as plt
import pressure_loss_calculator.PressureLossMod as PL

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
    stellarator.massflow = stellarator.get_massflow()
    stellarator.d_pressure = stellarator.get_d_pressure()
    stellarator.cond_volume = stellarator.get_cond_volume()

def controll(stellarator):
    #stellarator.controll_circumference_within()
    stellarator.controll_outer_dimension()
    stellarator.controll_number_of_windings_y()
    stellarator.controll_radius_major()
    stellarator.controll_geometry()
    return True

def sorting(n_total, out_put_put, output_var_names):
    # sort the data so that N is in order for a nicer plot
    #sort N and get the list of indices
    sorting_help = np.zeros(len(n_total))
    for i in range(len(sorting_help)):
        sorting_help[i] = n_total[i]
    sorting_args = np.argsort(sorting_help)
    sorting_help = np.sort(sorting_help)
    n_total = sorting_help.tolist()

    #sort the data
    for output_var_name in output_var_names:
        sorted_out_put_put = copy.deepcopy(out_put_put[output_var_name]) 
        for (x, y, value) in out_put_put[output_var_name]:
            sorted_index = sorting_args[x]
            if x != sorted_index:
                value_help = float(value)
                sorted_out_put_put[x+y*len(n_total)][2][0] = out_put_put[output_var_name][sorted_index+y*len(n_total)][2]
        out_put_put[output_var_name] = sorted_out_put_put
    return n_total, out_put_put


def test(output_var_names):
    coil_tor_max_width = 0.05  # m
    n_tor_min = 2
    n_pol_min = 2

    # Create a grid of values for the parameter
    outer_radius_values = np.array([4.75, 6, 6.35, 6.35, 8, 8, 8, 10]) * 10e-4 /2
    thick_list = np.array([0.75, 1, 0.79, 1, 1, 1.5, 2, 2]) * 10e-4 /2
    inner_radius_values = outer_radius_values - thick_list

    
    # Initialize matrices to store the output variable values
    output_values = {output_var_name: [] for output_var_name in output_var_names}

    stellarator_temp = StellaratorDesign(material="copper", diam_max=None, max_height=None,
                                         max_aspect_ratio=None, min_aspect_ratio=None,
                                         radius_major=None, radius_minor=None,
                                         number_of_coils_per_circuit=None, number_of_circuits=None,
                                         number_of_windings_x=None, number_of_windings_y=None,
                                         max_current_per_m_2=None, specific_resistance=None,
                                         major_winding_radius=None, winding_radius=None, inner_radius=None, 
                                         isolation_width=None, geometry=None)
    
    n_tor_max = np.zeros((len(outer_radius_values), 1))
    for i in range(len(outer_radius_values)):
        n_tor_max[i] = int(coil_tor_max_width / (stellarator_temp.geometry.spacing_between_windings + outer_radius_values[i]))
        if n_tor_max[i] % 2 != 0:
            n_tor_max[i] -= 1
    
    n_pol_max = 6#n_tor_max[0] 
    n_tor = np.linspace(n_tor_min, n_tor_max[0], int((n_tor_max[0] - n_tor_min) / 2 + 1))
    n_pol = np.linspace(n_pol_min, n_pol_max, int((n_pol_max - n_pol_min) + 1))
    collect_n_total = []

    for j, outer_radius_value in enumerate(outer_radius_values):
        # Create an instance of the StellaratorDesign class with the current parameter values
        collect_n_total.clear()
        stellarator = StellaratorDesign(material="copper", diam_max=None, max_height=None,
                                        max_aspect_ratio=None, min_aspect_ratio=None,
                                        radius_major=None, radius_minor=None,
                                        number_of_coils_per_circuit=None, number_of_circuits=None,
                                        number_of_windings_x=None, number_of_windings_y=None,
                                        max_current_per_m_2=None, specific_resistance=None,
                                        major_winding_radius=None, winding_radius=None, inner_radius=None, 
                                        isolation_width=None, geometry=None)
        
        # Set the parameters dynamically
        setattr(stellarator, "outer_radius", outer_radius_value)
        setattr(stellarator, 'inner_radius', inner_radius_values[j])

        for i, n_tor_value in enumerate(n_tor):
            for k, n_pol_value in enumerate(n_pol):
                N = n_tor_value * n_pol_value
                if N not in collect_n_total and 12 < N < 60:                    
                    collect_n_total.append(N)
                    setattr(stellarator, "number_of_windings_x", n_pol_value)
                    setattr(stellarator, "number_of_windings_y", n_tor_value)

                    # Perform calculations to update the stellarator's attributes
                    calculations(stellarator)
            
                    # Access and store the output variables dynamically
                    for output_var_name in output_var_names:
                        output_var_value = getattr(stellarator, output_var_name)
                        output_values[output_var_name].append((len(collect_n_total)-1, j, output_var_value))

    collect_n_total, output_values = sorting(collect_n_total, output_values, output_var_names)

    # Create directory for heatmaps
    heatmap_dir = 'heatmaps'
    os.makedirs(heatmap_dir, exist_ok=True)

    # Create and save a graph for each output variable
    xticks = [f"r_i = {inner_radius_values[0]}, r_o = {outer_radius_values[0]}",
              f"r_i = {inner_radius_values[1]}, r_o = {outer_radius_values[1]}",
              f"r_i = {inner_radius_values[2]}, r_o = {outer_radius_values[2]}"]
    
    for output_var_name in output_var_names:
        data_matrix = np.zeros((len(collect_n_total), len(outer_radius_values)))
        for (x, y, value) in output_values[output_var_name]:
            #print(x, y)
            data_matrix[x, y] = value

        plt.figure(figsize=(10, 4))  
        ax = sns.heatmap(data_matrix, xticklabels=xticks, yticklabels=collect_n_total, cmap='viridis')
        plt.title(f'{output_var_name.replace("_", " ").title()}')
        plt.xlabel("Layout")
        plt.ylabel("Number of Windings per coil")
        plt.tight_layout()
        
        plt.savefig(f'{heatmap_dir}/{output_var_name}.png')
        plt.close()

    # Create and save a 1D graph for each output variable and layout
    #for j, outer_radius_value in enumerate(outer_radius_values):
    #    # Create directory for 1D graphs of the specific inner and outer radius combination
    #    graph_dir = f'graphs/r_i_{inner_radius_values[j]}_r_o_{outer_radius_value}'
    #    os.makedirs(graph_dir, exist_ok=True)
    #    
    #    for output_var_name in output_var_names:
    #        plt.figure(figsize=(10, 4))  # Reduced height
    #        y_values = [value for (i, y, value) in output_values[output_var_name] if y == j]
    #        plt.plot(param1_values, y_values[:len(param1_values)], marker='o')
    #        plt.title(f'{output_var_name.replace("_", " ").title()} vs {param1_name.replace("_", " ").title()} for r_i = {inner_radius_values[j]}, r_o = {outer_radius_value}')
    #        plt.xlabel(param1_name.replace("_", " ").title())
    #        plt.ylabel(output_var_name.replace("_", " ").title())
    #        plt.grid(True)
    #        
    #        plt.savefig(f'{graph_dir}/{output_var_name}.png')
    #        plt.close()
