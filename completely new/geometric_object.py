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
    def __init__(self, name, winding_radius, radius_cooling, number_of_windings_x, number_of_windings_y, spacing_between_windings):
        super().__init__(name)
        self.winding_radius = winding_radius
        self.radius_cooling = radius_cooling
        self.spacing_between_windings = spacing_between_windings
        self.number_of_windings_x = number_of_windings_x
        self.number_of_windings_y = number_of_windings_y
        self.area_winding = math.pi * self.winding_radius ** 2
    
    def get_area_winding(self):
        return 3.14 * self.winding_radius ** 2
    
    def get_total_coil_area(self):
        return 

    def draw_coil(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Define parameters
        num_windings = self.number_of_windings_x * self.number_of_windings_y
        wire_spacing = 2 * self.radius_cooling + self.spacing_between_windings  # Spacing between circles and rows

        # Calculate total width and height
        total_width = self.number_of_windings_x * 2 * self.radius_cooling + (self.number_of_windings_x + 1) * self.spacing_between_windings
        total_height = self.number_of_windings_y * 2 * self.radius_cooling + (self.number_of_windings_y + 1) * self.spacing_between_windings

        # Plot coil
        for i in range(num_windings):
            # Calculate row and column index
            row = i // self.number_of_windings_x
            col = i % self.number_of_windings_x

            # Calculate x and y coordinates
            x = self.radius_cooling + col * wire_spacing
            y = self.radius_cooling + row * wire_spacing

            # Plot outer circle (blue)
            outer_circle = plt.Circle((x, y), self.radius_cooling, color='blue', fill=False, linestyle='--')
            ax.add_patch(outer_circle)

            # Plot inner circle (red)
            inner_circle = plt.Circle((x, y), self.winding_radius, color='red', fill=False, linestyle='--')
            ax.add_patch(inner_circle)

            # Add self.winding_radius labels to the first circle
            if i == 0:
                ax.text(x - self.radius_cooling + 0.1, y + 0.1, f'{self.radius_cooling}', fontsize=12, verticalalignment='center')
                ax.plot([x - self.radius_cooling, x], [y, y], color='black', linewidth=1)
                ax.text(x + 0.1 * self.winding_radius, y + self.radius_cooling + 0.1 * self.winding_radius, f'{self.spacing_between_windings}', fontsize=12, verticalalignment='center')
                ax.plot([x, x], [y + self.radius_cooling, y + self.radius_cooling + self.spacing_between_windings], color='black', linewidth=1)
            if i == self.number_of_windings_x:
                ax.text(x - self.winding_radius*1.1, y + 0.1*self.winding_radius, f'{self.winding_radius}', fontsize=12, verticalalignment='center')
                ax.plot([x - self.winding_radius, x], [y, y], color='black', linewidth=1)
                ax.text(x + 0.05, y + self.radius_cooling + 0.08, f'{self.spacing_between_windings}', fontsize=12, verticalalignment='center')
                ax.plot([x, x], [y + self.radius_cooling, y + self.radius_cooling + self.spacing_between_windings], color='black', linewidth=1)
                # Draw self.winding_radius lines)

        # Draw box around coils
        box = Rectangle((-self.spacing_between_windings, - self.spacing_between_windings), total_width, total_height, edgecolor='black', linewidth=1, fill=False)
        ax.text(-self.spacing_between_windings - 0.4, total_height/2-self.spacing_between_windings, f'{total_height}', fontsize=12, verticalalignment='center')
        ax.text(total_width/2 - self.spacing_between_windings - 0.1, total_height - 0.1, f'{total_width}', fontsize=12, verticalalignment='center')
        ax.add_patch(box)

        # Display important variables
        important_variables = {'Radius': self.winding_radius, 'Outer Radius': self.radius_cooling, 'spacing_between_windings': self.spacing_between_windings, 'length_x': wire_spacing*self.number_of_windings_x-self.spacing_between_windings, 'length_y': wire_spacing*self.number_of_windings_y-self.spacing_between_windings}
        text = '\n'.join([f'{key}: {value}' for key, value in important_variables.items()])
        ax.text(total_width + self.winding_radius * 2, total_height / 2 - self.spacing_between_windings, text, fontsize=12, verticalalignment='center')

        # Set aspect ratio to equal and adjust plot limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-self.winding_radius * 2, total_width + self.winding_radius * 2)
        ax.set_ylim(-self.winding_radius * 2, total_height + self.winding_radius * 2)
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


bremsding = rund("rund", winding_radius = 0.0015, radius_cooling= 0.002, number_of_windings_x=2, number_of_windings_y=3, spacing_between_windings = 0.0002)
bremsding.draw_coil()
