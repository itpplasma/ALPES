import math
import sys
import numpy as np
import inspect
import os
import copy
import seaborn as sns
import matplotlib.pyplot as plt
import pressure_loss_calculator.PressureLossMod as PL
from matplotlib.colors import LogNorm

from crosssection import *
from definitions import *

def calculations(stellarator):
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
    # Sort N and get the list of indices
    sorting_help = np.zeros(len(n_total))
    for i in range(len(sorting_help)):
        sorting_help[i] = n_total[i]
    sorting_args = np.argsort(sorting_help)
    sorting_help = np.sort(sorting_help)
    n_total = sorting_help.tolist()

    # Sort the data
    for output_var_name in output_var_names:
        sorted_out_put_put = []
        for j in range(int(len(out_put_put[output_var_name])/len(sorting_args))):
            for i,idx in enumerate(sorting_args):
                sorted_out_put_put.append((i,out_put_put[output_var_name][i+j*len(sorting_args)][1],out_put_put[output_var_name][idx+j*len(sorting_args)][2]))
        out_put_put[output_var_name] = sorted_out_put_put

    return n_total, out_put_put

def test(output_var_names, output_dep_var_names, outer_radius_values, thick_list, coil_tor_max_width):
    n_tor_min = 4
    n_pol_min = 2
    N_min = 12
    N_max = 60
    inner_radius_values = outer_radius_values - thick_list

    stellarator_temp = StellaratorDesign(material="copper", diam_max=None, max_height=None,
                                         max_aspect_ratio=None, min_aspect_ratio=None,
                                         radius_major=None, radius_minor=None,
                                         number_of_coils_per_circuit=None, number_of_circuits=None,
                                         number_of_windings_x=None, number_of_windings_y=None,
                                         max_current_per_m_2=None, specific_resistance=None, winding_radius=None, inner_radius=None, 
                                         isolation_width=None, geometry=None)
    
    # get the number of windings in toroidal and poloidal direction which should be tested
    n_tor_max = np.zeros((len(outer_radius_values), 1))
    for i in range(len(outer_radius_values)):
        n_tor_max[i] = int(coil_tor_max_width / (stellarator_temp.geometry.spacing_between_windings + outer_radius_values[i]))
        if n_tor_max[i] % 2 != 0:
            n_tor_max[i] -= 1
    
    n_pol_max = n_tor_max[0]
    n_tor = np.linspace(n_tor_min, int(n_tor_max[0]), int((n_tor_max[0] - n_tor_min) / 2 + 1), dtype=int)
    n_pol = np.linspace(n_pol_min, n_pol_max, int((n_pol_max - n_pol_min) + 1), dtype=int)
    collect_n_total = []

    # Initialize matrices to store the output variable values
    output_values = {output_var_name: [] for output_var_name in output_var_names}
    output_dep_values = np.zeros((len(output_dep_var_names),len(outer_radius_values), len(n_tor),len(n_pol)))
    
    # Create directory for heatmaps
    heatmap_dir = 'heatmaps'
    pressure_dir = 'heatmaps/pressure'
    os.makedirs(heatmap_dir, exist_ok=True)
    os.makedirs(pressure_dir, exist_ok=True)

    for j, outer_radius_value in enumerate(outer_radius_values):
        # Create an instance of the StellaratorDesign class with the current parameter values
        collect_n_total.clear()
        stellarator = StellaratorDesign(material="copper", diam_max=None, max_height=None,
                                        max_aspect_ratio=None, min_aspect_ratio=None,
                                        radius_major=None, radius_minor=None,
                                        number_of_coils_per_circuit=None, number_of_circuits=None,
                                        number_of_windings_x=None, number_of_windings_y=None,
                                        max_current_per_m_2=None, specific_resistance=None, winding_radius=None, inner_radius=None, 
                                        isolation_width=None, geometry=None)
        
        # Set the parameters dynamically
        setattr(stellarator, "outer_radius", outer_radius_value)
        setattr(stellarator, 'inner_radius', inner_radius_values[j])
        crosssection_cPipes(outer_radius_value*2, thick_list[j], "copper", 
                iso_thickness = stellarator.geometry.spacing_between_windings, casing_thickness = 0.002, mass_flow=0,
                windings_pol=int(4), windings_tor=int(4))
        for i, n_tor_value in enumerate(n_tor):
            for k, n_pol_value in enumerate(n_pol):
                N = n_tor_value * n_pol_value
                # Change the number of windings un poloidal and toroidal direction
                setattr(stellarator, "number_of_windings_x", n_pol_value)
                setattr(stellarator, "number_of_windings_y", n_tor_value)
                # Perform calculations to update the stellarator's attributes
                calculations(stellarator)
                for h in range(len(output_dep_var_names)):
                    output_dep_values[h][j][i][k] = getattr(stellarator, output_dep_var_names[h])
                if N not in collect_n_total and 12 < N < 60:  
                    """save the attributes which are not dependant on the arrangement of coils"""                  
                    collect_n_total.append(N)
                    # Access and store the output variables dynamically
                    for output_var_name in output_var_names:
                        output_var_value = getattr(stellarator, output_var_name)
                        output_values[output_var_name].append((len(collect_n_total)-1, j, output_var_value))
                #if n_pol_value == n_tor_value == 4:
                    #stellarator.print_parameters()

    collect_n_total, output_values = sorting(collect_n_total, output_values, output_var_names)

    # Create and save a graph for each output variable
    xticks = []
    for i in range(len(outer_radius_values)):
        xticks.append(f"r_i = {round(inner_radius_values[i]*1000, 2)}, r_o = {round(outer_radius_values[i]*1000, 2)}")
    
    for output_var_name in output_var_names:
        if output_var_name != "I_winding" and output_var_name != "voltage_per_circuit":
            data_matrix = np.zeros((len(collect_n_total), len(outer_radius_values)))
            for (x, y, value) in output_values[output_var_name]:
                data_matrix[x, y] = value

            plt.figure(figsize=(8, 5))  
            ax = sns.heatmap(data_matrix, xticklabels=xticks, yticklabels=collect_n_total, cmap='viridis')
            plt.title(f'{output_var_name.replace("_", " ").title()} [W]')
            plt.xlabel("Layout [mm]")
            plt.ylabel("Number of Windings per coil")
            plt.tight_layout()

            plt.savefig(f'{heatmap_dir}/{output_var_name}.png')
            plt.close()
        elif output_var_name == "voltage_per_circuit":
            data_matrix = np.zeros((1,len(outer_radius_values)))
            for (x, y, value) in output_values[output_var_name]:
                data_matrix[0, y] = value

            plt.figure(figsize=(4, 4))  
            ax = sns.heatmap(data_matrix, xticklabels=xticks, cmap='viridis')
            plt.title(f'{output_var_name.replace("_", " ").title()} [V]')
            plt.xlabel("Layout [mm]")
            plt.tight_layout()

            plt.savefig(f'{heatmap_dir}/{output_var_name}.png')
            plt.close()
        else:
            data_matrix = np.zeros((len(collect_n_total), 1))
            for (x, y, value) in output_values[output_var_name]:
                data_matrix[x, 0] = value

            plt.figure(figsize=(4, 4))  
            ax = sns.heatmap(data_matrix, yticklabels=collect_n_total, cmap='viridis')
            plt.title(f'{output_var_name.replace("_", " ").title()} [A]')
            plt.ylabel("Number of Windings per coil")
            plt.tight_layout()

            plt.savefig(f'{heatmap_dir}/{output_var_name}.png')
            plt.close()
    
    for h, output_var_name in enumerate(output_dep_var_names):
        for j in range(len(outer_radius_values)):
            data_matrix = np.zeros((len(n_pol), len(n_tor)))
            for k, n_pol_value in enumerate(n_pol):
                for i, n_tor_value in enumerate(n_tor):
                    tor_width = float((stellarator_temp.geometry.spacing_between_windings + outer_radius_values[j]) * n_tor[i] + stellarator_temp.geometry.spacing_between_windings)
                    pol_width = float((stellarator_temp.geometry.spacing_between_windings + outer_radius_values[j]) * n_pol[k] + stellarator_temp.geometry.spacing_between_windings )
                    #print(j,output_values["voltage_per_circuit"][j*len(collect_n_total)])
                    if coil_tor_max_width > tor_width and output_dep_values[h][j][i][k]<4 and coil_tor_max_width > pol_width:# and float(output_values["voltage_per_circuit"][j*len(collect_n_total)][2])<60:
                        """is the coil too wide/deep? is there too much pressure? is the too much voltage?"""
                        data_matrix[k][i] = output_dep_values[h][j][i][k]
                    else:
                        data_matrix[k][i] = np.nan
            plt.figure(figsize=(3, 4))
            ax = sns.heatmap(data_matrix, xticklabels=n_tor, yticklabels=n_pol, cmap='viridis', vmin=np.nanmin(data_matrix), vmax=np.nanmax(data_matrix))
            plt.title("Pressure loss in double pancake [bar]")
            plt.xlabel("Number of tor Windings")
            plt.ylabel("Number of pol Windings")
            plt.tight_layout()
            plt.savefig(f'{pressure_dir}/{output_var_name}_outer_{round(outer_radius_values[j]*1000, 2)}_inner_{round(inner_radius_values[j]*1000, 2)}.png')
            plt.close()
