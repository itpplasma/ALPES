import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def draw_coil(number_of_windings_x, number_of_windings_y):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Define parameters
    number_of_windings_y = 2
    number_of_windings_x = 3
    radius = 0.5  # Radius of each circle
    outer_radius = radius * 1.5  # Radius of outer circle
    spacing = 0.2  # Spacing between outer circles
    wire_spacing = 2 * outer_radius + spacing  # Spacing between circles and rows
    
    # Calculate total width and height
    total_width = number_of_windings_x * 2 * outer_radius + (number_of_windings_x + 1) * spacing
    total_height = number_of_windings_y * 2 * outer_radius + (number_of_windings_y + 1) * spacing
    
    # Plot coil
    for i in range(num_windings):
        # Calculate row and column index
        row = i // number_of_windings_x
        col = i % number_of_windings_x
        
        # Calculate x and y coordinates
        x = outer_radius + col * wire_spacing
        y = outer_radius + row * wire_spacing
        
        # Plot outer circle (blue)
        outer_circle = plt.Circle((x, y), outer_radius, color='blue', fill=False, linestyle='--')
        ax.add_patch(outer_circle)
        
        # Plot inner circle (red)
        inner_circle = plt.Circle((x, y), radius, color='red', fill=False, linestyle='--')
        ax.add_patch(inner_circle)
        
        # Add radius labels to the first circle
        if i == 0:
            ax.text(x - outer_radius + 0.1, y + 0.1, f'{outer_radius}', fontsize=12, verticalalignment='center')
            ax.plot([x - outer_radius, x], [y, y], color='black', linewidth=1)
            ax.text(x + 0.05, y + outer_radius + 0.08, f'{spacing}', fontsize=12, verticalalignment='center')
            ax.plot([x, x], [y + outer_radius, y + outer_radius + spacing], color='black', linewidth=1)
        if i == number_of_windings_x:
            ax.text(x - radius + 0.1, y + 0.1, f'{radius}', fontsize=12, verticalalignment='center')
            ax.plot([x - radius, x], [y, y], color='black', linewidth=1)
            ax.text(x + 0.05, y + outer_radius + 0.08, f'{spacing}', fontsize=12, verticalalignment='center')
            ax.plot([x, x], [y + outer_radius, y + outer_radius + spacing], color='black', linewidth=1)
            # Draw radius lines)
    
    # Draw box around coils
    box = Rectangle((-spacing, -spacing), total_width, total_height, edgecolor='black', linewidth=1, fill=False)
    ax.text(-spacing - 0.4, total_height/2-spacing, f'{total_height}', fontsize=12, verticalalignment='center')
    ax.text(total_width/2 - spacing - 0.1, total_height - 0.1, f'{total_width}', fontsize=12, verticalalignment='center')
    ax.add_patch(box)

    # Display important variables
    important_variables = {'Radius': radius, 'Outer Radius': outer_radius, 'Spacing': spacing, 'length_x': wire_spacing*number_of_windings_x-spacing, 'length_y': wire_spacing*number_of_windings_y-spacing}
    text = '\n'.join([f'{key}: {value}' for key, value in important_variables.items()])
    ax.text(total_width + radius * 2, total_height / 2 - spacing, text, fontsize=12, verticalalignment='center')
    
    # Set aspect ratio to equal and adjust plot limits
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-radius * 2, total_width + radius * 2)
    ax.set_ylim(-radius * 2, total_height + radius * 2)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Coil with {} Windings of Bremsleitungen'.format(num_windings))
    ax.axis('off')  # Turn off axes
    plt.show()

# Example usage:
draw_coil(number_of_windings_x, number_of_windings_y)