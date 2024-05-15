import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math

class coil_geometry:
    '''geometric object'''
    def __init__(self, name):
        self.name = name
    
    def get_area_winding(self):
        pass

    def draw_coil(self):
        pass

class rund(coil_geometry):
    def __init__(self, name, winding_radius, cooling_radius, number_of_windings_x, number_of_windings_y, spacing_between_windings):
        super().__init__(name)
        self.winding_radius = winding_radius
        self.cooling_radius = cooling_radius
        self.spacing_between_windings = spacing_between_windings
        self.number_of_windings_x = number_of_windings_x
        self.number_of_windings_y = number_of_windings_y
        self.area_winding = math.pi * self.winding_radius ** 2
        self.len_x = (spacing_between_windings + 2 * cooling_radius) * self.number_of_windings_x + self.spacing_between_windings
        self.len_y = (spacing_between_windings + 2 * cooling_radius) * self.number_of_windings_y + self.spacing_between_windings
    
    def get_area_winding(self):
        return 3.14 * self.winding_radius ** 2
    
    def get_total_coil_area(self):
        return 

    def draw_coil(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Define parameters
        num_windings = self.number_of_windings_x * self.number_of_windings_y
        wire_spacing = 2 * self.cooling_radius + self.spacing_between_windings  # Spacing between circles and rows

        # Plot coil
        for i in range(num_windings):
            # Calculate row and column index
            row = i // self.number_of_windings_x
            col = i % self.number_of_windings_x

            # Calculate x and y coordinates
            x = self.cooling_radius + col * wire_spacing
            y = self.cooling_radius + row * wire_spacing

            # Plot outer circle (blue)
            outer_circle = plt.Circle((x, y), self.cooling_radius, color='blue', fill=False, linestyle='--')
            ax.add_patch(outer_circle)

            # Plot inner circle (red)
            inner_circle = plt.Circle((x, y), self.winding_radius, color='red', fill=False, linestyle='--')
            ax.add_patch(inner_circle)

            # Add self.winding_radius labels to the first circle
            if i == 0:
                ax.text(x - self.cooling_radius + 0.1 * self.winding_radius, y + 0.4 * self.winding_radius, 'cooling_radius', fontsize=12, verticalalignment='center')
                ax.plot([x - self.cooling_radius, x], [y, y], color='black', linewidth=1)
                ax.text(x + 0.1 * self.winding_radius, y + self.cooling_radius + 0.1 * self.winding_radius, 'spacing_between_windings', fontsize=12, verticalalignment='center')
                ax.plot([x, x], [y + self.cooling_radius, y + self.cooling_radius + self.spacing_between_windings], color='black', linewidth=1)
            if i == self.number_of_windings_x:
                ax.text(x - self.winding_radius*1.1, y + 0.4*self.winding_radius, 'winding_radius', fontsize=12, verticalalignment='center')
                ax.plot([x - self.winding_radius, x], [y, y], color='black', linewidth=1)
                

        # Draw box around coils
        box = Rectangle((-self.spacing_between_windings, - self.spacing_between_windings), self.len_x, self.len_y, edgecolor='black', linewidth=1, fill=False)
        ax.text(-self.spacing_between_windings - 2 * self.winding_radius, self.len_y/2-self.spacing_between_windings, 'len_y', fontsize=12, verticalalignment='center')
        ax.text(self.len_x/2 - self.spacing_between_windings - 0.4 * self.winding_radius, self.len_y + 0.2 * self.winding_radius, 'len_x', fontsize=12, verticalalignment='center')
        ax.add_patch(box)

        # Display important variables
        important_variables = {'Radius': self.winding_radius, 'Outer Radius': self.cooling_radius, 'spacing_between_windings': self.spacing_between_windings, 'length_x': wire_spacing*self.number_of_windings_x-self.spacing_between_windings, 'length_y': wire_spacing*self.number_of_windings_y-self.spacing_between_windings}
        text = '\n'.join([f'{key}: {value}' for key, value in important_variables.items()])
        ax.text(self.len_x + self.winding_radius * 2, self.len_y / 2 - self.spacing_between_windings, text, fontsize=12, verticalalignment='center')

        # Set aspect ratio to equal and adjust plot limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-self.winding_radius * 2, self.len_x + self.winding_radius * 2)
        ax.set_ylim(-self.winding_radius * 2, self.len_y + self.winding_radius * 2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Coil with {} Windings of Bremsleitungen'.format(num_windings))
        ax.axis('off')  # Turn off axes
        plt.show()


class rect(coil_geometry):
    def __init__(self, name, length, width):
        super().__init__(name)
        self.length = length
        self.width = width
    
    def get_area_winding(self):
        return self.length * self.width
    
    def perimeter(self):
        return 2 * (self.length + self.width)


