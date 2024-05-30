import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



def test_two_parameters(R_min, R_max, number_of_tests_R, W_min, W_max, number_of_tests_W, param1_name, param2_name, output_var_name):
    # Create a grid of values for the two parameters
    param1_values = np.linspace(R_min, R_max, number_of_tests_R)
    param2_values = np.linspace(W_min, W_max, number_of_tests_W)
    
    # Initialize a matrix to store the output variable values
    output_values = np.zeros((number_of_tests_R, number_of_tests_W))
    
    for i, param1_value in enumerate(param1_values):
        for j, param2_value in enumerate(param2_values):
            # Create an instance of the StellaratorDesign class with the current parameter values
            stellarator = StellaratorDesign(material="aluminium", diam_max=None, max_height=None,
                                            max_aspect_ratio=None, min_aspect_ratio=None,
                                            radius_major=None, radius_minor=None,
                                            number_of_coils_per_circuit=None, number_of_circuits=None,
                                            number_of_windings_x=None, number_of_windings_y=None,
                                            max_current_per_m_2=None, specific_resistance=None,
                                            major_winding_radius=None, winding_radius=None, cooling_radius=None, isolation_width = None)
            
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
test_two_parameters(1.0, 10.0, 50, 5, 50, 50, 'radius_major', 'number_of_windings_y', 'I_winding')